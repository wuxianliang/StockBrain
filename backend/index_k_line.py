from flask import jsonify
#from multiprocessing import cpu_count
def get_i_k(index_data, index_code):
    # = cpu_count()
    #print(n)
    data = index_data.loc[index_data['S_INFO_WINDCODE'] == index_code]
    result = data.sort_values(by="TRADE_DT").reset_index().T.to_json()
    return result
