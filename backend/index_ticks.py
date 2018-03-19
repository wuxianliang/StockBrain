import tushare as ts
from flask import jsonify

def get_i_t(data):
    index_code = data['code']
    cons = ts.get_apis()
    df = ts.tick(index_code, conn=cons, date=data['date'], asset='INDEX')
    result = {'time':df['datetime'].to_dict(), 'prices': df['price'].to_dict(), 'volumes': df['vol'].to_dict()}
    return jsonify(result)
