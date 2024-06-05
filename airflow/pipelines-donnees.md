# Pipelines de données

## pipeline_offres_date

- Fichier de DAG: ./airflow/dags/pipeline_offres_date.py
- Programmation: Tous les jours à 01h00
- Description: afin d'historiser les données des offres d'emploi, on collecte tous les jours à 01h00 les offres créés la journée écoulée.

![Graphe pipeline_offres_date](/doc/img/pipeline_offres_date.png)

## pipeline_nomenclature_rome

- Fichier de DAG: ./airflow/dags/pipeline_nomenclature_rome.py
- Programmation: éxecution manuelle
- Description: collecte des 3 niveaux dénormalisés de la nomenclature ROME

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

## pipeline_nomenclature_naf

- Fichier de DAG: ./airflow/dags/pipeline_nomenclature_naf.py
- Programmation: éxecution manuelle
- Description: chargement dans entrepôt DuckDB nomenclature NAF (5 niveaux dénormalisés)
