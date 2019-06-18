from flask import Flask
from flask import abort

app = Flask(__name__)

@app.route("/register_pattern")
def register_pattern():
    abort(501, "Not Implemented")

@app.route("/play_pattern")
def play_pattern():
    abort(501, "Not Implemented")

@app.route("/get_playing_pattern")
def get_playing_pattern():
    abort(501, "Not Implemented")

@app.errorhandler(501)
def error_handler(error):
    return "Error", error.code

