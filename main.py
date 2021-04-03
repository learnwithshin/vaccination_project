from vaccination_source import (
    get_data_source_from_lws,
    content_to_df,
    get_confirmed_cases_api,
)
from database import get_data_from_db, upload_df_to_db

DB = "vax.db"
MASTER_QRY = """
SELECT
  *
FROM
  vaccination_data AS vd
  JOIN countries AS c ON vd.country = c.country
  LEFT JOIN confirmed_cases AS cc ON vd.country || vd.date = cc.id
"""


def main():
    countries = get_data_source_from_lws(0)
    vaccination_data = get_data_source_from_lws(1)
    country_df = content_to_df(countries)
    vaccination_df = content_to_df(vaccination_data)
    upload_df_to_db(country_df, DB, "countries")
    upload_df_to_db(vaccination_df, DB, "vaccination_data")

    country_list = country_df["country"]

    confirmed_cases_df = get_confirmed_cases_api(country_list)
    upload_df_to_db(confirmed_cases_df, DB, "confirmed_cases")

    print("Done uploading data!")

    master_df = get_data_from_db(DB, MASTER_QRY)
    master_df.to_csv("master.csv")
    print("File saved. All done!")


if __name__ == "__main__":
    main()
