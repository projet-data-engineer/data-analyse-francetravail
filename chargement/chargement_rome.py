import os
import duckdb


def chargement():

    

    with duckdb.connect(os.getenv('DESTINATION_ENTREPOT')) as con:

        con.sql("CREATE SCHEMA IF NOT EXISTS collecte")

        file_path = os.path.join(os.getenv('DESTINATION_ROME'), 'rome_domaine.json')

        SQL = f"""
            CREATE OR REPLACE TABLE collecte.rome_domaine AS (
                SELECT
                    code,
                    libelle
                FROM 
                    '{file_path}'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM collecte.rome_domaine")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")


        file_path = os.path.join(os.getenv('DESTINATION_ROME'), 'rome_famille.json')

        SQL = f"""
            CREATE OR REPLACE TABLE collecte.rome_famille AS (
                SELECT
                    code,
                    libelle
                FROM 
                    '{file_path}'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM collecte.rome_famille")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")


        file_path = os.path.join(os.getenv('DESTINATION_ROME'), 'rome_metier.json')

        SQL = f"""
            CREATE OR REPLACE TABLE collecte.rome_metier AS (
                SELECT
                    code,
                    libelle
                FROM 
                    '{file_path}'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM collecte.rome_metier")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")