from geopy.geocoders import Nominatim
import toml
import pandas as pd

with open("nodes.toml", "r") as toml_file:
    cities = toml.load(toml_file)

def populate_latlongs(city_name: str) -> tuple:
    geolocator = Nominatim(user_agent="Pat Pragman")
    location = geolocator.geocode(city_name)
    return location.latitude, location.longitude

def get_latlon(city_name: str):
    return cities[city_name]

if __name__ == "__main__":
    df = pd.read_csv("romania.csv")
    cities = df.columns[1:]
    city_dict = {}
    for city in cities:
        city_dict[city] = populate_latlongs(city)


    with open("nodes.toml", "w") as toml_file:
        toml.dump(city_dict, toml_file)
