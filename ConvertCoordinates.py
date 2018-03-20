
# coding: utf-8

# In[ ]:


#CrossCompute
user_address = ''
search_count = 10
target_folder = '/home/user/Experiments'


# In[ ]:


get_ipython().system('pip install sodapy')


# In[ ]:


import pandas
from pandas import Series
from sodapy import Socrata


# In[ ]:


client = Socrata('data.cityofnewyork.us',
                 'KYk3Ul7BNvcahTIWDyqVJdQwu',
                 username="huhong215@gmail.com",
                 password="Hh930215")
results = client.get("9w7m-hzhe", limit=390000)
restaurants = pandas.DataFrame.from_records(results)


# In[ ]:


len(restaurants)


# In[ ]:


restaurants_sort = restaurants.sort_values(by='inspection_date')


# In[ ]:


len(restaurants_sort)


# In[ ]:


from os.path import join
sort_target_path = join(target_folder, 'sort.csv')
restaurants_sort.to_csv(sort_target_path, index=False)


# In[ ]:


restaurants_deduplicate = restaurants.drop_duplicates(subset=['building', 'street', 'boro', 'dba'], keep='last')


# In[ ]:



deduplicate_target_path = join(target_folder, 'deduplicate.csv')
restaurants_deduplicate.to_csv(deduplicate_target_path, index=False)


# In[ ]:


restaurants_deduplicate


# In[ ]:


geoclient_id = 'a3c926c5'
geoclient_key = 'c191a8de8cc1e9d84f888a82e69fc3b7'
url = 'https://api.cityofnewyork.us/geoclient/v1/address.json'
import requests
import geopy
geocode = geopy.GoogleV3(api_key='AIzaSyBxBSl2ESDVimP0-nW6i5vOccSO38Aw-js', timeout=5).geocode
user_location = geocode(user_address)


# In[ ]:



errorCount = 0
geopyCount = 0
def convert(row):
    building = row['building']
    street = row['street']
    boro = row['boro']
    zipcode = row['zipcode']
    response = requests.get(url, dict(houseNumber=building, street=street, borough=boro, zipcode=zipcode,
                                      app_id=geoclient_id, app_key=geoclient_key))
    global geopyCount
    global errorCount
    try:
        response_json = response.json()
        d = response_json['address']
        return Series([d['latitude'], d['longitude']])
    except:
        try:
            
            current_location = geocode(str(building) + ' ' + street + ' ' + boro + ' ' + str(zipcode))
            geopyCount += 1
            print(geopyCount, 'Google geocode:', building, street, boro, row['dba'])
            return Series([current_location.latitude, current_location.longitude])
        except:
            errorCount += 1
            print(errorCount, building, street, boro, row['dba'], 'no coordinates!!!!!!')
            return Series([0.0, 0.0])
        


# In[ ]:


import time
timeBeforeConv = time.asctime(time.localtime(time.time()))
print('Before converting, time is:', timeBeforeConv)
coordinate_table = restaurants_deduplicate.apply(convert, axis=1)
timeAfterConv = time.asctime(time.localtime(time.time()))
print('After converting, time is:', timeAfterConv)
coordinate_table.columns = ['Latitude', 'Longitude']
#time consuming: 38 min


# In[ ]:


len(restaurants_deduplicate), len(coordinate_table)


# In[ ]:


restaurants_coordinate = restaurants_deduplicate.join(coordinate_table)
coordinate_target_path = join(target_folder, 'deduplicate_coordinate.csv')
restaurants_coordinate.to_csv(coordinate_target_path, index=False)


# In[ ]:


len(restaurants_coordinate)

