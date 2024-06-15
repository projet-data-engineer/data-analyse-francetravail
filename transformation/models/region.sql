WITH
    region AS (
        SELECT
            version AS version,
            insee_reg AS code,            
            nom AS nom,
            geom AS frontiere            
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_region') }}
    )
    SELECT
        *
    FROM
        region