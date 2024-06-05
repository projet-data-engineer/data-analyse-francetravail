from datetime import datetime, timedelta
import os
import pendulum

from airflow.decorators import dag, task
from collecte import collecte_rome
from chargement import chargement_rome


local_tz = pendulum.timezone("Europe/Paris")

"""
Collecte et chargement nomenclature 3 niveaux
"""

NOM_FICHIER_DONNEES_BRUTES='nomenclature_rome.json'

@dag(
    dag_id='pipeline_nomenclature_rome',
    description='Collecte 3 niveaux nomenclature ROME depuis api francetravail.io',
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_nomenclature_rome():

    @task
    def collecte():

        collecte_rome.collecte(
            chemin_donnees_brutes=os.getenv('CHEMIN_DONNEES_BRUTES'), 
            nom_fichier_donnees_brutes=NOM_FICHIER_DONNEES_BRUTES
        )

    @task
    def chargement():

        chargement_rome.chargement(
            chemin_donnees_brutes=os.getenv('CHEMIN_DONNEES_BRUTES'), 
            nom_fichier_donnees_brutes=NOM_FICHIER_DONNEES_BRUTES, 
            chemin_stockage=os.getenv('CHEMIN_STOCKAGE'),
            nom_fichier_stockage=os.getenv('NOM_FICHIER_STOCKAGE')
        )

    collecte() >> chargement()

pipeline_nomenclature_rome()