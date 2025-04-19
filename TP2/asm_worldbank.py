import requests
import ctypes
from my_client import MyClient

# Specify country and year
country_searched = "Bolivia"
year_searched = "2018"

api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

# Search GINI index for the specified country and year
def fetch_gini_index(country_searched, year_searched) -> float:
    response = requests.get(api_url)
    data = response.json()
    gini_val = 0
                
    for item in data[1]:
        country = item.get('country', {}).get('value')
        year = item.get('date')
        
        if country == country_searched and year == year_searched:
            gini_val = item.get('value')
        else:
            continue
                
    return gini_val

old_gini = fetch_gini_index(country_searched, year_searched)

# Connect to the 32-bit library using msl-loadlib
c_program = MyClient()

# Print GINI values
print("Gini viejo: ", old_gini)
print("Gini actualizado: ", c_program._gini(old_gini))
