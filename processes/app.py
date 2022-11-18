from platform import node
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
    coo_id=request.args.get('coo_no')
    node_id=request.args.get('node_no')
    print(coo_id)
    print(node_id)
    # obj = client.Client({"coordinator": 5200, "read": 5201})
    # print(obj.do_read("SD"))
    # print(obj.do_write("SD", "1"))
    # print(obj.do_read("SD"))
    return render_template('Node.html',node_id=node_id,coo_no=coo_id)

@app.route('/coordinator')
def Coordinator():
    coo_id=request.args.get('coo_no')
    print(coo_id)
    nodes=[{
        "id":1,
        "key":"SD",
        "value":"1",
        "status":"True",
    },{
        "id":1,
        "key":"SD",
        "value":"1",
        "status":"True",
    },{
        "id":1,
        "key":"SD",
        "value":"1",
        "status":"True",
    },{
        "id":1,
        "key":"SD",
        "value":"1",
        "status":"True",
    }]
    return render_template('coord.html',coo_no=coo_id,nodeslist=nodes)    

@app.route('/addnode',methods=['POST'])
def addnode():
    coo_id=request.args.get('coo_no')
    print(coo_id)
    node_id=request.args.get('node_no')
    print(node_id)
    global allNodes
    allNodes.append(node_id)

if __name__ == '__main__':
    app.run(port=4500, debug=True)
    allNodes=[{
        "id":1,
        "key":"SD",
        "value":"1",
        "status":"True",
    },]
    
