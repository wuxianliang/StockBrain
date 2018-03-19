import faiss
import numpy as np
from flask import jsonify
from multiprocessing import cpu_count, Pool
from functools import partial
nCores = cpu_count()
import json
from time import clock
# need to speed up


def base(code, dim, k_data):
    stock = k_data.loc[k_data['S_INFO_WINDCODE'] == code].sort_values(by="TRADE_DT").reset_index()
    close = stock['S_DQ_CLOSE'].tolist()
    open = stock['S_DQ_OPEN'].tolist()
    low = stock['S_DQ_LOW'].tolist()
    high = stock['S_DQ_HIGH'].tolist()
    date = stock['TRADE_DT'].tolist()
        #data =  {'open':open, 'close': close, 'high': high, 'low': low, 'date': date, 'code': code}
    results = []
    print(code)
    i=0
    while i + dim < len(open):
        result = {'open':open[i:i+dim], 'close':close[i:i+dim], 'low':low[i:i+dim], 'high':high[i:i+dim]}
        results.append({'value':result, 'code': code, 'date': date[i]})
        i+=1

    return results

def normalize(value):
    open = list(map(lambda x: x/value['open'][0], value['open']))
    close = list(map(lambda x: x/value['close'][0], value['close']))
    low = list(map(lambda x: x/value['low'][0], value['low']))
    high = list(map(lambda x: x/value['high'][0], value['high']))
    return open+close+low+high

#return value have not done
def back_or_front(results, param):
    similar_data = wind_codes[I]
    return jsonify({'result':result})

def get_k(xb, params):
    if params['kLineFirst']:
        dim = len(params['pickedStockKLine']['values'])
    else:
        dim = len(params['pickedStockTicks']['values'])
    #database
    #pool = Pool(processes=50,)
    #partial_base = partial(base, dim=dim, k_data=k_data)
    #bases = pool.map_async(partial_base, wind_codes)
    #pool.close()
    #pool.join()
    #value_base = []
    #for i in bases:
    #    value_base.extend(i)

    #value_base = base(dim, wind_codes, k_data)

    #xb = np.array(list(map(lambda x: normalize(x['value']), value_base))).astype('float32')

    #query
    kLine = params['pickedStockKLine']['values']
    open = list(map(lambda x:x[0], kLine))
    close = list(map(lambda x:x[1], kLine))
    low = list(map(lambda x:x[2], kLine))
    high = list(map(lambda x:x[3], kLine))
    query = list(map(lambda x: x/open[0], open))+list(map(lambda x: x/close[0], close)) +list(map(lambda x: x/low[0], low))+list(map(lambda x: x/high[0], high))

    xq = np.array( [np.array(query)]).astype('float32')


    #build index
    index = faiss.IndexFlatL2(dim*4)
    index.add(xb)
    start = clock()
    D, I = index.search(xq, 10)
    #have not done
    results = list(map(lambda x: xb[x], I[0]))
    end = clock()
    print(end-start)
    return back_or_front(results, paramss['back_or_front']) #not yet
