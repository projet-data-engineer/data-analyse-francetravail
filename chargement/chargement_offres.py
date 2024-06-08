import os
import duckdb

def chargement(date_creation):

    file_path = os.path.join(os.getenv('DESTINATION_OFFRE_EMPLOI'), f'offres-{date_creation}.json')

    with duckdb.connect(os.getenv('DESTINATION_ENTREPOT')) as con:

        con.sql("CREATE SCHEMA IF NOT EXISTS collecte")
        con.sql("CREATE SCHEMA IF NOT EXISTS entrepot")

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
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")