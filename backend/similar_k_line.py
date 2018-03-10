import faiss
import numpy as np
# need to speed up
def base(dim, wind_codes, all_data):
    data = []
    count =0
    for item in wind_codes:
        stock = all_data.loc[all_data['S_INFO_WINDCODE'] == item].sort_values(by="TRADE_DT").reset_index()
        close = map(lambda x: round(x, 2), stock['S_DQ_CLOSE'].to_dict().values())
        open = map(lambda x: round(x, 2), stock['S_DQ_OPEN'].to_dict().values())
        low = map(lambda x: round(x, 2), stock['S_DQ_LOW'].to_dict().values())
        high = map(lambda x: round(x, 2), stock['S_DQ_HIGH'].to_dict().values())
        date = stock['TRADE_DT'].to_dict().values()
        i = 0
        while i + dim < len(close):
            result = {'open':open[i:i+dim], 'close':close[i:i+dim], 'low':low[i:i+dim], 'high':high[i:i+dim]}
            data.append({'value':result, 'code': item, 'date': date[i]})
            i += 1
        print count
        count +=1
    return data
def normalize(value):
    open = map(lambda x: x/value['open'][0], value['open'])
    close = map(lambda x: x/value['close'][0], value['close'])
    low = map(lambda x: x/value['low'][0], value['low'])
    high = map(lambda x: x/value['high'][0], value['high'])
    return open+close+low+high

#return value have not done
def results(wind_codes, I):
    similar_data = wind_codes[I]
    return similar_data

def get_k(wind_codes, k_data, params):
    if params['kLineFirst']:
        dim = len(params['pickedStockKLine']['values'])
    else:
        dim = len(params['pickedStockTicks']['values'])
    #database
    value_base = base(dim, wind_codes, k_data)

    xb = np.array(map(lambda x: normalize(x['value']), value_base)).astype('float32')
    #query
    kLine = params['pickedStockKLine']['values']
    open = map(lambda x:x[0], kLine)
    close = map(lambda x:x[1], kLine)
    low = map(lambda x:x[2], kLine)
    high = map(lambda x:x[3], kLine)
    query = map(lambda x: x/open[0], open)+map(lambda x: x/close[0], close) +map(lambda x: x/low[0], low)+map(lambda x: x/high[0], high)

    xq = np.array([query]).astype('float32')
    #build index
    index = faiss.IndexFlatL2(dim*4)
    index.add(xb)

    D, I = index.search(xq, 10)
    #have not done
    result = map(lambda x: value_base[x], I[0])
    return result
