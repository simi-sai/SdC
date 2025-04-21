import requests
import ctypes

# Specify country and year
country_searched = "Argentina"
year_searched = "2020"

api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

# Search GINI index for the specified country and year
def fetch_gini_index(country_searched, year_searched) -> int:
    response = requests.get(api_url)
    data = response.json()
    gini_val = 0
                
    for item in data[1]:
        country = item.get('country', {}).get('value')
        year = item.get('date')
        
        if country == country_searched and year == year_searched:
            gini_val = item.get('value')
            break
                
    return gini_val

# Load C library
lib_send_gini = ctypes.CDLL('./lib_send_gini.so', mode=ctypes.RTLD_GLOBAL)
    
# Set argument and return types
lib_send_gini._gini.argtypes = (ctypes.c_int,)
lib_send_gini._gini.restype = (ctypes.c_int)

# Define python function
def send_gini(num):
    return lib_send_gini._gini(num)

old_gini = fetch_gini_index(country_searched, year_searched)

print("Gini viejo: ", old_gini)
print("Gini actualizado: ", send_gini(int(old_gini)))