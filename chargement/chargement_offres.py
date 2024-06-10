import os
import duckdb

def chargement(date_creation):

    file_path = os.path.join(os.getenv('DESTINATION_OFFRE_EMPLOI'), f'offres-{date_creation}.json')

    with duckdb.connect(os.getenv('DESTINATION_ENTREPOT')) as con:

        con.sql("CREATE SCHEMA IF NOT EXISTS collecte")

        SQL = f"""
            CREATE OR REPLACE TABLE collecte.offre_emploi AS (
                SELECT
                    *
                FROM 
                    '{file_path}'
            )
        """
        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM collecte.offre_emploi")    
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")