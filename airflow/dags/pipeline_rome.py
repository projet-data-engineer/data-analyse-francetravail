from datetime import datetime, timedelta
import os
import pendulum

from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


local_tz = pendulum.timezone("Europe/Paris")

"""
Tous les jours à 01h00, requêtage api des offres créées J-1, puis chargement
"""

@dag(
    dag_id="pipeline_rome",
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    schedule=None,
    catchup=False
)
def pipeline_offres_date():

    collecte_rome = DockerOperator(

        task_id='collecte_rome',
        image='collecte:latest',
        container_name='collecte_rome',
        api_version='auto',
        auto_remove=True,
        docker_url="TCP://docker-proxy:2375",
        mount_tmp_dir=False,
        command="python ./collecte_rome.py",
        environment={
            'FRANCETRAVAIL_HOST': os.getenv('FRANCETRAVAIL_HOST'),
            'FRANCETRAVAIL_ID_CLIENT': os.getenv('FRANCETRAVAIL_ID_CLIENT'),
            'FRANCETRAVAIL_CLE_SECRETE': os.getenv('FRANCETRAVAIL_CLE_SECRETE'),
            'RAW_DATA_PATH': os.getenv('RAW_DATA_PATH')
        },
        mounts=[Mount(target=os.getenv('RAW_DATA_PATH'), source=os.getenv('RAW_DATA_VOLUME_NAME'), type='volume')]
    )

    chargement_rome = DockerOperator(

        task_id='chargement_rome',
        image='chargement:latest',
        container_name='chargement_rome',
        api_version='auto',
        auto_remove=True,
        docker_url="TCP://docker-proxy:2375",
        mount_tmp_dir=False,
        command="python ./chargement_rome.py",
        environment={
            'DUCKDB_FILE': os.getenv('DUCKDB_FILE'),
            'DB_PATH': os.getenv('DB_PATH'),
            'RAW_DATA_PATH': os.getenv('RAW_DATA_PATH')
        },
        mounts=[
            Mount(target=os.getenv('RAW_DATA_PATH'), source=os.getenv('RAW_DATA_VOLUME_NAME'), type='volume'),
            Mount(target=os.getenv('DB_PATH'), source=os.getenv('DB_PATH_VOLUME_NAME'), type='volume')
        ]
    )

    collecte_rome >> chargement_rome

pipeline_offres_date()