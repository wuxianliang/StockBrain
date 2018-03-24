import faiss
import numpy as np
import pandas as pd
import tushare as ts
from flask import jsonify
from multiprocessing import cpu_count, Pool
from functools import partial
nCores = cpu_count()
import json
from time import clock
# need to speed up


#too slow
def back_and_front(results, k_data, dates):
    kResults =[]
    for item in results:
        a = clock()
        stock = k_data.loc[k_data['S_INFO_WINDCODE'] == item['code']]
        b = clock()
        stock["TRADE_DT"] = pd.to_datetime(stock['TRADE_DT'])
        stock = stock.set_index('TRADE_DT', drop=False).sort_index()
        #b = clock()
        print(b - a)
        c = clock()
        dates = ts.trade_cal()
        open_dates = dates.loc[dates['isOpen']==1].reset_index()
        start = open_dates.loc[open_dates.loc[open_dates['calendarDate']==item['date'][0]].index -10, 'calendarDate'].values[0]
        item['date'].reverse()
        end = open_dates.loc[open_dates.loc[open_dates['calendarDate']==item['date'][0]].index +10, 'calendarDate'].values[0]
        kResults.append(stock[start:end].T.to_json())
        d = clock()
        print(d-c)
    return kResults

def get_k(bases, xb, params, k_data, dates):
    if params['kLineFirst']:
        dim = len(params['pickedStockKLine']['values'])
    else:
        dim = len(params['pickedStockTicks']['values'])

    #query
    kLine = params['pickedStockKLine']['values']
    open = list(map(lambda x:x[0], kLine))
    close = list(map(lambda x:x[1], kLine))
    low = list(map(lambda x:x[2], kLine))
    high = list(map(lambda x:x[3], kLine))
    query = list(map(lambda x: x/open[0], open))+list(map(lambda x: x/close[0], close)) +list(map(lambda x: x/low[0], low))+list(map(lambda x: x/high[0], high))

    xq = np.array( [np.array(query)]).astype('float32')

    ngpus = faiss.get_num_gpus()
    #build index
    cpu_index = faiss.IndexFlatL2(dim*4)
    gpu_index = faiss.index_cpu_to_all_gpus(cpu_index)
    gpu_index.add(xb)
    start = clock()
    D, I = gpu_index.search(xq, 10)
    #have not done
    results = list(map(lambda x: bases[x], I[0]))
    end = clock()
    print(end-start)

    return jsonify(back_and_front(results, k_data, dates)) #not yet
