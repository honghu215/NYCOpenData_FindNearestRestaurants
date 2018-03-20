# before running the code, be sure to install via pip: sodapy, pandas
# coding: utf-8

#CrossCompute
user_address = 'INPUT ADDRESS'
search_count = 10
target_folder = 'YOUR WORKING FOLDER'

import pandas
from pandas import Series
from sodapy import Socrata

client = Socrata('data.cityofnewyork.us',
                 'KYk3Ul7BNvcahTIWDyqVJdQwu',
                 username="huhong215@gmail.com",
                 password="Hh930215")
results = client.get("9w7m-hzhe", limit=390000)
restaurants = pandas.DataFrame.from_records(results)


restaurants_sort = restaurants.sort_values(by='inspection_date')

from os.path import join
sort_target_path = join(target_folder, 'sort.csv')
restaurants_sort.to_csv(sort_target_path, index=False)


restaurants_deduplicate = restaurants.drop_duplicates(subset=['building', 'street', 'boro', 'dba'], keep='last')


deduplicate_target_path = join(target_folder, 'deduplicate.csv')
restaurants_deduplicate.to_csv(deduplicate_target_path, index=False)


geoclient_id = 'a3c926c5'
geoclient_key = 'c191a8de8cc1e9d84f888a82e69fc3b7'
url = 'https://api.cityofnewyork.us/geoclient/v1/address.json'
import requests
import geopy
geocode = geopy.GoogleV3(api_key='AIzaSyBxBSl2ESDVimP0-nW6i5vOccSO38Aw-js', timeout=5).geocode
user_location = geocode(user_address)


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


coordinate_table = restaurants_deduplicate.apply(convert, axis=1)
coordinate_table.columns = ['Latitude', 'Longitude']

restaurants_coordinate = restaurants_deduplicate.join(coordinate_table)
coordinate_target_path = join(target_folder, 'deduplicate_coordinate.csv')
restaurants_coordinate.to_csv(coordinate_target_path, index=False)

