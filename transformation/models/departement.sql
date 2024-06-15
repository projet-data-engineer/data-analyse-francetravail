WITH
    departement AS (
        SELECT
            version AS version,
            insee_dep AS code,            
            nom AS nom,
            insee_reg AS code_region,
            geom AS frontiere            
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_departement') }}
    )
    SELECT
        *
    FROM
        departement