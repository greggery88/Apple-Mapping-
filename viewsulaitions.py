import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import geoplot as gplt
import geopandas as geopd
import geoplot.crs as gcrs


def get_geo_countys():
    cd = geopd.read_file(
        "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson"
    )
    cd = cd[cd["STATE"] == "23"].reset_index()
    cd = cd.drop(
        columns=["STATE", "index", "id", "GEO_ID", "CENSUSAREA", "COUNTY", "LSAD"]
    )
    cd = cd.rename(columns={"NAME": "county"})
    cd.to_csv("CountyEdges.csv", index=False)


def make_the_plot():
    df_ce = geopd.read_file(
        "/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/CountyEdges.csv"
    )
    gf_county_edges = geopd.GeoDataFrame(
        df_ce, geometry=geopd.GeoSeries.from_wkt(df_ce["geometry"])
    )

    county_points = geopd.read_file(
        "/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/CountyPoints.csv"
    )

    fig = plt.figure(figsize=(6, 6))
    ax = fig.subplots()
    gplt.polyplot(gf_county_edges, projection=gcrs.AlbersEqualArea(), ax=ax)

    plt.show()


if __name__ == "__main__":
    make_the_plot()
