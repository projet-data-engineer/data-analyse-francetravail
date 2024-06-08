from datetime import datetime
import os
import pendulum

from airflow.decorators import dag, task
from chargement import chargement_naf

local_tz = pendulum.timezone("Europe/Paris")

@dag(
    dag_id='pipeline_naf',
    description='Chargement dans entrepôt DuckDB nomenclature NAF (5 niveaux dénormalisés)',
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)
def pipeline_naf():

    @task
    def chargement():
        chargement_naf.chargement()

    chargement()

pipeline_naf()