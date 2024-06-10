SELECT
    offre.id,
    CAST(offre.dateCreation AS DATE) AS date_creation,
    offre.lieuTravail.commune AS lieu_travail_code,
    offre.lieuTravail.latitude AS lieu_travail_latitude,
    offre.lieuTravail.longitude AS lieu_travail_longitude,
    offre.codeNAF AS code_naf,
    offre.romeCode AS code_rome,
    offre.entreprise.entrepriseAdaptee AS entreprise_adaptee,
    offre.typeContrat AS type_contrat,
    offre.natureContrat AS nature_contrat,
    offre.experienceExige AS experience_exige,
    offre.alternance AS alternance,
    offre.nombrePostes AS nombre_postes,
    offre.accessibleTH AS accessible_TH,
    CAST(offre.qualificationCode AS VARCHAR) AS qualification_code
FROM
    {{ source('collecte_offre_emploi', 'offre_emploi') }} as offre