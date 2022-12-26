# app.py
from flask import Flask, request, jsonify
import pandas as pd
import openpyxl
import reader as R

app = Flask(__name__)

@app.route('/')
def index():
    """
    Display a message when the root URL is accessed.
    """
    return "<h1>use '/pull_data' to pull info from sheet</h1>"

@app.route("/pull_data", methods=["GET"])
def get_countries():
    """
    Return the data from the Google Sheets spreadsheet as a JSON object.
    
    Returns:
    - JSON object: The data from the Google Sheets spreadsheet, converted into a list of dictionaries.
    """
    return jsonify(R.dictify())

def shutdown_server():
    """
    Shut down the server.
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=["GET"])
def shutdown():
    """
    Shut down the server when this URL is accessed.
    
    Returns:
    - str: A message indicating that the server is shutting down.
    """
    shutdown_server()
    return 'Server shutting down...'
