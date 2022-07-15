import time

import geocoder
import h3
import pandas as pd

df = pd.read_csv(
    "data/unique.tsv", sep="\t", names=["address", "price", "type", "page"]
)


def address_cleaner(adr):
    return adr.strip().replace("1 ", "").replace("2 ", "").replace("3 ", "")


addresses = [address_cleaner(adr) for adr in df["address"]]
districts = [adr.split(",")[1] for adr in addresses]
roads = [adr.split(",")[0] for adr in addresses]

df["address"] = roads
df["district"] = districts

geocoded = {}

# these two services doesn't require an API key,
# but they limit the number of requests, so we
# retry the rejected ones
print(f"we have {len(set(roads))} unique addresses")
print("let's start geocoding")
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
print("geocoding finished")

addr_latlong = {}
for k, v in geocoded.items():
    try:
        if (
            v["features"][0]["properties"]["country"] == "Hungary"
            or v["features"][0]["properties"]["country"] == "Magyarország"
        ):
            lat = v["features"][0]["properties"]["lat"]
            long = v["features"][0]["properties"]["lng"]
            addr_latlong[k] = {"lat": lat, "long": long}
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

print("geohasing latlong")
l5 = []
l6 = []
l7 = []
l8 = []
l9 = []
l10 = []
l11 = []
l12 = []
l13 = []
l14 = []
l15 = []

for _, row in df.iterrows():
    l5.append(h3.geo_to_h3(row["lat"], row["long"], 5))
    l6.append(h3.geo_to_h3(row["lat"], row["long"], 6))
    l7.append(h3.geo_to_h3(row["lat"], row["long"], 7))
    l8.append(h3.geo_to_h3(row["lat"], row["long"], 8))
    l9.append(h3.geo_to_h3(row["lat"], row["long"], 9))
    l10.append(h3.geo_to_h3(row["lat"], row["long"], 10))
    l11.append(h3.geo_to_h3(row["lat"], row["long"], 11))
    l12.append(h3.geo_to_h3(row["lat"], row["long"], 12))
    l13.append(h3.geo_to_h3(row["lat"], row["long"], 13))
    l14.append(h3.geo_to_h3(row["lat"], row["long"], 14))
    l15.append(h3.geo_to_h3(row["lat"], row["long"], 15))

print("geohashing finished")
df["l5"] = l5
df["l6"] = l6
df["l7"] = l7
df["l8"] = l8
df["l9"] = l9
df["l10"] = l10
df["l11"] = l11
df["l12"] = l12
df["l13"] = l13
df["l14"] = l14
df["l15"] = l15

df.to_csv("data/ingatlan_cleaned_geocoded.tsv", index=False, sep="\t")
print("data is ready")
