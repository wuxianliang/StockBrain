import dask.dataframe as dd
from dask.multiprocessing import get
import pandas as pd
import numpy as np
from time import clock
from multiprocessing import cpu_count, Pool
from numba import jit
import tushare as ts
import faiss

'''
a = pd.DataFrame([1,2,3])
print(a[0:10])

dates = ts.trade_cal()
test =dates['calendarDate'].tolist()

d= {"date":test}
open_dates = dates.loc[dates['isOpen']==1].reset_index()
test.reverse()
d['date'].reverse()
end = open_dates.loc[open_dates.loc[open_dates['calendarDate']=='2014-03-26'].index +10, 'calendarDate']
print(end.values[0])
'''
k_data = pd.read_csv('/home/wxl/p/StockBrain/backend/data/ashareeodprices.csv', low_memory=False)
#print('finish reading')
#pre_k_data = dd.from_pandas(pre_k_data, npartitions = nCores)
#pre_k_data['TRADE_DT'] = pre_k_data.map_partitions(lambda df: df['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9]) )
#k_data['TRADE_DT'] = k_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9])
#print('finish design')
#pre_k_data.compute(get=get)
a = clock()
stock = k_data.loc[k_data['S_INFO_WINDCODE'] == '600031.SH']
#print(stock.index)

#stock["TRADE_DT"] = pd.to_datetime(stock['TRADE_DT'])
stock = stock.set_index('TRADE_DT')
b = clock()
print(b-a)
print(stock['2013-01-01':'2013-02-01'].T.to_json())

'''
def sx(x):
    if x[0] == '6':
        return x + '.SH'
    elif x[0] == '0' or x[0] == '3':
        return x + '.SZ'
wind_codes = list(map(lambda x: sx(x) , ts.get_stock_basics().index.tolist()))[0:3]

def get_k(code):
    stock = pre_k_data.loc[pre_k_data['S_INFO_WINDCODE'] == code].sort_values(by="TRADE_DT").reset_index()
    close = stock['S_DQ_CLOSE'].tolist()
    open = stock['S_DQ_OPEN'].tolist()
    low = stock['S_DQ_LOW'].tolist()
    high = stock['S_DQ_HIGH'].tolist()
    date = stock['TRADE_DT'].tolist()
    results = []
    print(code)
    i=0
    dim = 2
    while i + dim < len(open):
        result = {'open':open[i:i+dim], 'close':close[i:i+dim], 'low':low[i:i+dim], 'high':high[i:i+dim]}
        results.append({'value':result, 'code': code, 'date': date[i]})
        i+=1
    return results
start = clock()
bases = [[], []]
pool = Pool(processes=nCores,)
results = [y for x in pool.imap_unordered(get_k, wind_codes) for y in x]
r = [{},{}]+results
pool.close()
pool.join()

#k_data = base(wind_codes, pre_k_data)
end = clock()
print(end-start)
print(r[:3])
def normalize(value):
    open = list(map(lambda x: x/value['open'][0], value['open']))
    close = list(map(lambda x: x/value['close'][0], value['close']))
    low = list(map(lambda x: x/value['low'][0], value['low']))
    high = list(map(lambda x: x/value['high'][0], value['high']))
    return open+close+low+high
xb = np.array(list(map(lambda x: normalize(x['value']), r[:3]))).astype('float32')
print(xb)
def get_k(xb, params):

    dim = 2

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
    results = list(map(lambda x: xb[x], I[0]))
    end = clock()
    print(end-start)
    print(params)
    return results #not yet
'''
