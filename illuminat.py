from flask import Flask
from flask import abort
from flask import jsonify

from rpi_ws281x import *

from itertools import repeat

app = Flask(__name__)

LED_COUNT = 8 * 8
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
PERIOD = 1. / 15
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# 0th element: lights out
patterns = list(list(list(repeat(Color(0, 0, 0), LED_COUNT))))
playing_id = 0
changed_id = False

def led_thread():
    while True:
       for frame in range(len(patterns[playing_id])):
           if changed_id:
               changed_id = False
               break
           for led in range(len(patterns[playing_id][frame])): # LED_COUNT
               strip.setPixelColor(led, patterns[playing_id][frame][led])

@app.route("/register_pattern", methods=['POST'])
def register_pattern():
    req = request.json
    id_ = len(patterns)
    patterns.append(req.pattern)
    return jsonify(id=id_)

@app.route("/play_pattern", methods=['POST'])
def play_pattern():
    req = request.json
    id_ = req.id
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
    elif error.code = 501:
        return "Not Implemented", error.code
    else:
        return "Error", error.code

if __name__ == '__main__':
    strip.begin()
    thread = threading.Thread(target=led_thread)
    thread.start()

    # dangerous
    app.run(host='0.0.0.0', debug=True)

