def get_i_k(index_data, index_code):
    data = index_data.loc[index_data['S_INFO_WINDCODE'] == index_code]
    result = data.sort_values(by="TRADE_DT").reset_index().T.to_dict().values()
    return result
