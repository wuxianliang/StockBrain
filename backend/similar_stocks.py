import tushare as ts
import pandas as pd
#import ray.dataframe as pd
'''
return the area of query. the rule is with the same industry, area, small , concept or similar value.
'''
def get_s(code):
    industries = ts.get_industry_classified()
    concepts = ts.get_concept_classified()
    areas = ts.get_area_classified()
    totals = ts.get_stock_basics()
    i = industries.loc[industries['code'] == code]['c_name']
    c = concepts.loc[concepts['code'] == code]['c_name']
    a = areas.loc[areas['code'] == code]['area']
    t = totals.ix[[code]]['outstanding'].values[0]
    i_result = industries.loc[industries['c_name'].isin(i)]['code'].tolist()
    c_result = concepts.loc[concepts['c_name'].isin(c)]['code'].tolist()
    a_result = areas.loc[areas['area'].isin(a)]['code'].tolist()
    #similar_values = totals.loc[0.5*t<totals['outstanding']<2*t].index.tolist()
    #print(len(similar_values))
    results =  i_result+c_result+a_result#+similar_values
    results = sorted(set(results), key=results.index)
    def sx(x):
        if x[0] == '6':
            return x + '.SH'
        elif x[0] == '0' or x[0] == '3':
            return x + '.SZ'
    return list(map(lambda x: sx(x) , results))
