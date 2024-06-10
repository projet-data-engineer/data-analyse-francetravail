# Création d'un entrepôt de données à partir des offres d'emploi francetravail.io

## Présentation générale

### Description du projet

Projet dans le cadre de la formation Data Engineer Datascientest.com.
Développement d'une application d'analyse du marché de l'emploi à partir d'une extration quotidienne des offres d'emploi de francetravail.io.

### Sources de données

- **API Offres d'emploi** de [francetravail.io](https://francetravail.io): source de données principale.

- **Base d'immatriculation Sirene des entreprises et de leurs établissements** depuis [data.gouv](<https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/>): pour étude corrélation entre le nombre d'établissements d'un secteur d'activité donné pour un territoire et le nombre d'offres d'emploi du même secteur.

- **IGN: limites géographiques** du découpage administratif du territoire français (commune, arrondissement départemental, département, région...). Ce jeu de données contient également les populations communales. Format ShapeFile. [ADMIN-EXPRESS-COG-CARTO](<https://geoservices.ign.fr/adminexpress#telechargementCogCarto/>)

- **Nomenclatures**: Activité NAF (5 niveaux), métiers ROME (3 niveaux)

![vue-fonctionnelle](/doc/img/vue-fonctionnelle.png)

### Structure du projet

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

### Execution locale du projet

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

URI_COG_CARTO=https://data.geopf.fr/telechargement/download/ADMIN-EXPRESS-COG-CARTO/ADMIN-EXPRESS-COG-CARTO_3-2__SHP_WGS84G_FRA_2024-02-22/ADMIN-EXPRESS-COG-CARTO_3-2__SHP_WGS84G_FRA_2024-02-22.7z


CHEMIN_LOCAL_DONNEES_BRUTES=./donnees_brutes
CHEMIN_DONNEES_BRUTES=/donnees_brutes

CHEMIN_LOCAL_STOCKAGE=./stockage
CHEMIN_STOCKAGE=/stockage
NOM_FICHIER_STOCKAGE=entrepot-emploi.duckdb
```

- **Execution Docker**

```bash
#!/bin/bash

docker-compose build
docker-compose up -d
```

## Construction de l'entrepôt de données

### Sources de données et traitements de collecte

#### Limites géographiques des territoires

- Source: Géoservices de l'IGN - ADMIN-EXPRESS-COG-CARTO

- [Documentation ADMIN EXPRESS Version 3.2](https://geoservices.ign.fr/sites/default/files/2023-06/DC_DL_ADMIN_EXPRESS_3-2.pdf)

- URL de téléchargement des jeux de données: [Page de téléchargement IGN COG CARTO](https://geoservices.ign.fr/adminexpress#telechargementCogCarto)

  - Format: ShapeFile

  - Contenu des jeux de données: les jeux de données contiennent les limites géographiques pour l'ensemble des niveaux territoriaux (régions, département, communes, arrondissements municipaux, collectivités territoriales, etc ...)

  - Les jeux de données sont disponibles avec 2 niveaux de précisions, et pour différentes zones géographiques influant sur le système de projection géographique

    - Précision entre 2.5 et 30 m pour ADMIN EXPRESS & ADMIN EXPRESS COG
    - Précision entre 15 et 30 m ADMIN EXPRESS COG CARTO

- Jeu de données retenu: **ADMIN-EXPRESS-COG-CARTO édition 2024 France entière**

  - URL: <https://data.geopf.fr/telechargement/download/ADMIN-EXPRESS-COG-CARTO/ADMIN-EXPRESS-COG-CARTO_3-2__SHP_WGS84G_FRA_2024-02-22/ADMIN-EXPRESS-COG-CARTO_3-2__SHP_WGS84G_FRA_2024-02-22.7z>

  - Système de projection: WGS84G (Métropole + DROM)

  - Procédure

### Chargement des données dans l'entrepôt

### Transformation

- Installation dbt-duckdb

```powershell
python -m pip install dbt-duckdb

dbt --version                   
Core:
  - installed: 1.8.2   
  - latest:    1.8.2 - Up to date!

Plugins:
  - duckdb: 1.8.1 - Up to date!   
```

- Création du projet DBT "transformation"

```powershell
dbt init transformation
10:06:31  Running with dbt=1.8.2
10:06:31
Your new dbt project "transformation" was created!

For more information on how to configure the profiles.yml file,
please consult the dbt documentation here:

  https://docs.getdbt.com/docs/configure-your-profile

One more thing:

Need help? Don't hesitate to reach out to us via GitHub issues or on Slack:

  https://community.getdbt.com/

Happy modeling!

10:06:31  Setting up your profile.
Which database would you like to use?
[1] duckdb

(Don't see the one you want? https://docs.getdbt.com/docs/available-adapters)

Enter a number: 1 
```

- Ajouter un fichier **profiles.yml** à la racine du dossier transformation

```yaml
transformation:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ..\stockage\entrepot.duckdb
      schema: entrepot
    prod:
      type: duckdb
      path: ..\stockage\entrepot.duckdb
      schema: entrepot
```

- Tester la connexion avec la commande dbt debug qui doit se terminer par le message *All checks passed!*

```powershell

cd .\transformation\

# Tester la configuration; Doit se terminer par le message "All checks passed!"
dbt debug

07:48:42  Running with dbt=1.8.2
07:48:42  dbt version: 1.8.2
07:48:42  python version: 3.10.11
07:48:42  python path: C:\privé\DE\data-analyse-francetravail\.venv\Scripts\python.exe
07:48:42  os info: Windows-10-10.0.19044-SP0
07:48:43  Using profiles dir at C:\privé\DE\data-analyse-francetravail\transformation
07:48:43  Using profiles.yml file at C:\privé\DE\data-analyse-francetravail\transformation\profiles.yml
07:48:43  Using dbt_project.yml file at C:\privé\DE\data-analyse-francetravail\transformation\dbt_project.yml
07:48:43  adapter type: duckdb
07:48:43  adapter version: 1.8.1
07:48:43  Configuration:
07:48:43    profiles.yml file [OK found and valid]
07:48:43    dbt_project.yml file [OK found and valid]
07:48:43  Required dependencies:
07:48:43   - git [OK found]

07:48:43  Connection:
07:48:43    database: entrepot
07:48:43    schema: entrepot
07:48:43    path: ..\stockage\entrepot.duckdb
07:48:43    config_options: None
07:48:43    extensions: None
07:48:43    settings: None
07:48:43    external_root: .
07:48:43    use_credential_provider: None
07:48:43    attach: None
07:48:43    filesystems: None
07:48:43    remote: None
07:48:43    plugins: None
07:48:43    disable_transactions: False
07:48:43  Registered adapter: duckdb=1.8.1
07:48:43    Connection test: [OK connection ok]

07:48:43  All checks passed!

# Générer la documentation DBT
dbt docs generate

# Executer le site web local de documentation
dbt docs serve

# Execution des models DBT, construction de l'entrepôt
dbt run

```

### Pipelines de données & ordonnacement avec Apache Airflow

#### pipeline_offres_date

- Fichier de DAG: ./airflow/dags/pipeline_offres_date.py
- Programmation: Tous les jours à 01h00
- Description: afin d'historiser les données des offres d'emploi, on collecte tous les jours à 01h00 les offres créés la journée écoulée.

![Graphe pipeline_offres_date](/doc/img/pipeline_offres_date.png)

#### pipeline_nomenclature_rome

- Fichier de DAG: ./airflow/dags/pipeline_nomenclature_rome.py
- Programmation: éxecution manuelle
- Description: collecte des 3 niveaux dénormalisés de la nomenclature ROME
- Source:

Exemple d'item de nomenclature ROME:

```json
[
    {
        "code_1": "M",
        "libelle_1": "Support à l'entreprise",
        "code_2": "M18",
        "libelle_2": "Systèmes d'information et de télécommunication",
        "code_3": "M1811",
        "libelle_3": "Data engineer"
    }
]
```

![Graphe pipeline_nomenclature_rome](/doc/img/pipeline_nomenclature_rome.png)

#### pipeline_nomenclature_naf

- Fichier de DAG: ./airflow/dags/pipeline_nomenclature_naf.py
- Programmation: éxecution manuelle
- Description: Chargement des fichiers CSV de la Nomenclature d’activités française – NAF rév. 2
- Source: (<https://www.insee.fr/fr/information/2120875>)
  - Format: Excel
  - Téléchargement des 6 fichiers suivants: Sections, Divisions, Groupes, Classes, Sous-classes, Les 5 niveaux emboîtés
  - Les fichiers Excel sont légèrement retravaillés pour les rendre compatibles au format CSV
  - Export CSV des 6 fichiers Excel dans le dossier donnees_brutes/naf

#### pipeline_etablissements_sirene

- Fichier de DAG: ./airflow/dags/pipeline_etablissements_sirene.py
- Programmation: éxecution mensuelle, le 1er de chaque mois
- Description: chargement dans entrepôt DuckDB nomenclature NAF (5 niveaux dénormalisés)

## Requêtage de l'entrepôt DuckDB

Fichier de persistence DuckDB: **./stockage/entrepot-emploi.duckdb**

Les accès à l'entrepôt sont réalisés de deux manières:

- Via l'API Python: [Documentation API Python DuckDB](https://duckdb.org/docs/api/python/overview)
- Via une interface CLI pour les tests/développement: [Documentation CLI DuckDB](https://duckdb.org/docs/api/cli/overview)
- [Installation DuckDB](https://duckdb.org/docs/installation/?version=stable&environment=cli&platform=win&download_method=package_manager)

### Guide de démarrage rapide avec la CLI

- Liens de téléchargement:

  - DuckDB CLI Windows: https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-windows-amd64.zip
  - DuckDB CLI macOS: https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-osx-universal.zip
  - DuckDB CLI Linux: https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip

- Execution sur une machine Windows:

  - Décompacter le zip à la racine du projet et se positionner sur cet emplacement dans une fenêtre de terminal
  - Lancer la CLI en indiquant le chemin vers le fichier de persistence DuckDB

```powershell
.\duckdb.exe ..\stockage\entrepot-emploi.duckdb
v1.0.0 1f98600c2c
Enter ".help" for usage hints.
D
```

- Quelques exemples de requêtes de découverte de l'entrepôt de données

```powershell
D SELECT COUNT(*) FROM collecte.raw_offre;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│        38199 │
└──────────────┘

D SELECT database_name, path FROM duckdb_databases();
┌───────────────┬─────────────────────────────┐
│ database_name │            path             │
│    varchar    │           varchar           │
├───────────────┼─────────────────────────────┤
│ entrepot      │ ..\stockage\entrepot.duckdb │
│ system        │                             │
│ temp          │                             │
└───────────────┴─────────────────────────────┘

D SELECT schema_name,table_name,column_count FROM duckdb_tables();
┌─────────────┬────────────────────────────────────┬──────────────┐
│ schema_name │             table_name             │ column_count │
│   varchar   │              varchar               │    int64     │
├─────────────┼────────────────────────────────────┼──────────────┤
│ collecte    │ cog_carto_arrondissement_municipal │            6 │
│ collecte    │ cog_carto_commune                  │            8 │
│ collecte    │ cog_carto_departement              │            5 │
│ collecte    │ cog_carto_region                   │            4 │
│ collecte    │ etablissement                      │           54 │
│ collecte    │ naf                                │           10 │
│ collecte    │ naf_hierarchie                     │            5 │
│ collecte    │ naf_niveau_1                       │            2 │
│ collecte    │ naf_niveau_2                       │            2 │
│ collecte    │ naf_niveau_3                       │            2 │
│ collecte    │ naf_niveau_4                       │            2 │
│ collecte    │ naf_niveau_5                       │            2 │
│ collecte    │ raw_offre                          │           16 │
│ collecte    │ rome                               │            6 │
│ collecte    │ rome_domaine                       │            2 │
│ collecte    │ rome_famille                       │            2 │
│ collecte    │ rome_metier                        │            2 │
├─────────────┴────────────────────────────────────┴──────────────┤
│ 17 rows                                               3 columns │
└─────────────────────────────────────────────────────────────────┘

D SELECT schema_name, table_name FROM duckdb_tables() WHERE schema_name = 'entrepot'; 
┌─────────────┬────────────┐
│ schema_name │ table_name │
│   varchar   │  varchar   │
├─────────────┼────────────┤
│ entrepot    │ dim_naf    │
└─────────────┴────────────┘

D SELECT database_name, schema_name FROM duckdb_schemas(); 
┌───────────────┬────────────────────┐
│ database_name │    schema_name     │
│    varchar    │      varchar       │
├───────────────┼────────────────────┤
│ entrepot      │ collecte           │
│ entrepot      │ entrepot           │
│ entrepot      │ information_schema │
│ entrepot      │ main               │
│ entrepot      │ pg_catalog         │
│ system        │ information_schema │
│ system        │ main               │
│ system        │ pg_catalog         │
│ temp          │ information_schema │
│ temp          │ main               │
│ temp          │ pg_catalog         │
├───────────────┴────────────────────┤
│ 11 rows                  2 columns │
└────────────────────────────────────┘

D SELECT schema_name, view_name FROM duckdb_views() WHERE schema_name in ('entrepot', 'collecte');
┌─────────────┬───────────┐
│ schema_name │ view_name │
│   varchar   │  varchar  │
├─────────────┼───────────┤
│ entrepot    │ dim_naf   │
└─────────────┴───────────┘ 

D describe table collecte.cog_carto_commune;
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ version     │ VARCHAR     │ YES     │         │         │         │
│ ID          │ VARCHAR     │ YES     │         │         │         │
│ NOM         │ VARCHAR     │ YES     │         │         │         │
│ NOM_M       │ VARCHAR     │ YES     │         │         │         │
│ INSEE_COM   │ VARCHAR     │ YES     │         │         │         │
│ STATUT      │ VARCHAR     │ YES     │         │         │         │
│ POPULATION  │ INTEGER     │ YES     │         │         │         │
│ INSEE_CAN   │ VARCHAR     │ YES     │         │         │         │
│ INSEE_ARR   │ VARCHAR     │ YES     │         │         │         │
│ INSEE_DEP   │ VARCHAR     │ YES     │         │         │         │
│ INSEE_REG   │ VARCHAR     │ YES     │         │         │         │
│ SIREN_EPCI  │ VARCHAR     │ YES     │         │         │         │
│ geom        │ GEOMETRY    │ YES     │         │         │         │
├─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 13 rows                                                 6 columns │
└───────────────────────────────────────────────────────────────────┘



SELECT schema_name,table_name,column_count FROM duckdb_tables();  

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

- Execution sur une machine Linux:

```bash
#!/bin/bash

# Téléchargement DuckDB CLI, décompactage puis suppression du fichier compacté.

cd <projet_dir>
wget --no-check-certificate https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip && \
unzip duckdb_cli-linux-amd64.zip && \
rm duckdb_cli-linux-amd64.zip

./duckdb ..\stockage\entrepot-emploi.duckdb
v1.0.0 1f98600c2c
Enter ".help" for usage hints.
D
```