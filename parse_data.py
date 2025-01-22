import numpy as np
import pandas as pd
import os
import geoplot as gplt
import geopandas as geopd
import geoplot.crs as gcrs


def get_date_from_excel():

    rows = []

    file_list = os.listdir(
        "/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/Maine Fairs"
    )
    t = 0
    for county in file_list:
        t += 1
        print(f"{t}/{len(file_list)}")

        sheet_names = pd.ExcelFile(f"Maine Fairs/{county}").sheet_names
        sheet_names.remove("Varieties List")

        county_name = county.replace("Copy of Maine, ", "").replace(
            " County Fairs.xlsx", ""
        )

        for fair in sheet_names:
            df = pd.read_excel(f"Maine Fairs/{county}", sheet_name=fair)

            years = []
            for c in df.columns.values:
                if str(c).isdigit():
                    years.append(c)

            for year in years:
                for i in range(df.shape[0]):
                    if not pd.isnull(df[year].iloc[i]):
                        apple = df["Variety"].iloc[i]

                        rows.append(
                            dict(
                                county=county_name,
                                fair=fair,
                                year=year,
                                apple_type=apple,
                            )
                        )

    data = pd.DataFrame.from_records(rows)
    return data


def add_apple_totals(df):
    a = df.groupby(["county", "fair", "year"]).count().reset_index()
    b = a.rename(columns={"apple_type": "apple_totals"})
    c = b.drop(columns="county")
    return pd.merge(df, c, on=["fair", "fair", "year", "year"], how="left")


def save_data(data):
    data.to_csv("reformated_data.csv", index=False)
    data.to_excel("reformated_exel.xlsx")


def geo_add():
    df = pd.read_csv(
        "/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/reformated_data.csv"
    )
    cd = geopd.read_file(
        "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson"
    )
    df.groupby()
    mc = cd[cd["STATE"] == "23"].reset_index()
    mc = mc.drop(
        columns=["STATE", "index", "id", "GEO_ID", "CENSUSAREA", "COUNTY", "LSAD"]
    )
    mc = mc.rename(columns={"NAME": "county"})
    print(mc)

    g = mc.merge(df, on=["county", "county"], how="right")
    print(g)


def main():

    geo_add()
    print(4)
    # df = get_date_from_excel()
    # df = add_apple_totals(df)
    # save_data(df)
    # print("done")


if __name__ == "__main__":
    main()
