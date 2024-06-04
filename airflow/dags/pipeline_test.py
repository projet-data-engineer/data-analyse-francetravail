from datetime import datetime, timedelta
import os
from airflow import DAG
import pendulum

from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator

from docker.types import Mount


local_tz = pendulum.timezone("Europe/Paris")

"""
Tous les jours à 01h00, requêtage api des offres créées J-1, puis chargement
"""

dag = DAG(
    dag_id='pipeline_test',
    schedule=None,
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)

test = DockerOperator(

    task_id='test',
    image='collecte:latest',
    container_name='test',
    api_version='auto',
    auto_remove=True,
    docker_url="TCP://docker-proxy:2375",
    mount_tmp_dir=False,
    command="python ./collecte_test_file.py",
    network_mode="data-emploi",
    environment={
        'RAW_DATA_PATH': os.getenv('RAW_DATA_PATH')
    },
    mounts=[Mount(source="raw_data", target="/raw_data", type="volume")],
    dag=dag
)

test