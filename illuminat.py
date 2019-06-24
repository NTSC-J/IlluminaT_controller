#!/usr/bin/env python3

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request

from rpi_ws281x import *

from itertools import repeat

import threading
import time

app = Flask(__name__)

LED_COUNT = 8 * 8
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
PERIOD = 1. / 1
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# 0th element: lights out
patterns = [[list(repeat(Color(255, 0, 0), LED_COUNT)), list(repeat(Color(0, 255, 0), LED_COUNT))]]
print(patterns)
playing_id = 0
changed_id = False

def led_thread():
    global strip
    global patterns
    global playing_id
    global changed_id
    while True:
        target_time = time.monotonic()
        for frame in patterns[playing_id]:
            # assert(len(frame) == LED_COUNT)
            if changed_id:
                changed_id = False
                print("Changed ID: " + str(playing_id))
                break
            for lednum, led in enumerate(frame):
                strip.setPixelColor(lednum, led)
            strip.show()
            target_time += PERIOD
            sleep_time = target_time - time.monotonic()
            if 0 < sleep_time:
                time.sleep(sleep_time)

@app.route("/register_pattern", methods=['POST'])
def register_pattern():
    req = request.json
    pattern = req.get("pattern")
    print(pattern)
    id_ = len(patterns)
    patterns.append(pattern)
    print(pattern)
    return jsonify(id=id_)

@app.route("/play_pattern", methods=['POST'])
def play_pattern():
    global playing_id
    global changed_id
    req = request.json
    id_ = req.get("id")
    if len(patterns) <= id_:
        abort(404, "Not found")
    playing_id = id_
    changed_id = True
    return ''

@app.route("/get_playing_pattern", methods=['GET'])
def get_playing_pattern():
    return jsonify(id=playing_id)

@app.errorhandler(404)
@app.errorhandler(501)
def error_handler(error):
    if error.code == 404:
        return "Not Found", error.code
    elif error.code == 501:
        return "Not Implemented", error.code
    else:
        return "Error", error.code

if __name__ == '__main__':
    strip.begin()
    thread = threading.Thread(target=led_thread)
    thread.start()

    # dangerous
    app.run(host='0.0.0.0')

