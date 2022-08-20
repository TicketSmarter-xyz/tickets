import json
import time
import datetime
import os
from random import random
from time import sleep
import pdb
import flask
from flask import Flask, render_template, url_for, copy_current_request_context, request, redirect
from web3 import Web3, HTTPProvider, exceptions, _utils
from web3.contract import ConciseContract
import regex as re


application = Flask(__name__)



@application.route("/")
def index(): #landing
    return "Welcome"

@application.route("/login")
def login():
    return "please login"

@application.route("/dashboard")
def dashboard():
    return "dashboard"

@application.route("/event_<event_id>")
def event_page(event_id):
    return "Welcome to event " + event_id

@application.route("/marketplace")
def marketplace():
    return "marketplace"



if __name__ == '__main__':
    print("application.py is RUNNING")
    application.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)
