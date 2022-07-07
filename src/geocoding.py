import time

import geocoder
import pandas as pd

df2 = pd.read_csv("data/unique.tsv",
                 sep="\t",
                 names=["address", "price", "type", "page"])


def address_cleaner(adr):
    return adr.strip().replace("1 ", "").replace("2 ", "").replace("3 ", "")


addresses = [address_cleaner(adr) for adr in df["address"]]
districts = [adr.split(",")[1] for adr in addresses]
roads = [adr.split(",")[0] for adr in addresses]

df["address"] = roads
df["district"] = districts

geocoded = {}

# these two services doesn't require a API key,
# but they limit the number of requests so we
# retry the rejected ones
for adr in set(roads):
    adr = "Budapest " + adr + " Hungary"
    try:
        g = geocoder.geocodefarm(adr)
        geocoded[adr] = g.geojson
        time.sleep(0.3)
    except Exception as e:
        print(e)
        continue

for k, v in geocoded.items():
    if not v["features"]:
        try:
            g = geocoder.osm(k)
            geocoded[k] = g.geojson
            time.sleep(0.3)
        except Exception as e:
            print(e)
            continue

addr_latlong = {}
for k,v in geocoded.items():
    try:
        if v["features"][0]["properties"]["country"] == "Hungary" or v["features"][0]["properties"]["country"] == "Magyarország":
            lat = v["features"][0]["properties"]["lat"]
            long = v["features"][0]["properties"]["lng"]
            addr_latlong[k] = {"lat": lat,
                               "long": long}
    except Exception as e:
        print(k, v)
        continue


def get_location(addr):
    lat_long = addr_latlong.get(addr, "None")
    if lat_long != "None":
        return lat_long["lat"], lat_long["long"]
    else:
        return pd.NA, pd.NA


df["lat"] = [get_location("Budapest " + addr + " Hungary")[0] for addr in roads]
df["long"] = [get_location("Budapest " + addr + " Hungary")[1] for addr in roads]


def clean_price(price):
    return int("".join(price.replace("Ft/m2", "").strip().split()))


df["price"] = [clean_price(pr) for pr in df["price"]]
df.dropna(inplace=True)

df.to_csv("data/ingatlan_cleaned_geocoded.tsv",
          index=False,
          sep="\t")
