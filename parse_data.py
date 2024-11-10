import numpy as np
import pandas as pd
import os


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

        county_name = county.replace("Copy of Maine, ", "").replace("Fairs.xlsx", "")

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


def save_data(data):
    data.to_csv("reformated_data.csv")
    data.to_excel("reformated_exel.xlsx")


def main():
    df = get_date_from_excel()
    save_data(df)
    print("done")


if __name__ == "__main__":
    main()
