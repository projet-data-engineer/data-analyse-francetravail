import os
import duckdb

DB_FILE = os.getenv('DB_FILE')
JSON_FILE = os.getenv('JSON_FILE')

with duckdb.connect(DB_FILE) as con:

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
                '{JSON_FILE}'
        )
    """

    con.sql(SQL)
    con.execute("SELECT COUNT(*) FROM collecte.raw_offre")
    
    print(f"\n\n{con.fetchone()[0]} offres chargées !\n\n")