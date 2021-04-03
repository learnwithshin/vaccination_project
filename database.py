from contextlib import closing
import sqlite3


def upload_df_to_db(df, db_name, table):
    with closing(sqlite3.connect(db_name)) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"Updated {table}!")


def get_data_from_db(db_name, qry):
    with closing(sqlite3.connect(db_name)) as conn:
        return pd.read_sql_query(qry, conn)