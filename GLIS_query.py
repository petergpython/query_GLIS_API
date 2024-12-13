import requests
import json
import time


#URL of the GLIS API
url = "https://glis.fao.org/glisapi/v1/pgrfas?"

# parameters for my request
parameters = {'holdwiews': 'CRI001' , 'genus'  : 'Coffea','_format': 'json' , '_pretty': False ,  'per-page': 100 }

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
    parameters = {'holdwiews': 'CRI001' , 
                    'genus'  : 'Coffea', 
                    '_format': 'json' , 
                    '_pretty': False ,  
                    'per-page': 100 , 
                    'page': i}
    r = requests.get(url, params=parameters)  
    #for each accession in the json file extract the date of DOI registration and append to results   
    for i in r.json():
        results.append((i['info']['doiregistered']))
    time.sleep(1)   # wait one second before making another request to not go over the Rate limit 