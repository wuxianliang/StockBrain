import tushare as ts

def get_s_t(data):
    stock_code = str(data[0])
    df = ts.get_tick_data(stock_code, date=str(data[1])).sort_values(by="time")
    return {'time':df['time'].to_dict().values(), 'values': df['price'].to_dict().values(), 'volumes': df['volume'].to_dict().values()}
