import numpy as np
import pandas as pd


def para_data():
    # variables
    row = []


def data(file):
    # makes a dictionary to hold all the data.
    am_data = {}
    rows = []

    # loops through the files
    files = [f"Maine Fairs/Copy of {file}.xlsx"]  # makes an array of the files.
    for f in files:  # this is the loop for the files.

        # find the sheet_names of each file to run through.
        excel = pd.ExcelFile(f"./{f}")  # turn the file into a data frame.
        fairs = excel.sheet_names  # find the sheet names and labels them fairs.
        fairs.remove("Varieties List")  # removes the List of all apples.

        for fa in fairs:  # loops through each fair/sheet.

            fair_dict = {}  # make a dictionary for fairs.

            df = pd.read_excel(
                f"./{f}", sheet_name=fa
            )  # get the data from the sheet into a data frame.

            # makes the years array.
            years = []

            for c in df.columns.values:
                if str(
                    c
                ).isdigit():  # loop over the columns to find the one with years.
                    years.append(c)

            for y in years:  # loop over the year columns to find the apples present

                apples = []  # makes an array for apple present in that years winners
                for i in range(df.shape[0]):
                    if not np.isnan(df[y].iloc[i]):
                        apple = df["Variety"].iloc[i]
                        apples.append(df["Variety"].iloc[i])

                        # year and an apple
                        rows.append(dict(year=y, apple=apple, fair=fa, county=file))

                fair_dict[y] = apples

            am_data[fa] = fair_dict

        return pd.DataFrame.from_records(rows)
        # return am_data


def main():
    df = data("Maine Androscoggin County Fairs")

    print(data("Maine Androscoggin County Fairs"))

    import seaborn as sns
    import matplotlib.pyplot as plt

    a = df.groupby(["county", "year"], as_index=False).count()
    a.reset_index()
    print(a)

    # sns.relplot(
    #     a,
    #     x="year",
    #     y="apple",
    #     hue="county",
    #     kind="line",
    # )

    sns.histplot(
        df[df["fair"] == "Poland"].reset_index(),
        x="year",
        hue="fair",
    )
    plt.show()


if __name__ == "__main__":
    main()
