import os

import pandas as pd
import pydeck as pdk

indir = "data/aggregated"

infiles = [f for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f))]

for f in infiles:
    df = pd.read_csv(os.path.join(indir, f), sep="\t")
    layer = pdk.Layer(
        "H3HexagonLayer",
        df,
        get_hexagon=f"{f.split('.')[0]}",
        auto_highlight=True,
        elevation_scale=10,
        pickable=True,
        elevation_range=[min(df["price"]), max(df["price"])],
        extruded=True,
        coverage=0.8,
        opacity=0.01,
        get_fill_color="[0, 255, price]"
    )

    view_state = pdk.ViewState(latitude=47.500000, longitude=19.040236,
                               zoom=10, bearing=0, pitch=35)
    r = pdk.Deck(layers=[layer],
                 initial_view_state=view_state,
                 tooltip={"text": "square meter price: {price}"})
    r.to_html(f"vizs/{f.split('.')[0]}.html")
