from datetime import datetime
import os

from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

@dag(
    dag_id="france-travail-pipeline",
    #schedule_interval='*/2 * * * *',
    schedule=None,
    start_date=datetime(2023, 12, 1),
    catchup=False
)
def francetravail():

    extraction_api_francetravail = DockerOperator(

        task_id='extraction_api_francetravail',
        image='extraction_francetravail:latest',
        container_name='extraction_api_francetravail',
        api_version='auto',
        auto_remove=True,
        docker_url="TCP://docker-proxy:2375",
        mount_tmp_dir=False,
        network_mode="data-emploi",
        environment={
            'FRANCETRAVAIL_HOST': os.getenv('FRANCETRAVAIL_HOST'),
            'FRANCETRAVAIL_ID_CLIENT': os.getenv('FRANCETRAVAIL_ID_CLIENT'),
            'FRANCETRAVAIL_CLE_SECRETE': os.getenv('FRANCETRAVAIL_CLE_SECRETE'),
            'DATE_CREATION': '2024-05-16' 
        },
        mounts=[Mount(target='/raw-data', source='raw-data', type='volume')]
    )

    chargement_duckdb_francetravail = DockerOperator(

        task_id='chargement_duckdb_francetravail',
        image='chargement_francetravail:latest',
        container_name='chargement_duckdb_francetravail',
        api_version='auto',
        auto_remove=True,
        docker_url="TCP://docker-proxy:2375",
        mount_tmp_dir=False,
        network_mode="data-emploi",
        environment={
            'JSON_FILE': '/raw-data/offres-francetravail.io-2024-05-16.json',
            'DB_FILE': '/db/warehouse.db'
        },
        mounts=[
            Mount(target='/raw-data', source='raw-data', type='volume'),
            Mount(target='/db', source='db', type='volume')
        ]
    )

    extraction_api_francetravail >> chargement_duckdb_francetravail

francetravail()