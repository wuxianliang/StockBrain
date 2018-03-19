import dask.dataframe as dd
from dask.multiprocessing import get
import pandas as pd
from time import clock
from multiprocessing import cpu_count, Pool
from numba import jit
import tushare as ts
nCores = cpu_count()
print(nCores)

pre_k_data = pd.read_csv('/home/wxl/p/StockBrain/backend/data/ashareeodprices.csv', low_memory=False)
#print('finish reading')
#pre_k_data = dd.from_pandas(pre_k_data, npartitions = nCores)
#pre_k_data['TRADE_DT'] = pre_k_data.map_partitions(lambda df: df['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9]) )
pre_k_data['TRADE_DT'] = pre_k_data['TRADE_DT'].apply(lambda x: str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:9])
#print('finish design')
#pre_k_data.compute(get=get)

def sx(x):
    if x[0] == '6':
        return x + '.SH'
    elif x[0] == '0' or x[0] == '3':
        return x + '.SZ'
wind_codes = list(map(lambda x: sx(x) , ts.get_stock_basics().index.tolist()))

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
    dim = 10
    while i + dim < len(open):
        result = {'open':open[i:i+dim], 'close':close[i:i+dim], 'low':low[i:i+dim], 'high':high[i:i+dim]}
        results.append({'value':result, 'code': code, 'date': date[i]})
        i+=1
    return results
start = clock()
pool = Pool(processes=50,)
abc = pool.map_async(get_k, wind_codes)
pool.close()
pool.join()

#k_data = base(wind_codes, pre_k_data)
end = clock()
print(end-start)
