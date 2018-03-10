def get_s_k(k_data, stock_code):
    stock = k_data.loc[k_data['S_INFO_WINDCODE'] == stock_code]
    result = stock.sort_values(by="TRADE_DT").reset_index().T.to_dict().values()
    return result
