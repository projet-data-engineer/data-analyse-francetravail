import os
import duckdb
import shutil

def chargement(version):

    shp_region=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'REGION.shp')}"
    shp_departement=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'DEPARTEMENT.shp')}"
    shp_commune=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'COMMUNE.shp')}"
    shp_arrondissement_municipal=f"{os.path.join(os.getenv('DESTINATION_COG_CARTO'),version,'ARRONDISSEMENT_MUNICIPAL.shp')}"

    with duckdb.connect(os.getenv('DESTINATION_ENTREPOT')) as con:

        con.sql("CREATE SCHEMA IF NOT EXISTS collecte")

        con.install_extension("spatial")
        con.load_extension("spatial")

        # Chargement fichier shapefile REGION.shp dans table collecte.cog_carto_region
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.cog_carto_region AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_reg AS code,
                    shp.nom,
                    shp.geom
                FROM 
                    '{shp_region}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.cog_carto_region")
        print(f"\n\nChargement de {con.fetchone()[0]} regions !\n\n")

        # Chargement fichier shapefile DEPARTEMENT.shp dans table collecte.cog_carto_departement
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.cog_carto_departement AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_dep AS code,
                    shp.insee_reg AS code_region,
                    shp.nom,
                    shp.geom
                FROM 
                    '{shp_departement}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.cog_carto_departement")
        print(f"\n\nChargement de {con.fetchone()[0]} départements !\n\n")

        # Chargement fichier shapefile COMMUNE.shp dans table collecte.cog_carto_commune
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.cog_carto_commune AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_com AS code,
                    shp.insee_reg AS code_region,
                    shp.insee_dep AS code_departement,
                    shp.nom,
                    shp.statut,
                    shp.population,                    
                    shp.geom
                FROM 
                    '{shp_commune}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.cog_carto_commune")
        print(f"\n\nChargement de {con.fetchone()[0]} communes !\n\n")

        # Chargement fichier shapefile ARRONDISSEMENT_MUNICIPAL.shp dans table collecte.cog_carto_arrondissement_municipal
        con.sql( f"""
                
            CREATE OR REPLACE TABLE collecte.cog_carto_arrondissement_municipal AS (
                SELECT
                    '{version}' AS version,
                    shp.insee_arm AS code,
                    shp.insee_com AS code_commune,                    
                    shp.nom,
                    shp.population,
                    shp.geom
                FROM 
                    '{shp_arrondissement_municipal}' AS shp
            )

        """
        )
        con.execute("SELECT COUNT(*) FROM collecte.cog_carto_arrondissement_municipal")
        print(f"\n\nChargement de {con.fetchone()[0]} communes !\n\n")