from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
import requests
from importlib import reload
from backend import random_number
from backend import index_k_line
from backend import stock_k_line
from backend import stock_ticks
from backend import index_ticks
import pandas as pd
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#prepare raw data
rawkdata = []
pre_index_data = pd.read_csv('/home/wxl/dumps/aindexeodprices.csv', low_memory=False)
pre_index_data['TRADE_DT'] = pre_index_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9]) #, meta=('TRADE_DT', 'str')
index_data = pre_index_data
pre_k_data = pd.read_csv('/home/wxl/dumps/ashareeodprices.csv', low_memory=False)
pre_k_data['TRADE_DT'] = pre_k_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9]) #, meta=('TRADE_DT', 'str')
k_data = pre_k_data
description = pd.read_csv('/home/wxl/dumps/asharedescription.csv') #divided by comma in mysql
wind_codes = description["S_INFO_WINDCODE"].to_dict().values()#.persist().compute()
dates = pd.read_csv('/home/wxl/dumps/asharecalendar.csv')["TRADE_DAYS"].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9])

#define APIs
@app.route('/api/random')
def test():
    reload(random_number)
    return random_number.get_random_number()

@app.route('/api/index_k_line')
def index_k():
    code = requests.get_json()
    reload(index_k_line)
    return index_k_line.get_i_k()

@app.route('/api/index_ticks')
def index_t():
    reload(index_ticks)
    return index_ticks.get_i_t()

@app.route('/api/stock_k_line')
def stock_k():
    reload(stock_k_line)
    return stock_k_line.get_s_k()

@app.route('/api/stock_ticks')
def stock_t():
    reload(stock_ticks)
    return stock_ticks.get_s_t()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
