from datetime import datetime
import os
import pendulum

from airflow.decorators import dag, task
from chargement import chargement_naf

local_tz = pendulum.timezone("Europe/Paris")

@dag(
    dag_id='pipeline_nomenclature_naf',
    description='Chargement dans entrepôt DuckDB nomenclature NAF (5 niveaux dénormalisés)',
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_nomenclature_naf():

    @task
    def chargement():

        chargement_naf.chargement(
            chemin_donnees_brutes=os.getenv('CHEMIN_DONNEES_BRUTES'), 
            chemin_fichier_donnees_brutes='nomenclature_naf_csv', 
            chemin_stockage=os.getenv('CHEMIN_STOCKAGE'),
            nom_fichier_stockage=os.getenv('NOM_FICHIER_STOCKAGE')
        )

    chargement()

pipeline_nomenclature_naf()