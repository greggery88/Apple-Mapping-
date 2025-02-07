import numpy as np
import pandas as pd
import seaborn as sns
import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
from shapely import wkt


def main():
    df = pd.read_csv("reformated_data.csv", index_col=False)
    af = pd.read_csv("CountyPoints.csv", index_col=False)
    cf = pd.read_csv("CountyEdges.csv", index_col=False)
    cf["geometry"] = gpd.GeoSeries.from_wkt(cf["geometry"])
    cf = gpd.GeoDataFrame(cf, geometry="geometry")
    nf = df.merge(af, on="county", how="left")
    nf["geometry"] = gpd.GeoSeries.from_wkt(nf["geometry"])
    nf = gpd.GeoDataFrame(nf, geometry="geometry")

    ax = gplt.polyplot(
        cf, zorder=-1, linewidth=1, projection=gcrs.AlbersEqualArea(), figsize=(12, 6)
    )
    # blue with some transparency

    gplt.pointplot(nf, ax=ax)  # red with transparency

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
