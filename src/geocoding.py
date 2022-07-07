import geocoder
import pandas as pd

df = pd.read_csv("data/unique.tsv",
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

for adr in set(roads):
    adr = "Budapest " + adr + " Hungary"
    try:
        g = geocoder.geocodefarm(adr)
        geocoded[adr] = g.geojson
    except Exception as e:
        print(e)
        continue

#TODO: 1) lat & long columns 2) clean price