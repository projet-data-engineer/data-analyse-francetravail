import os
import duckdb
from zipfile import ZipFile

def decompactage(yyyy_mm):

    nom_archive=f"{os.getenv('DESTINATION_SIRENE')}/sirene_{yyyy_mm}.zip"

    with ZipFile(nom_archive, 'r') as f:
        f.extractall(path=os.getenv('DESTINATION_SIRENE'))

def chargement(yyyy_mm):

    csv=f"{os.path.join(os.getenv('DESTINATION_SIRENE'),'StockEtablissement_utf8.csv')}"

    with duckdb.connect(os.getenv('DESTINATION_ENTREPOT')) as con:

        con.sql("CREATE SCHEMA IF NOT EXISTS collecte")

        SQL = f"""
            CREATE OR REPLACE TABLE collecte.etablissement AS (
                SELECT
                    '{yyyy_mm}' AS version, e.*
                FROM 
                    '{csv}' AS e
                WHERE
                    e.etatAdministratifEtablissement = 'A'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM collecte.etablissement")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")

    os.remove(csv)