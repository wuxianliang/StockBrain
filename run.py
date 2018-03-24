from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS
import requests
from importlib import reload
from backend import random_number
from backend import index_k_line
from backend import stock_k_line
from backend import stock_ticks
from backend import index_ticks
from backend import similar_ticks
from backend import similar_k_line
from backend import similar_stocks
from multiprocessing import cpu_count, Pool
import tushare as ts
from time import clock
import numpy as np
from functools import partial
nCores = cpu_count()
import pandas as pd
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#prepare raw data
rawkdata = []
pre_index_data = pd.read_csv('/home/wxl/p/StockBrain/backend/data/aindexeodprices.csv', low_memory=False)
pre_index_data['TRADE_DT'] = pre_index_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9]) #, meta=('TRADE_DT', 'str')
index_data = pre_index_data
pre_k_data = pd.read_csv('/home/wxl/p/StockBrain/backend/data/ashareeodprices.csv', low_memory=False)
pre_k_data['TRADE_DT'] = pre_k_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9]) #, meta=('TRADE_DT', 'str')
k_data = pre_k_data
def sx(x):
    if x[0] == '6':
        return x + '.SH'
    elif x[0] == '0' or x[0] == '3':
        return x + '.SZ'
wind_codes = list(map(lambda x: sx(x) , ts.get_stock_basics().index.tolist()))
dates = pd.read_csv('/home/wxl/p/StockBrain/backend/data/asharecalendar.csv')["TRADE_DAYS"].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9])
print('finish loading data')
def divid_k(code, dim):
    stock = k_data.loc[k_data['S_INFO_WINDCODE'] == code].sort_values(by="TRADE_DT").reset_index()
    close = stock['S_DQ_CLOSE'].tolist()
    open = stock['S_DQ_OPEN'].tolist()
    low = stock['S_DQ_LOW'].tolist()
    high = stock['S_DQ_HIGH'].tolist()
    date = stock['TRADE_DT'].tolist()
    results = []
    print(code+str(dim))
    i=0
    while i + dim < len(open):
        result = {'open':open[i:i+dim], 'close':close[i:i+dim], 'low':low[i:i+dim], 'high':high[i:i+dim]}
        results.append({'value':result, 'code': code, 'date': date[i:i+dim]})
        i+=1
    return results
start = clock()
#not yet finish
bases = [[], []]
xb = [[], []]
def normalize(value):
    open = list(map(lambda x: x/value['open'][0], value['open']))
    close = list(map(lambda x: x/value['close'][0], value['close']))
    low = list(map(lambda x: x/value['low'][0], value['low']))
    high = list(map(lambda x: x/value['high'][0], value['high']))
    return open+close+low+high
def make_bases():
    xb = []
    bases = []
    for i in range(10):
        pool = Pool(processes=50,)
        j = i+2
        partial_divid_k = partial(divid_k, dim=j)
        result = [y for x in pool.imap_unordered(partial_divid_k, wind_codes) for y in x]
        bases.append(result)
        xb.append(np.array(list(map(lambda x: normalize(x['value']), result))).astype('float32'))
        pool.close()
        pool.join()
    return {'xb': xb, 'bases':bases}
bases = bases + make_bases()['bases']
xb = xb + make_bases()['xb']
end = clock()
print(end-start)


#ticks =
#define APIs
@app.route('/api/random')
def test():
    reload(random_number)
    return random_number.get_random_number()

@app.route('/api/index_k_line', methods=['POST'])
def index_k():
    index_code = str(request.get_data(), encoding='utf-8')
    print(index_code)
    reload(index_k_line)
    return index_k_line.get_i_k(index_data, index_code)

@app.route('/api/index_ticks', methods=['POST'])
def index_t():
    encoding = request.get_data().decode("utf-8")
    data = json.loads(encoding)
    reload(index_ticks)
    return index_ticks.get_i_t(data)

@app.route('/api/stock_k_line', methods=['POST'])
def stock_k():
    stock_code = str(request.get_data(), encoding='utf-8')
    reload(stock_k_line)
    return stock_k_line.get_s_k(k_data, stock_code)

@app.route('/api/stock_ticks', methods=['POST'])
def stock_t():
    encoding = request.get_data().decode("utf-8")
    data = json.loads(encoding)
    reload(stock_ticks)
    return stock_ticks.get_s_t(data)

@app.route('/api/similar_k_line', methods=['POST'])
def similar_k():
    encoding = request.get_data().decode("utf-8")
    params = json.loads(encoding)
    reload(similar_k_line)
    reload(similar_stocks)
    codes = similar_stocks.get_s(params['queryCode'])
    if params['kLineFirst']:
        dim = len(params['pickedStockKLine']['values'])
    else:
        dim = len(params['pickedStockTicks']['values'])
    return similar_k_line.get_k(bases[dim], xb[dim], params, k_data, dates)

@app.route('/api/similar_ticks', methods=['POST'])
def similar_t():
    params = request.get_data()
    reload(get_similar_ticks)
    return similar_ticks.get_t(ticks, parmas)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True, port=5000, processes=nCores)
