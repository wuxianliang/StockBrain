import faiss
import numpy as np
import pandas as pd
#import ray.dataframe as pd
import tushare as ts
from flask import jsonify
from multiprocessing import cpu_count, Pool
from functools import partial
nCores = cpu_count()
import json
from time import clock
# need to speed up
def back_and_front(results, k_data, dates):
    kResults =[]
    for item in results:
        code = item["code"]
        stock = k_data.query('S_INFO_WINDCODE == @code')
        stock = stock.set_index('TRADE_DT', drop=False).sort_index()
        open_dates = dates.query('isOpen == 1').reset_index()
        first_date = str(item['date'][0])[0:4]+"-"+str(item['date'][0])[4:6]+"-"+str(item['date'][0])[6:9]
        start = open_dates.loc[open_dates.loc[open_dates['calendarDate']==first_date].index -5, 'calendarDate'].values[0].replace('-', '')
        item['date'].reverse()
        last_date = str(item['date'][0])[0:4]+"-"+str(item['date'][0])[4:6]+"-"+str(item['date'][0])[6:9]
        end = open_dates.loc[open_dates.loc[open_dates['calendarDate']==last_date].index +5, 'calendarDate'].values[0].replace('-', '')
        kResults.append(stock.loc[slice(start, end),:].T.to_json())
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
    volume = params['pickedStockKLine']['volumes']
    query = list(map(lambda x: x/open[0], open))+list(map(lambda x: x/open[0], close)) +list(map(lambda x: x/open[0], low))+list(map(lambda x: x/open[0], high))+list(map(lambda x: x[1]/volume[0][1], volume))
    xq = np.array( [np.array(query)]).astype('float32')
    ngpus = faiss.get_num_gpus()
    #build index
    start = clock()
    cpu_index = faiss.IndexFlatL2(dim*5)
    gpu_index = faiss.index_cpu_to_all_gpus(cpu_index)
    gpu_index.add(xb)

    D, I = gpu_index.search(xq, 10)
    #have not done
    end = clock()
    print(end-start)
    results = list(map(lambda x: bases[x], I[0]))
    print(results)
    return jsonify(back_and_front(results, k_data, dates)) #not yet
