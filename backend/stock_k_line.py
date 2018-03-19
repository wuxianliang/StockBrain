from flask import jsonify

def get_s_k(k_data, stock_code):
    if stock_code[0] == '6':
        stock_code = stock_code + '.SH'
    elif stock_code[0] == '0' or stock_code[0] == '3':
        stock_code = stock_code + '.SZ'
    stock = k_data.loc[k_data['S_INFO_WINDCODE'] == stock_code]
    print(stock)
    result = stock.sort_values(by="TRADE_DT").reset_index().T.to_json()
    return result
