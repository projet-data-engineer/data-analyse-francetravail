# Création d'un entrepôt de données à partir des offres d'emploi francetravail.io

Projet dans le cadre de la formation Data Engineer Datascientest.com

Développement d'une application d'analyse du marché de l'emploi à partir d'une extration quotidienne des offres d'emploi de francetravail.io.

## Sources de données

- **API Offres d'emploi** de [francetravail.io](https://francetravail.io). Extraction quotidienne des offres d'emploi du jour (env. 40 000 offres/jour)
- **Base Sirene des entreprises et de leurs établissements** (SIREN, SIRET) depuis [data.gouv](<https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/>). Téléchargement mensuel le 1er du mois sous forme de deux fichiers CSV (env. 10G de données)
- **IGN: limites géographiques** du découpage administratif du territoire français (commune, arrondissement départemental, département, région...). Ce jeu de données contient également les populations communales. Format ShapeFile
- **Nomenclatures**: Activité NAF (5 niveaux), métiers ROME (3 niveaux)

![vue-fonctionnelle](/doc/img/vue-fonctionnelle.png)

## Structure du projet

- **airflow**: ordonnancement des pipelines de données

  - **dags**: répertoire des fichiers DAG, monté sur /opt/airflow/dags du conteneur

    - **pipeline_nomenclature_rome.py**: collecte et chargement de la nomenclature ROME (3 niveaux dénormalisés)

    - **pipeline_offres_date.py**: collecte et chargement des offres francetravail créés J-1
  - **logs**: répertoire des logs Airflow, monté sur /opt/airflow/logs du conteneur

- **chargement**: scripts appelés par les pipelines qui chargent les données brutes collectées dans l'entrepôt DuckDB

- **collecte**: scripts appelés par les pipelines qui collectent les fichiers de données brutes depuis les sources de données

- **donnees_brutes**: emplacement local de stockage des fichiers bruts créés par les traitements de collecte

  - **collecte_offres_francetravail**: emplacement de stockage des fichiers de données brutes des offres d'emploi

  - **nomenclatures**: emplacement de stockage des fichiers de données brutes des nomenclatures

- **stockage**: emplacement local du fichier de persistance de l'entrepôt DuckDB

  - **entrepot-emploi.duckdb**: fichier de persistance de l'entrepôt DuckDB

## Execution locale du projet

### Prérequis

- Inscription sur la plateforme [francetravail.io](https://francetravail.io/inscription)
- Créer une application sur la plateforme et y ajouter l'**API Offres d'emploi**
- NB: un couple identifiant/clé secrète est associé à l'application créée. Ce couple identifiant/clé secrète doit être renseigné dans un fichier .env (cf. plus bas), et est utilisé pour authentifier les appels vers l'API dans le traitement d'extraction

### Créer un fichier .env à la racine du projet

```text
COMPOSE_PROJECT_NAME=entrepot-francetravail

FRANCETRAVAIL_HOST=https://api.francetravail.io
FRANCETRAVAIL_ID_CLIENT=<FRANCETRAVAIL_ID_CLIENT>
FRANCETRAVAIL_CLE_SECRETE=<FRANCETRAVAIL_CLE_SECRETE>

CHEMIN_LOCAL_DONNEES_BRUTES=./donnees_brutes
CHEMIN_DONNEES_BRUTES=/donnees_brutes

CHEMIN_LOCAL_STOCKAGE=./stockage
CHEMIN_STOCKAGE=/stockage
NOM_FICHIER_STOCKAGE=entrepot-emploi.duckdb
```

### Execution Docker

```bash
#!/bin/bash

docker-compose build
docker-compose up -d
```

## Construction de l'entrepôt de données

[Documentation des pipelines de données](./airflow/pipelines-donnees.md)
