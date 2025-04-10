import requests
import ctypes

# Specify country and year
country = "Argentina"
year = "2020"

api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
response = requests.get(api_url)
data = response.json()

# data[1][0]['country']['value'] = "Argentina"

# Search GINI index for the specified country and year
for i_country in data[1]:
    if i_country['country']['value'] == country:
        if i_country['date'] == year:
            # print(i_country)
            gini_val = i_country['value']
            print("Gini actual: ",gini_val)

# Load C library
lib_send_gini = ctypes.CDLL('./lib_send_gini.so')

# Set argument and return types
lib_send_gini._gini.argtypes = (ctypes.c_double,)
lib_send_gini._gini.restype = ctypes.c_double

# Define python function
def send_gini(num):
    return lib_send_gini._gini(num)

print("Gini actualizado: ",send_gini(gini_val))