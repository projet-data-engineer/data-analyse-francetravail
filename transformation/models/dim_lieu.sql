WITH
    commune_arm AS (
        SELECT
            version AS version,
            insee_com AS code,
            insee_com AS code_parent,
            insee_dep AS code_dep,
            insee_reg AS code_reg,
            nom AS nom,
            population AS population,
            geom AS frontiere
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_commune') }}
        UNION
        SELECT
            version AS version,
            insee_arm AS code,
            insee_com AS code_parent,
            null AS code_dep,
            null AS code_reg,
            nom AS nom,
            population AS population,
            geom AS frontiere
        FROM
            {{ source('collecte_cog_carto', 'cog_carto_arrondissement_municipal') }}
    )

    SELECT
        c.version AS version,
        c.code AS code,
        c.code_parent AS code_parent,
        c.nom AS nom,
        c.population AS population,
        c.frontiere AS frontiere,
        c.code_dep AS code_dep,
        d.nom AS nom_dep,
        d.geom AS frontiere_dep,
        c.code_reg AS code_reg,
        r.nom AS nom_reg,
        r.geom AS frontiere_reg
    FROM
        commune_arm AS c
    LEFT JOIN
        {{ source('collecte_cog_carto', 'cog_carto_departement') }} AS d
    ON
        d.insee_dep = c.code_dep
    LEFT JOIN
        {{ source('collecte_cog_carto', 'cog_carto_region') }} AS r
    ON
        r.insee_reg = c.code_reg