# Construction d'un entrepôt de données des basé sur les offres d'emploi France Travail

## Description

Projet dans le cadre de la formation Data Engineer Datascientest.com.
Développement d'une application d'analyse du marché de l'emploi à partir d'une extration quotidienne des offres d'emploi de francetravail.io.

## Sources de données

- **API Offres d'emploi** de [francetravail.io](https://francetravail.io): source de données principale.

- **Base d'immatriculation Sirene des entreprises et de leurs établissements** depuis [data.gouv](<https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/>): pour étude corrélation entre le nombre d'établissements d'un secteur d'activité donné pour un territoire et le nombre d'offres d'emploi du même secteur.

- **IGN: limites géographiques** du découpage administratif du territoire français (commune, arrondissement départemental, département, région...). Ce jeu de données contient également les populations communales. Format ShapeFile. [ADMIN-EXPRESS-COG-CARTO](<https://geoservices.ign.fr/adminexpress#telechargementCogCarto/>)

- **Nomenclatures**: Activité NAF (5 niveaux), métiers ROME (3 niveaux)

![vue-fonctionnelle](/doc/img/vue-fonctionnelle.png)

## Execution locale du projet

- **Prérequis**

  - Inscription sur la plateforme [francetravail.io](https://francetravail.io/inscription)
  - Créer une application sur la plateforme et y ajouter l'**API Offres d'emploi**
  - NB: un couple identifiant/clé secrète est associé à l'application créée. Ce couple identifiant/clé secrète doit être renseigné dans un fichier .env (cf. plus bas), et est utilisé pour authentifier les appels vers l'API dans le traitement d'extraction

- **Créer un fichier .env à la racine du projet** avec les variables ci-dessous.

Note: les variables FRANCETRAVAIL_ID_CLIENT et FRANCETRAVAIL_CLE_SECRETE doivent être valorisées avec les identifiants de l'application créée sur la plateforme francetravail.io.

```text
COMPOSE_PROJECT_NAME=entrepot-francetravail

FRANCETRAVAIL_HOST=https://api.francetravail.io
FRANCETRAVAIL_ID_CLIENT=<FRANCETRAVAIL_ID_CLIENT>
FRANCETRAVAIL_CLE_SECRETE=<FRANCETRAVAIL_CLE_SECRETE>

URI_STOCK_ETABLISSEMENT=https://www.data.gouv.fr/fr/datasets/r/0651fb76-bcf3-4f6a-a38d-bc04fa708576
VERSION_COG_CARTO=2024-02-22
URI_COG_CARTO=https://data.geopf.fr/telechargement/download/ADMIN-EXPRESS-COG-CARTO/ADMIN-EXPRESS-COG-CARTO_3-2__SHP_WGS84G_FRA_${VERSION_COG_CARTO}/ADMIN-EXPRESS-COG-CARTO_3-2__SHP_WGS84G_FRA_${VERSION_COG_CARTO}.7z

CHEMIN_LOCAL_DONNEES_BRUTES=./donnees_brutes
CHEMIN_DONNEES_BRUTES=/donnees_brutes

DESTINATION_RACINE=/donnees_brutes
DESTINATION_RACINE_LOCAL=./donnees_brutes

DOSSIER_COG_CARTO=cog_carto
DOSSIER_ROME=rome
DOSSIER_OFFRE_EMPLOI=offre_emploi
DOSSIER_NAF=naf
DOSSIER_SIRENE=sirene

DESTINATION_STOCKAGE_LOCAL=./stockage
DESTINATION_STOCKAGE=/stockage
DUCKDB_ENTREPOT=entrepot.duckdb
```

- Créer un environnement virtuel Python à la racine du projet puis installer les dépendances

```powershell
python -m pip install -r requirements.txt
```

- **Execution Docker**

```bash
#!/bin/bash

docker-compose build
docker-compose up -d
```

## Collecte

- scripts de collecte des sources de données

[Documentation Sources de données et traitements de collecte](./collecte/docs/README.md)

## Chargement

- scripts de chargement des données brutes collectées dans l'entrepôt DuckDB

## Transformation - DBT

- projet DBT qui contruit le schéma en étoile de l'entrepôt à partir des données brutes déjà chargées dans l'entrepôt

[Documentation Transformation des données brutes avec DBT](./transformation/docs/README.md)

## Stockage - Entrepôt DuckDB

[Documentation Requêtage de l'entrepôt DuckDB](./stockage/docs/README.md)

## Pipelines de données & Ordonnancement Apache Airflow

[Documentation Pipelines de données & Ordonnancement Apache Airflow](./airflow/docs/README.md)

## Présentation: API et visualisation des données

[Documentation API et visualisation des données](./presentation/docs/README.md)
