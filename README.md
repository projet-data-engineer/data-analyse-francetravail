# Formation DataScientest - Data Engineer - Projet "Job Market"

Développement d'une application d'analyse du marché de l'emploi à partir d'une extration quotidienne des offres d'emploi de francetravail.io.

## Execution locale du projet

- Création des volumes Docker

  - **raw-data**: volume utilisé pour stockage des fichiers brutes
  - **db**: volume utilisé pour stockage du fichier de base de données DuckDB

- Création d'un fichier .env à la racine du projet

  - Une inscription sur la plateforme francetravail.io est requise: <https://francetravail.io/inscription>
  - Une

```text
COMPOSE_PROJECT_NAME=data-emploi
FRANCETRAVAIL_HOST=https://api.francetravail.io
FRANCETRAVAIL_ID_CLIENT=<FRANCETRAVAIL_ID_CLIENT>
FRANCETRAVAIL_CLE_SECRETE=<FRANCETRAVAIL_CLE_SECRETE>
```

```bash
#!/bin/bash

# Création des volumes Docker raw-data et db
docker volume create raw-data
docker volume create db
```

### Extraction des offres francetravail.io

```bash
#!/bin/bash

cd extraction/francetravail/
docker image build -t extraction_francetravail:latest .

docker run --rm --name extraction_francetravail --env-file=.env -v raw-data:/raw-data -e DATE_CREATION='<date_creation>' extraction_francetravail:latest
```

### Chargement des offres francetravail.io dans DuckDB

```bash
#!/bin/bash

cd chargement/francetravail/
docker image build -t chargement_francetravail:latest .

docker run --name chargement_francetravail \
    --rm \
    -v db:/db \
    -v raw-data:/raw-data \
    -e JSON_FILE='/raw-data/offres-francetravail.io-2024-05-16.json' \
    -e DB_FILE='/db/warehouse.db' \
    chargement_francetravail:latest

docker run --name chargement_francetravail --rm -v db:/db -v raw-data:/raw-data -e JSON_FILE='/raw-data/offres-francetravail.io-2024-05-16.json' -e DB_FILE='/db/warehouse.db' chargement-francetravail:latest
```
    