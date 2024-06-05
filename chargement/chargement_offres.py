import os
import duckdb

def chargement(chemin_donnees_brutes, chemin_stockage, nom_fichier_stockage, date_creation):

    path = os.path.join(chemin_donnees_brutes, "collecte_offres_francetravail")
    file_path = f"{path}/offres-{date_creation}.json"

    with duckdb.connect(os.path.join(chemin_stockage, nom_fichier_stockage)) as con:

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
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")