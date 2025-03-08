import numpy as np
import pandas as pd
import os
import geoplot as gplt
import geopandas as geopd
import geoplot.crs as gcrs
import time

from pandas.conftest import datetime64_dtype

from clean_up_funcs import *


def cleanup_str(string: str):
    return (
        string.lower()
        .strip()
        .replace("?", "")
        .replace("()", "")
        .replace("  ", " ")
        .replace("(pears)", "(pear)")
    )


def get_date_from_county_fairs():
    time_total_start = time.time()
    rows = []

    file_list = os.listdir(
        "/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/Maine Fairs"
    )
    t = 0
    for county in file_list:
        time_start = time.time()
        t += 1

        sheet_names = pd.ExcelFile(f"Maine Fairs/{county}").sheet_names
        sheet_names.remove("Varieties List")

        county_name = county.replace("Copy of Maine, ", "").replace(
            " County Fairs.xlsx", ""
        )

        print(f"{t}/{len(file_list)}, {county_name}")

        for fair in sheet_names:
            df = pd.read_excel(
                f"Maine Fairs/{county}", sheet_name=fair, keep_default_na=False
            )

            years = []
            for c in df.columns.values:
                if str(c).isdigit():
                    years.append(c)
            try:
                for year in years:
                    for i in range(df.shape[0]):
                        if not pd.isnull(df[year].iloc[i]):
                            if df[year].iloc[i] != "":

                                given_id: str = df["Variety"].iloc[i]
                                alt_id: str = df["Alt. Name Given"].iloc[i]
                                presumed_id: str = df["Presumed ID"].iloc[i]

                                uncertain = "?" in presumed_id

                                is_apple = True

                                given_id_clean = cleanup_str(given_id)

                                # given_id = given_id
                                if "(pear)" in given_id_clean:
                                    is_apple = False
                                    given_id_clean = given_id_clean.replace(
                                        "(pear)", ""
                                    ).strip()

                                presumed_id_clean = cleanup_str(presumed_id)
                                if "(pear)" in presumed_id_clean:
                                    presumed_id_clean = presumed_id_clean.replace(
                                        "(pear)", ""
                                    ).strip()
                                    is_apple = False

                                alt_id_clean = cleanup_str(alt_id)

                                rows.append(
                                    dict(
                                        County=cleanup_str(county),
                                        Fair=cleanup_str(fair),
                                        Year=float_to_int(year),
                                        IsApple=is_apple,
                                        Given_ID=given_id,
                                        Given_ID_Clean=given_id_clean,
                                        Alt_ID=alt_id,
                                        Alt_ID_Clean=alt_id_clean,
                                        Presumed_ID=presumed_id,
                                        Presumed_ID_Clean=presumed_id_clean,
                                        Uncertain=uncertain,
                                    )
                                )
            except Exception as e:
                g = list(df.columns)
                if g[2] != "Presumed ID":
                    print(
                        f"ERROR: Presumed ID is wrong it is ({g[2]}), the error is in {county} {fair}"
                    )
                if g[1] != "Alt. Name Given":
                    print(
                        f"ERROR: Alt. Name Given is wrong it is ({g[1]}), the error is in {county} {fair}"
                    )
                print(e)
                print("ERROR: unknown")

        print(f" time: {time.time() - time_start}s")
    print(f" time total: {time.time() - time_total_start}s")
    data = pd.DataFrame.from_records(rows)
    print("done reading files.")
    return data


def get_data_from_source():
    rows = []

    file_list = os.listdir(
        "/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/fair sources"
    )
    for county in file_list:
        sheet_names = pd.ExcelFile(
            f"/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/fair sources/{county}"
        ).sheet_names

        county_name = county.replace("Copy of Maine, ", "").replace(
            " County Sources.xlsx", ""
        )
        for fair in sheet_names:
            sd = pd.read_excel(
                f"/Users/jwilliamson/git/plasma_particle_simulator/Apple-mapping/fair sources/{county}",
                sheet_name=fair,
                keep_default_na=False,
            )

            s = sd.shape[0]
            try:
                for i in range(sd.shape[0]):
                    year: int = sd["Year"].iloc[i]
                    event: str = sd["Event"].iloc[i]
                    location: str = sd["Location"].iloc[i]
                    # source_date = sd["Source Date"].iloc[i]
                    source: str = sd["Source"].iloc[i]
                    page: int = sd["Page"].iloc[i]
                    notes: str = sd["Notes"].iloc[i]

                    if isinstance(year, str):
                        year = np.nan

                    rows.append(
                        dict(
                            county=cleanup_str(county_name),
                            fair=cleanup_str(fair),
                            year=int(year),
                            event=cleanup_str(event),
                            location=cleanup_str(location),
                            source=cleanup_str(source),
                            page=int(page),
                            notes=cleanup_str(notes),
                        )
                    )
            except Exception as e:
                print(county_name, fair)

                print(f"ERROR: {e}")

                print(f"columns: {list(sd.columns)}")

    reformated_data = pd.DataFrame.from_records(rows)
    reformated_data.to_csv("csv/reformated_sources.csv", index=False)
    print("data")


def add_apple_totals(df):
    a = df.groupby(["county", "fair", "year"])
    a["given_var"].count().reset_index()
    b = a.rename(columns={"apple_type": "apple_totals"})
    c = b.drop(columns="county")
    return pd.merge(
        df,
        c,
        on=["fair", "year", "given_variety", "alt_variety", "presumed_variety"],
        how="left",
    )


def save_data(data):
    data.to_csv("csv/reformated_data.csv", index=False)
    print("done writing files")


def main():
    df = get_date_from_county_fairs()
    save_data(df)
    print("all done")


if __name__ == "__main__":
    remove_errors()
    main()
