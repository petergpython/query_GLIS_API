import requests
import json
import time
import pandas as pd
import numpy as np

def call_glis_API(instcode):
    """
    function calling GLIS API and return the results as a list
    takes INSTCODE of genebank as argument
    """
    #URL of the GLIS API
    url = "https://glis.fao.org/glisapi/v1/pgrfas?"
    # parameters for my request
    #parameters = {'holdwiews': 'ZMB048' , 'genus'  : 'Coffea','_format': 'json' , '_pretty': False ,  'per-page': 100 }
    parameters = {'holdwiews': instcode ,'_format': 'json' , '_pretty': False ,  'per-page': 100 }
    # make request and get info on number of pages from the header
    r = requests.get(url, params=parameters)
    print(r.url)
    pages = int(r.headers['X-Pagination-Page-Count'])
    print('limit:' , r.headers['X-Rate-Limit-Limit'])
    print('time:' , r.headers['X-Rate-Limit-Reset'])
    print('pages:' , pages)
    # iterate through the pages of the query results
    # and append the results in a list
    results = []
    for i in range(1,pages+1):
        parameters = {'holdwiews': instcode ,  
                    '_format': 'json' , 
                    '_pretty': False ,  
                    'per-page': 100 , 
                    'page': i}
        r = requests.get(url, params=parameters)  
        #for each accession in the json file with the accession information and append to results   
        for i in r.json():
            #results.append((i['info']['doiregistered']))
            results.append(i)
        time.sleep(1)   # wait one second before making another request to not go over the Rate limit
    return results


def make_estimate(results_API_call, year = '2024'):
    """
    take as arguments result from API call (JSON) and a year , and return a dataframe
    with columns with year that DOI was registered,  bollean values for DOI registered and inclusion in MLS for the year selected 
    """
    df = pd.DataFrame()
    r = []
    for i in results_API_call:
        if i['R07'] is None:  #R07 is the filed where MLS status is recorded
            pass
        else:
            r.append((i['R07']['code'],i['info']['doiregistered']) ) #doi registered is the date of registration of the DOI
    try:
        df = pd.DataFrame(r)
        df.columns = ['MLS', 'date_DOI']
        df['DOI_year'] = df.date_DOI.str[:4]
        df['MLS'] = df.MLS.astype(int)
        df['DOI_'+year] = np.where(df.DOI_year == year , True, False)
        df['MLS_'+year] = np.where((df.DOI_year == year) & (df.MLS > 0 ), True, False)
        return df
    finally:
        return df
