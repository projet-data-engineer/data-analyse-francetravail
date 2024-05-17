# data-analyse-francetravail

Projet dans le cadre de la formation Data Engineer Datascientest.com

Développement d'une application d'analyse du marché de l'emploi à partir d'une extration quotidienne des offres d'emploi de francetravail.io.

## Execution locale du projet

- Création des volumes Docker

  - **raw-data**: volume utilisé pour stockage des fichiers brutes
  - **db**: volume utilisé pour stockage du fichier de base de données DuckDB

```bash
#!/bin/bash

# Création des volumes Docker raw-data et db
docker volume create raw-data
docker volume create db
```

- Création d'un fichier .env à la racine du projet

```text
COMPOSE_PROJECT_NAME=data-emploi
FRANCETRAVAIL_HOST=https://api.francetravail.io
FRANCETRAVAIL_ID_CLIENT=<FRANCETRAVAIL_ID_CLIENT>
FRANCETRAVAIL_CLE_SECRETE=<FRANCETRAVAIL_CLE_SECRETE>
```

- Execution Apache Airflow

```bash
#!/bin/bash

docker-compose up -d
```

- Interface de gestion Apache Airflow

![interface web Airflow](/doc/img/airflow-francetravail.png)

- Pipeline **france-travail-pipeline**

  - Task **extraction_api_francetravail**: extraction des offres depuis api francetravail.io créées à une date donnée, et export des résultats dans un fichier json
  - Task **chargement_duckdb_francetravail**: chargement du fichier json dans DuckDB.