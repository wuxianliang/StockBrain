import tushare as ts
from flask import jsonify

def get_s_t(data):
    stock_code = data['code']

    data['date'] = str(data['date'])[0:4]+"-"+str(data['date'])[4:6]+"-"+str(data['date'])[6:9]
    print(data['date'])
    df = ts.get_tick_data(stock_code, date=data['date']).sort_values(by="time")

    result = {'time':df['time'].to_dict(), 'prices': df['price'].to_dict(), 'volumes': df['volume'].to_dict()}
    return jsonify(result)
