import altair as alt
import pandas as pd
import requests


def download(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


def read_raw_dataframe(filename):
    sheet_names = {"ИТБ": "ITMB", "ФЭТ": "FET", "ФМ": "FM"}

    dfs = []
    for sheet_name_ru in sheet_names.keys():
        df = pd.read_excel(filename, header=1, sheet_name=sheet_name_ru)
        df["program"] = sheet_names[sheet_name_ru]
        dfs.append(df)

    # Concatenate the dataframes from all sheets
    df = pd.concat(dfs, ignore_index=True)

    # Drop the columns which have all nan values
    return df.dropna(axis="columns", how="all")


def clean_columns(df):
    column_names = {
        # Omit the names
        # 'ФИО': 'name',
        "program": "program",
        "Бюджет/договор": "is_budget",
        # "сумма баллов": "ege_total",
        "Мат.": "ege_math",
        "Русс.": "ege_russian",
        "ИКТ": "ege_it",
        "Ин.яз": "ege_foreign",

    }
    return df[column_names.keys()].rename(columns=column_names)


def budget_column(df):
    # Replace 'договор' with True, all other with False
    ix = df.is_budget == "Бюджет"
    df.loc[ix, "is_budget"] = True
    df.loc[~ix, "is_budget"] = False
    return df

def make_url(spreadsheet_id):
   return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"


if __name__ == "__main__":
    # %%

    spreadsheet_id = "1pUDOO5rROKI20sP5p5_2gVCMvsOoBoFzYUNtz2fZYqA"

    url = make_url("1pUDOO5rROKI20sP5p5_2gVCMvsOoBoFzYUNtz2fZYqA")
    print(url)
    xl_filename = "ege_scores.xlsx"
    csv_filename = "ege_scores.csv"
    print(xl_filename)

    import os
    if not os.path.exists(xl_filename):
        download(url, xl_filename)

    df = read_raw_dataframe(xl_filename)
    df = clean_columns(df)
    df = budget_column(df)
    df.to_csv("ege_scores.csv", index=False)
    print(csv_filename)

    assert len(df[df.is_budget]) == 5
    assert len(df) == 48
