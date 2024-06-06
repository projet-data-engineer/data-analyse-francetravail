import os
import duckdb

def chargement(chemin_donnees_brutes, chemin_fichier_donnees_brutes, chemin_stockage, nom_fichier_stockage):

    chemin_fichier_brut = os.path.join(chemin_donnees_brutes, chemin_fichier_donnees_brutes)

    with duckdb.connect(os.path.join(chemin_stockage, nom_fichier_stockage)) as con:

        SQL = f"""
            CREATE OR REPLACE TABLE collecte.naf AS
                WITH
                    hierarchie AS (
                        SELECT
                            niv5,
                            niv4,
                            niv3,
                            niv2,
                            niv1
                        FROM
                            '{chemin_fichier_brut}/hierarchie.csv'
                    ),
                    niveau_1 AS (
                        SELECT
                            code,
                            libelle
                        FROM
                            '{chemin_fichier_brut}/niveau_1.csv'
                    ),
                    niveau_2 AS (
                        SELECT
                            code,
                            libelle
                        FROM
                            '{chemin_fichier_brut}/niveau_2.csv'
                    ),
                    niveau_3 AS (
                        SELECT
                            code,
                            libelle
                        FROM
                            '{chemin_fichier_brut}/niveau_3.csv'
                    ),
                    niveau_4 AS (
                        SELECT
                            code,
                            libelle
                        FROM
                            '{chemin_fichier_brut}/niveau_4.csv'
                    ),
                    niveau_5 AS (
                        SELECT
                            code,
                            libelle
                        FROM
                            '{chemin_fichier_brut}/niveau_5.csv'
                    )

                    SELECT
                        niveau_1.code AS code_1,
                        niveau_1.libelle AS libelle_1,
                        niveau_2.code AS code_2,
                        niveau_2.libelle AS libelle_2,
                        niveau_3.code AS code_3,
                        niveau_3.libelle AS libelle_3,
                        niveau_4.code AS code_4,
                        niveau_4.libelle AS libelle_4,
                        niveau_5.code AS code_5,
                        niveau_5.libelle AS libelle_5
                    FROM
                        hierarchie
                    JOIN
                        niveau_1 ON hierarchie.niv1 = niveau_1.code
                    JOIN
                        niveau_2 ON hierarchie.niv2 = niveau_2.code
                    JOIN
                        niveau_3 ON hierarchie.niv3 = niveau_3.code
                    JOIN
                        niveau_4 ON hierarchie.niv4 = niveau_4.code
                    JOIN
                        niveau_5 ON hierarchie.niv5 = niveau_5.code
        """

        con.sql(SQL)
        con.execute("SELECT COUNT(*) FROM collecte.naf")
        
        print(f"\n\n{con.fetchone()[0]} enregistrements chargés !\n\n")