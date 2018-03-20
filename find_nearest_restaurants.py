
# coding: utf-8

# In[31]:


#CrossCompute
user_address = '6530 Kissena Blvd Queens'
search_count = 10
target_folder = '/home/user/Experiments'


# In[22]:


import pandas
import geopy
geocode = geopy.GoogleV3(api_key='AIzaSyBxBSl2ESDVimP0-nW6i5vOccSO38Aw-js', timeout=5).geocode
user_location = geocode(user_address)
target_latlon = user_location.latitude, user_location.longitude


# In[23]:


restaurants = pandas.read_csv('deduplicate_coordinate.csv')


# In[24]:


coordinates = restaurants[['Latitude', 'Longitude']]


# In[25]:


from pysal.cg import RADIUS_EARTH_MILES
from pysal.cg.kdtree import KDTree
source_tree = KDTree(coordinates.values, distance_metric="Arc", radius=RADIUS_EARTH_MILES)
distances, indices = source_tree.query((user_location.latitude, user_location.longitude), k = search_count)
select_restaurants = restaurants.iloc[indices].copy()
select_restaurants['Distance'] = distances


# In[17]:


from os.path import join
result_target_path = join(target_folder, 'search_locations.csv')
select_restaurants.to_csv(result_target_path, index=False)
print('select_restaurants_geotable_path = %s' % result_target_path)

