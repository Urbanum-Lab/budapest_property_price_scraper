import pandas as pd

df = pd.read_csv("data/ingatlan_cleaned_geocoded.tsv", sep="\t")

df = df[df["lat"] < 47.601216]
df = df[df["lat"] > 47.392134]
df = df[df["long"] > 18.936234]
df = df[df["long"] < 19.250031]
df2publish = df[
    [
        "type",
        "district",
        "price",
        "l5",
        "l6",
        "l7",
        "l8",
        "l9",
        "l10",
        "l11",
        "l12",
        "l13",
        "l14",
        "l15",
    ]
]

areas = ["l5", "l6", "l7", "l8", "l9", "l10", "l11", "l12", "l13", "l14", "l15"]

for hash in areas:
    df2save = df2publish.groupby(hash).mean()
    df2save.reset_index(inplace=True, level=[hash])
    df2save.to_csv(f"data/aggregated/{hash}.tsv", index=False, sep="\t")

