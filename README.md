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

    - **pipeline_nomenclature_naf.py**: chargement dans entrepôt DuckDB nomenclature NAF (5 niveaux dénormalisés)

  - **logs**: répertoire des logs Airflow, monté sur /opt/airflow/logs du conteneur

- **chargement**: scripts appelés par les pipelines qui chargent les données brutes collectées dans l'entrepôt DuckDB

- **collecte**: scripts appelés par les pipelines qui collectent les fichiers de données brutes depuis les sources de données

- **donnees_brutes**: emplacement local de stockage des fichiers bruts créés par les traitements de collecte

  - **collecte_offres_francetravail**: emplacement de stockage des fichiers de données brutes des offres d'emploi

  - **collecte_nomenclature_rome_francetravail**: emplacement de stockage du fichier brute de la nomenclature ROME collectée depuis francetravail.io

  - **nomenclature_naf_csv**: emplacement de stockage des fichiers brutes des 5 niveaux de la nomenclature NAF

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

## Requêtage de l'entrepôt DuckDB

Fichier de persistence DuckDB: **./stockage/entrepot-emploi.duckdb**

Les accès à l'entrepôt sont réalisés de deux manières:

- Via l'API Python: [Documentation API Python DuckDB](https://duckdb.org/docs/api/python/overview)
- Via une interface CLI: [Documentation CLI DuckDB](https://duckdb.org/docs/api/cli/overview)
- [Installation DuckDB](https://duckdb.org/docs/installation/?version=stable&environment=cli&platform=win&download_method=package_manager)

### Guide de démarrage rapide avec la CLI

- Liens de téléchargement:

  - [DuckDB CLI Windows](https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-windows-amd64.zip)
  - [DuckDB CLI macOS](https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-osx-universal.zip)
  - [DuckDB CLI Linux](https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip)

- Execution sur une machine Windows:

  - Décompacter le zip à la racine du projet et se positionner sur cet emplacement dans une fenêtre de terminal
  - Lancer la CLI en indiquant le chemin vers le fichier de persistence DuckDB

```powershell
.\duckdb.exe ..\stockage\entrepot-emploi.duckdb
v1.0.0 1f98600c2c
Enter ".help" for usage hints.
D
```

- Quelques exemples de requêtes

```powershell
D SHOW ALL TABLES; 

D SELECT COUNT(*) FROM collecte.raw_offre;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        38199 │
└──────────────┘

D SELECT code_5,libelle_5,code_1,libelle_1 FROM collecte.naf LIMIT 5;
┌─────────┬────────────────────────────────────────────────────────────────────────────────────────┬─────────┬────────────────────────────────────┐
│ code_5  │                                       libelle_5                                        │ code_1  │             libelle_1              │
│ varchar │                                        varchar                                         │ varchar │              varchar               │
├─────────┼────────────────────────────────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┤
│ 01.11Z  │ Culture de céréales (à l'exception du riz), de légumineuses et de graines oléagineuses │ A       │ Agriculture, sylviculture et pêche │
│ 01.14Z  │ Culture de la canne à sucre                                                            │ A       │ Agriculture, sylviculture et pêche │
│ 01.16Z  │ Culture de plantes à fibres                                                            │ A       │ Agriculture, sylviculture et pêche │
│ 01.19Z  │ Autres cultures non permanentes                                                        │ A       │ Agriculture, sylviculture et pêche │
│ 01.22Z  │ Culture de fruits tropicaux et subtropicaux                                            │ A       │ Agriculture, sylviculture et pêche │
└─────────┴────────────────────────────────────────────────────────────────────────────────────────┴─────────┴────────────────────────────────────┘

D .quit
```