import tushare as ts

def get_i_t(data):
    index_code = str(data[0])
    cons = ts.get_apis()
    df = ts.tick(index_code, conn=cons, date=str(data[1]), asset='INDEX')
    return {'time':df['datetime'].to_dict().values(), 'values': df['price'].to_dict().values(), 'volumes': df['vol'].to_dict().values()}
