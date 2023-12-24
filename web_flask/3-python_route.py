#!/usr/bin/python3
"""Starts a Flask web application with additional routes"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """Displays 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """Displays 'C ' followed by the value of the text variable"""
    return "C {}".format(escape(text))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def display_python(text='is cool'):
    """Displays 'Python ' followed by value oftext variable"""
    return "Python {}".format(escape(text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
