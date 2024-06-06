import os
import duckdb


def chargement(chemin_donnees_brutes, chemin_fichier_donnees_brutes, chemin_stockage, nom_fichier_stockage):

    chemin_fichier_brut = os.path.join(chemin_donnees_brutes,chemin_fichier_donnees_brutes)

    with duckdb.connect(os.path.join(chemin_stockage, nom_fichier_stockage)) as con:

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
                    '{chemin_fichier_brut}/nomenclature_rome.json'
            )
        """

        con.sql(SQL)

        con.execute("SELECT COUNT(*) FROM collecte.rome")
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")