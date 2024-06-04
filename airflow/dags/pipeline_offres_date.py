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
    dag_id='pipeline_offres_date',
    description='A simple tutorial DAG',
    schedule_interval='0 1 * * *',
    start_date=datetime(2024, 5, 23, tzinfo=local_tz),
    catchup=False
)


"""
retourne <date_execution_dag> - 1 jour
"""
@task
def date_creation(ds):
    return (datetime.strptime(ds, '%Y-%m-%d') + timedelta(days=-1)).strftime('%Y-%m-%d')

_date_creation = date_creation()

collecte_offres_date = DockerOperator(

    task_id='collecte_offres_date',
    image='collecte:latest',
    container_name='collecte_offres_date',
    api_version='auto',
    auto_remove=True,
    docker_url="TCP://docker-proxy:2375",
    mount_tmp_dir=False,
    command="python ./collecte_offres_date.py",
    network_mode="data-emploi",
    environment={
        'FRANCETRAVAIL_HOST': os.getenv('FRANCETRAVAIL_HOST'),
        'FRANCETRAVAIL_ID_CLIENT': os.getenv('FRANCETRAVAIL_ID_CLIENT'),
        'FRANCETRAVAIL_CLE_SECRETE': os.getenv('FRANCETRAVAIL_CLE_SECRETE'),
        'DATE_CREATION': _date_creation,
        'RAW_DATA_PATH': os.getenv('RAW_DATA_PATH')
    },
    mounts=[Mount(source="raw_data", target="/raw_data", type="volume")],
    dag=dag
)

chargement_offres_date = DockerOperator(

    task_id='chargement_offres_date',
    image='chargement:latest',
    container_name='chargement_offres_date',
    api_version='auto',
    auto_remove=True,
    docker_url="TCP://docker-proxy:2375",
    mount_tmp_dir=False,
    command="python ./chargement_offres_date.py",
    network_mode="data-emploi",
    environment={
        'DUCKDB_FILE': os.getenv('DUCKDB_FILE'),
        'DB_PATH': os.getenv('DB_PATH'),
        'DATE_CREATION': _date_creation,
        'RAW_DATA_PATH': os.getenv('RAW_DATA_PATH')
    },
   mounts=[
        Mount(source="raw_data", target="/raw_data", type="volume"),
        Mount(source="database", target="/database", type="volume")
    ],
    dag=dag
)

collecte_offres_date >> chargement_offres_date