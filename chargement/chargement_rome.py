import os
import duckdb

DB_PATH = os.getenv('DB_PATH')
DUCKDB_FILE = os.getenv('DUCKDB_FILE')
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")

path = os.path.join(RAW_DATA_PATH, "nomenclatures")
file_path = f"{path}/rome.json"

with duckdb.connect(os.path.join(DB_PATH, DUCKDB_FILE)) as con:

    con.sql("CREATE SCHEMA IF NOT EXISTS collecte")

    SQL = f"""
        CREATE OR REPLACE TABLE collecte.rome AS (
            SELECT
                code_1,
                libelle_1,
                code_2,
                libelle_2,
                code_3,
                libelle_3
            FROM 
                '{file_path}'
        )
    """

    con.sql(SQL)

    con.execute("SELECT COUNT(*) FROM collecte.rome")
    print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")