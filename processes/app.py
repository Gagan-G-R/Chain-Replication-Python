from platform import node
import client
from distutils.log import error
from http import server
from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
import pandas as pd
import time
import numpy as np
import requests
# Mongo
from pymongo import MongoClient
CONNECTION_STRING = "mongodb://localhost:27017/CRAQ"
mongoclient = MongoClient(CONNECTION_STRING)
db = mongoclient['CRAQ']

app = Flask(__name__)


@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/readwrite')
def ReadWrite():
    searchT = request.args.get('searchT')
    key = request.args.get('Key')
    value = request.args.get('Value')
    coo_id = request.args.get('coo_id')
    node_id = request.args.get('node_id')
    print("<<FLASK READ REQ>>", searchT, key, value, coo_id, node_id)
    obj = client.Client({"coordinator": coo_id, "read": node_id})
    respView = {}
    if searchT == 'r':
        try:
            responce = obj.do_read(key)
            respView['key'] = key
            respView['value'] = responce[key]
        except:
            responce = "!err"
            key = '-----ERR-----'
            value = '-----ERR-----'
            respView['key'] = key
            respView['value'] = value

    else:
        if key.strip() == '':
            return redirect('/node?coo_no='+coo_id+'&node_no='+node_id)
        responce = obj.do_write(key, value)
        if not responce:
            key = '-----ERR-----'
            value = '-----ERR-----'
        respView['key'] = key
        respView['value'] = value

    print("<<FLASK READ/WRITE RESPONSE>>", responce)
    web_obj = db[node_id].find()
    result = list(web_obj)
    return render_template('Node.html', node_id=node_id, coo_no=coo_id, node_data=result, respView=respView)


@app.route('/node')
def Node():
    coo_id = request.args.get('coo_no')
    node_id = request.args.get('node_no')
    if node_id == '' or not node_id:
        return redirect('/coordinator?coo_no='+coo_id)
    else:
        print("<<FLASK Node>>", coo_id, node_id)
        # obj = client.Client({"coordinator": coo_id, "read": node_id})

        web_obj = db[node_id].find()
        result = list(web_obj)

        return render_template('Node.html', node_id=node_id, coo_no=coo_id, node_data=result, respView=[])


@app.route('/coordinator')
def Coordinator():
    coo_id = request.args.get('coo_no')
    print(coo_id)
    collections = db.list_collection_names()
    no_of_collections = len(db.list_collection_names())
    result = {}
    for collection in collections:
        obj = db[collection].find()
        result[collection] = list(obj)

    return render_template('coord.html', coo_no=coo_id, nodeslist=result)


@app.route('/addnode', methods=['POST'])
def addnode():
    coo_id = request.args.get('coo_no')
    print(coo_id)
    node_id = request.args.get('node_no')
    print(node_id)
    global allNodes
    allNodes.append(node_id)


if __name__ == '__main__':
    app.run(port=4500, debug=True)
