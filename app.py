# app.py
from flask import Flask, request, jsonify
import pandas as pd
import openpyxl
import reader as R

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>use '/pull_data' to pull info from sheet</h1>"

@app.get("/pull_data")
def get_countries():
    return jsonify(R.dictify())

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

