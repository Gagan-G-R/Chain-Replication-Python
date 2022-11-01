import client
from distutils.log import error
from http import server
from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
import pandas as pd
import time
import numpy as np
import requests


app = Flask(__name__)


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/node')
def Node():

    # obj = client.Client({"coordinator": 5200, "read": 5201})
    # print(obj.do_read("SD"))
    # print(obj.do_write("SD", "1"))
    # print(obj.do_read("SD"))


if __name__ == '__main__':
    app.run(port=4500, debug=True)
