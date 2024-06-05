import json
import os
import time
import requests

"""
# 
# API Rome francetravail.io
# Collecte de la nomenclature ROME: 3 niveaux Grands Domaines > Domaines professionnels > métiers
# Dénormalisation des 3 niveaux dans un fichier rome.json
#
"""


def authenticate(identifiant_client, cle_secrete):

    url = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}    

    params = {
        'grant_type': 'client_credentials',
        'scope': 'api_rome-metiersv1 nomenclatureRome',
        'client_id': identifiant_client,
        'client_secret': cle_secrete
    }

    response = requests.post(url=url,data=params,headers=headers)
    response = json.loads(response.text)
    return response['access_token']


def get_data(url, access_token):

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url=url, headers=headers)

    while response.status_code == 429:            
            
        retry_after = response.headers['Retry-After']
        time.sleep(int(retry_after))
        response = requests.get(url=url,headers=headers) 

    response.encoding = 'utf-8'
    return response.text



def collecte(chemin_donnees_brutes, nom_fichier_donnees_brutes):
  
    romes = []

    FRANCETRAVAIL_ID_CLIENT = os.getenv("FRANCETRAVAIL_ID_CLIENT")
    FRANCETRAVAIL_CLE_SECRETE = os.getenv("FRANCETRAVAIL_CLE_SECRETE")

    access_token = authenticate(FRANCETRAVAIL_ID_CLIENT, FRANCETRAVAIL_CLE_SECRETE)
    url_rome = f"{os.getenv('FRANCETRAVAIL_HOST')}/partenaire/rome-metiers/v1/metiers"

    familles = json.loads(get_data(url=f"{url_rome}/grand-domaine", access_token=access_token))
    domaines = json.loads(get_data(url=f"{url_rome}/domaine-professionnel", access_token=access_token))
    metiers = json.loads(get_data(url=f"{url_rome}/metier", access_token=access_token))

    for metier in metiers:
        
        rome = {}

        grand_domaine = [data for data in familles if metier['code'][0] == data['code']]
        domaine_professionnel = [data for data in domaines if metier['code'][0:3] == data['code']]

        rome['code_1'] = grand_domaine[0]['code']
        rome['libelle_1'] = grand_domaine[0]['libelle']
        rome['code_2'] = domaine_professionnel[0]['code']
        rome['libelle_2'] = domaine_professionnel[0]['libelle']
        rome['code_3'] = metier['code']
        rome['libelle_3'] = metier['libelle']

        romes.append(rome)

    path = os.path.join(chemin_donnees_brutes, "nomenclatures")
    if not os.path.exists(path):
        os.mkdir(path)
        
    file_path = os.path.join(path, nom_fichier_donnees_brutes)

    with open(file_path, 'w') as output_file:
        json.dump(romes, output_file, indent=2, ensure_ascii=False)

    print(f"\nFin collecte de {len(romes)} enregistrements depuis api Rome francetravail.io\n")