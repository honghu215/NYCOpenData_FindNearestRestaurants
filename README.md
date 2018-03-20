
# NYC OpenData tool: Find nearest restaurants with inspection detail
find the nearest restaurants with sanitary inspection grade and details using geocoding service, source from NYC open data

This tool will show the user the nearest a number of restaurants (specified by user input) with inspection details based on user input address and search count.

The dataset the tool is using is [DOHMH New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j) from NYC Open Data.  
The tool is delpoyed on CrossCompute platform. Click [here](https://crosscompute.com/t/YLhMnMnpMLvaCXwa8MNFpr4h6OyKdmWp) to run the program.

### How it works
* Basically, it uses KD-Tree to build a 10-D tree (let's say search count it 10), and then find the shortest distance from the user's position. It calculates the distance in the form of nodes, which in this case is coordinates(latitude and longitude). 

#### Steps:
1. Get the dataset: NYC open data provides API for each dataset. Go to [API docs](https://dev.socrata.com/foundry/data.cityofnewyork.us/9w7m-hzhe) to learn about how to retrieve this dataset via Socrata Open Data API. 
1. The dataset is over 380,000 recordes, including all restaurants in New York. It has no coordinate attribute, but building number, borough, street and zip code. I'm using geoclient API to get coordinates and save it as .csv file locally. Refer to ConvertCoordinate.py
1. FindNearestRestaurants.py will read csv file, which includes coordinates attribute, and then build kd-tree to find shortest distance and ouput the nearest restaurants.

### Bugs
* Takes long time: The dataset is huge, over 380,000 records. Although it can be filtered to 27,000, it takes over half an hour to resolve this number of addresses to coordinates. 

![example](https://34.230.102.202/owncloud/index.php/s/JfuazhKJ2HKEiwz)
