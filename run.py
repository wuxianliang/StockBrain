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
#import ray.dataframe as rpd
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
start = clock()
#prepare raw data
pre_index_data = pd.read_csv('/home/wxl/p/StockBrain/backend/data/aindexeodprices.csv', low_memory=False)
index_data = pre_index_data
#index_data['TRADE_DT'] = index_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9])
pre_k_data = pd.read_csv('/home/wxl/p/StockBrain/backend/data/ashareeodprices.csv', low_memory=False)
k_data = pre_k_data

def sx(x):
    if x[0] == '6':
        return x + '.SH'
    elif x[0] == '0' or x[0] == '3':
        return x + '.SZ'
wind_codes = list(map(lambda x: sx(x) , ts.get_stock_basics().index.tolist()))
dates = ts.trade_cal()
print('finish loading data')
end = clock()
print(end -start)
def divid_k(code, dim):
    stock = k_data.query("S_INFO_WINDCODE == @code").sort_values(by="TRADE_DT").reset_index()
    close = stock['S_DQ_CLOSE'].tolist()
    open = stock['S_DQ_OPEN'].tolist()
    low = stock['S_DQ_LOW'].tolist()
    high = stock['S_DQ_HIGH'].tolist()
    #stock['TRADE_DT'] = stock['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9])
    date = stock['TRADE_DT'].tolist()
    volume = stock['S_DQ_VOLUME'].tolist()
    results = []
    print(code+str(dim))
    i=0
    while i + dim < len(open):
        result = {'open':open[i:i+dim], 'close':close[i:i+dim], 'low':low[i:i+dim], 'high':high[i:i+dim]}
        results.append({'value':result, 'code': code, 'date': date[i:i+dim], 'volume': volume[i:i+dim]})
        i+=1
    return results


init = [[],[]]
def normalize(value, volume):
    open = list(map(lambda x: x/value['open'][0], value['open']))
    close = list(map(lambda x: x/value['open'][0], value['close']))
    low = list(map(lambda x: x/value['open'][0], value['low']))
    high = list(map(lambda x: x/value['open'][0], value['high']))
    if volume[0]==0:
        volume = list(map(lambda x: 1, volume))
    else:
        volume = list(map(lambda x: x/volume[0], volume))
    return open+close+low+high+volume
def make_bases():
    xb = []
    bases = []
    for i in range(10):
        pool = Pool(processes=nCores,)
        j = i+2
        partial_divid_k = partial(divid_k, dim=j)
        result = [y for x in pool.imap_unordered(partial_divid_k, wind_codes) for y in x] # for real-world
        bases.append(result)
        xb.append(np.array(list(map(lambda x: normalize(x['value'], x['volume']), result))).astype('float32'))
        pool.close()
        pool.join()
    return {'xb': xb, 'bases':bases}
base = make_bases()
bases = init + base['bases']
xb = init + base['xb']

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
    app.run(debug=False, port=5000, processes=nCores)
