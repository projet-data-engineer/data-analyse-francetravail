# data-analyse-francetravail

Projet dans le cadre de la formation Data Engineer Datascientest.com

Développement d'une application d'analyse du marché de l'emploi à partir d'une extration quotidienne des offres d'emploi de francetravail.io.

## Sources de données

- **API Offres d'emploi** de [francetravail.io](https://francetravail.io). Extraction quotidienne des offres d'emploi du jour (env. 40 000 offres/jour)
- **Base Sirene des entreprises et de leurs établissements** (SIREN, SIRET) depuis [data.gouv](<https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/>). Téléchargement mensuel le 1er du mois sous forme de deux fichiers CSV (env. 10G de données)
- **IGN: limites géographiques** du découpage administratif du territoire français (commune, arrondissement départemental, département, région...). Ce jeu de données contient également les populations communales. Format ShapeFile
- **Nomenclatures**: Activité NAF (5 niveaux), métiers ROME (3 niveaux)

![vue-fonctionnelle](/doc/img/vue-fonctionnelle.png)

## Execution locale du projet

- Prérequis

  - Inscription sur la plateforme [francetravail.io](https://francetravail.io/inscription)
  - Créer une application sur la plateforme et y ajouter l'**API Offres d'emploi**
  - NB: un couple identifiant/clé secrète est associé à l'application créée. Ce couple identifiant/clé secrète doit être renseigné dans un fichier .env (cf. plus bas), et est utilisé pour authentifier les appels vers l'API dans le traitement d'extraction

![interface web Airflow](/doc/img/francetravail.png)

- Créer les volumes Docker suivants:

  - **raw_data**: volume utilisé pour stockage des fichiers brutes
  - **database**: volume utilisé pour stockage du fichier de base de données DuckDB

```bash
#!/bin/bash

# Création des volumes Docker raw-data et db
docker volume create raw_data
docker volume create database
```

- Créer un fichier **.env** à la racine du projet avec les variables ci-dessous:

```text
COMPOSE_PROJECT_NAME=data-analyse-francetravail

FRANCETRAVAIL_HOST=https://api.francetravail.io
FRANCETRAVAIL_ID_CLIENT=<FRANCETRAVAIL_ID_CLIENT>
FRANCETRAVAIL_CLE_SECRETE=<FRANCETRAVAIL_CLE_SECRETE>

DUCKDB_FILE=warehouse.duckdb

RAW_DATA_PATH=/raw_data
RAW_DATA_VOLUME_NAME=raw_data

DB_PATH=/database
DB_PATH_VOLUME_NAME=database
```

### Execution unitaire du conteneur de collecte des offres

```bash
#!/bin/bash

docker image build -t collecte_offres_date:latest extraction/francetravail/
docker run --rm --name collecte_offres_date --env-file=.env -v raw_data:/raw_data -e DATE_CREATION='2024-05-22' collecte_offres_date:latest python ./collecte_offres_date.py
```

### Execution unitaire du conteneur de chargement des offres

```bash
#!/bin/bash

docker image build -t chargement:latest chargement/
docker run --rm --name chargement --env-file=.env -v raw_data:/raw_data -v database:/database -e DATE_CREATION='2024-05-22' chargement:latest python ./chargement_offres_date.py
```

### Execution des pipelines dans Airflow

```bash
#!/bin/bash

docker-compose up -d
```