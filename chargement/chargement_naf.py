import os
import duckdb

def chargement():

    with duckdb.connect(os.getenv('DESTINATION_ENTREPOT')) as con:

        # hierarchie
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.naf_hierarchie AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/hierarchie.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.naf_hierarchie")
        print(f"\n\nnaf_hierarchie: chargement de {con.fetchone()[0]} enregistrements !\n\n")

        # Niveau 1
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.naf_niveau_1 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/niveau_1.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.naf_niveau_1")
        print(f"\n\nnaf_niveau_1: chargement de {con.fetchone()[0]} enregistrements!\n\n")

        # Niveau 2
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.naf_niveau_2 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/niveau_2.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.naf_niveau_2")
        print(f"\n\nnaf_niveau_2: chargement de {con.fetchone()[0]} enregistrements!\n\n")

        # Niveau 3
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.naf_niveau_3 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/niveau_3.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.naf_niveau_3")
        print(f"\n\nnaf_niveau_3: chargement de {con.fetchone()[0]} enregistrements!\n\n")

        # Niveau 4
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.naf_niveau_4 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/niveau_4.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.naf_niveau_4")
        print(f"\n\nnaf_niveau_4: chargement de {con.fetchone()[0]} enregistrements!\n\n")

        # Niveau 5
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.naf_niveau_5 AS (
                SELECT
                    *
                FROM 
                    '{os.getenv('DESTINATION_NAF')}/niveau_5.csv'
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.naf_niveau_5")
        print(f"\n\nnaf_niveau_5: chargement de {con.fetchone()[0]} enregistrements!\n\n")