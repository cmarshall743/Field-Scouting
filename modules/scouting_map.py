from utils import database
import plotly.graph_objects as go
import pandas as pd

cursor = database.cnxn.cursor()

query = "SELECT * FROM [scouting_data]"
df = pd.read_sql(query, database.cnxn)

fig = go.Figure(go.Scattermapbox(
    lat=df.Latitude,
    lon=df.Longitude,
    mode="markers",
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text="Issue: " + df.Issue_Code + "\n Description: " + df.Description,

),
)
fig.update_layout(mapbox_style="satellite-streets")
fig.update_layout(
    autosize=True,
    hovermode="closest",
    mapbox=dict(
        accesstoken="pk.eyJ1IjoiY2hyaXM3NDMiLCJhIjoiY2tqMzg3bHhtMTg2MDJzbzM3cThyNDNudyJ9.aHd21gP1qN-INQcdC75OwQ",
        bearing=0,
        center=dict(
            lat=36.7336,
            lon=-119.4964,
        ),
        pitch=0,
        zoom=10,
    ),
)

layout = fig

