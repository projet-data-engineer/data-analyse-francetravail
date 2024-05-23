import os
import duckdb

DB_PATH = os.getenv('DB_PATH')
DUCKDB_FILE = os.getenv('DUCKDB_FILE')
DATE_CREATION = os.getenv("DATE_CREATION")
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")

path = os.path.join(RAW_DATA_PATH, "collecte-francetravail")
file_path = f"{path}/offres-{DATE_CREATION}.json"

with duckdb.connect(os.path.join(DB_PATH, DUCKDB_FILE)) as con:

    con.sql("CREATE SCHEMA IF NOT EXISTS collecte")

    SQL = f"""
        CREATE OR REPLACE TABLE collecte.raw_offre AS (
            SELECT
                id,
                CAST(dateCreation AS DATE) AS dateCreation,
                lieuTravail.commune,
                lieuTravail.latitude,
                lieuTravail.longitude,
                codeNAF,
                romeCode,
                entreprise.entrepriseAdaptee,
                typeContrat,
                natureContrat,
                experienceExige,
                alternance,
                nombrePostes,
                accessibleTH,
                CAST(qualificationCode AS VARCHAR) AS qualificationCode,
                qualificationLibelle
            FROM 
                '{file_path}'
        )
    """

    con.sql(SQL)
    con.execute("SELECT COUNT(*) FROM collecte.raw_offre")
    
    print(f"\n\n{con.fetchone()[0]} offres chargées !\n\n")