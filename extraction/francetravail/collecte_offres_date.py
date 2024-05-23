import requests
import json
import time
import os
from datetime import datetime, timedelta

MAX_OFFRES = 3149
export_json = []

FRANCETRAVAIL_HOST = os.getenv('FRANCETRAVAIL_HOST')
DATE_CREATION = os.getenv("DATE_CREATION")
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
FRANCETRAVAIL_ID_CLIENT = os.getenv("FRANCETRAVAIL_ID_CLIENT")
FRANCETRAVAIL_CLE_SECRETE = os.getenv("FRANCETRAVAIL_CLE_SECRETE")

SEARCH_URL = f"{FRANCETRAVAIL_HOST}/partenaire/offresdemploi/v2/offres/search"
REFERENTIEL_URL = f"{FRANCETRAVAIL_HOST}/partenaire/offresdemploi/v2/referentiel"

def authenticate():

    url = 'https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}    

    params = {
        'grant_type': 'client_credentials',
        'scope': 'api_offresdemploiv2 o2dsoffre'
    }

    params['client_id'] = FRANCETRAVAIL_ID_CLIENT
    params['client_secret'] = FRANCETRAVAIL_CLE_SECRETE

    response = requests.post(url=url,data=params,headers=headers)
    response = json.loads(response.text)
    return response['access_token']

def get_referentiel(url, access_token):

    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url=url, headers=headers)
    response.raise_for_status
    response.encoding = 'utf-8'
    return response.text

def save(response):

    if response.status_code in (200, 206):

        resultats = json.loads(response.text)['resultats']

        if resultats is not None:
            for offre in resultats:
                export_json.append(offre)

def get_nb_total_offres(url, access_token):

    headers = {'Authorization': f'Bearer {access_token}'}
    total = 0

    try:

        response = requests.get(url=f"{url}", headers=headers)

        if 'Content-Range' in response.headers:

            content_range = response.headers['Content-Range']
            # NB: si aucun résultat content_range == "offres */0 communes"
            if int(content_range.split('/')[1]) == 0:
                total = 0
            else:
                total = int(content_range.split(sep=' ')[1].split(sep='/')[1])
        
    except Exception as e:
        print(f"Oups {response.status_code} - {response.text}")
    finally:
        return total

def search(url, access_token):

    headers = {'Authorization': f'Bearer {access_token}'}

    response = None

    try:

        start, end, total = (0, 0, 0)

        # execution requête
        response = requests.get(url=url,headers=headers)

        #429 Too Many Requests 
        while response.status_code == 429:            
            
            print({
                "query": url, 
                "status_code": f"{response.status_code}", 
                "response": f"{response.text}"
            })

            retry_after = response.headers['Retry-After']
            time.sleep(int(retry_after))
            response = requests.get(url=url,headers=headers)  

        if 'Content-Range' in response.headers:

            content_range = response.headers['Content-Range']

            # NB: si aucun résultat content_range == "offres */0 communes"
            if int(content_range.split('/')[1]) == 0:
                start = 0
                end = 0
                total = 0            
            else:
                start = int(content_range.split(sep=' ')[1].split(sep='/')[0].split(sep='-')[0])
                end = int(content_range.split(sep=' ')[1].split(sep='/')[0].split(sep='-')[1])
                total = int(content_range.split(sep=' ')[1].split(sep='/')[1])

        else:
            
            start = 0
            end = 0
            total = 0

            print({
                "query": url, 
                "message": "HTTP Header Content-Range absent", 
                "status_code": f"{response.status_code}", 
                "response": f"{response.text}"
            })

    except Exception as e:
        
        print({
            "query": url, 
            "message": e, 
            "status_code": f"{response.status_code}", 
            "response": f"{response.text}"
        })

    finally:

        if response is not None:
            return start, end, total, response
        else:
            return start, end, total, None

def get_offres_metier(codeROME, regions, minCreationDate, maxCreationDate, access_token):

    start = 0
    end = 149
    total = 0
   
    url = f"{SEARCH_URL}?range={start}-{end}&minCreationDate={minCreationDate}&maxCreationDate={maxCreationDate}&codeROME={codeROME}"
    start, end, total, response = search(url, access_token)

    if total > MAX_OFFRES:

        print(f"{codeROME}: {total} > {MAX_OFFRES} ! Lancement du requêtage des offres {codeROME} par région...")

        for region in regions:
            get_offres_metier_region(codeROME, region['code'], minCreationDate, maxCreationDate, access_token)

    else:

        print(f"{codeROME}: {total}")

        if total > 0:

            save(response)

            while end < total - 1:

                start += 150
                end += 150

                url = f"{SEARCH_URL}?range={start}-{end}&minCreationDate={minCreationDate}&maxCreationDate={maxCreationDate}&codeROME={codeROME}"
                start, end, total, response = search(url, access_token)

                save(response)

def get_offres_metier_region(codeROME, region, minCreationDate, maxCreationDate, access_token):

    start = 0
    end = 149
    total = 0
    
    url = f"{SEARCH_URL}?range={start}-{end}&minCreationDate={minCreationDate}&maxCreationDate={maxCreationDate}&codeROME={codeROME}&region={region}"
    start, end, total, response = search(url, access_token)

    if total > MAX_OFFRES:

        print(f"!! MAX_OFFRES ATTEINT !! {url.split('?')[1]}")

    else:

        print(f"{codeROME} {region}: {total}")

        if total > 0:

            save(response)

            while end < total - 1:

                start += 150
                end += 150

                url = f"{SEARCH_URL}?range={start}-{end}&minCreationDate={minCreationDate}&maxCreationDate={maxCreationDate}&codeROME={codeROME}&region={region}"
                start, end, total, response = search(url, access_token)

                if response is not None:
                    save(response)
                else:
                    print(f"response is None ... {start}-{end}/{total}: {codeROME} {region}")

if __name__ == '__main__':    

    minCreationDate = datetime \
        .strptime(DATE_CREATION, '%Y-%m-%d') \
        .strftime('%Y-%m-%dT%H:%M:%SZ')

    maxCreationDate = (datetime.strptime(DATE_CREATION, '%Y-%m-%d') + timedelta(days=1)) \
        .strftime('%Y-%m-%dT%H:%M:%SZ')

    access_token = authenticate()

    url = f"{SEARCH_URL}?range=0-1&minCreationDate={minCreationDate}&maxCreationDate={maxCreationDate}"
    total_offres = get_nb_total_offres(url=url, access_token=access_token)

    debut_total = time.time()
    date_debut = datetime.now()

    print(f"\n\n{date_debut.strftime('%d/%m/%Y %H:%M:%S')}: démarrage collecte de {total_offres} offres d'emploi depuis francetravail.io\n\n")

    regions = json.loads(get_referentiel(url=f'{REFERENTIEL_URL}/regions', access_token=access_token))
    metiers = json.loads(get_referentiel(url=f'{REFERENTIEL_URL}/metiers', access_token=access_token))

    for metier in metiers:
        get_offres_metier(metier['code'], regions, minCreationDate, maxCreationDate, access_token)

    fin_total = time.time()

    path = os.path.join(RAW_DATA_PATH, "collecte-francetravail")
    if not os.path.exists(path):
        os.mkdir(path)

    file_path = f"{path}/offres-{minCreationDate.split(sep='T')[0]}.json"

    with open(file_path, 'w') as output_file:
        json.dump(export_json, output_file, indent=2)

    hours = int((fin_total - debut_total) // 3600)
    minutes = int((fin_total - debut_total) // 60)

    duree_totale = ('0' + str(hours) if hours < 10 else str(hours)) + ':' + ('0' + str(minutes) if minutes < 10 else str(minutes))

    ingestion_data = {
        "message": "Fin collecte des offres francetravail.io",
        "date_debut": date_debut.strftime('%d/%m/%Y %H:%M:%S'),
        "date_fin": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        "total_offres": total_offres,
        "total_offres_collecte": len(export_json),
        "duree_totale": duree_totale
    }
    
    print(f"\n{ingestion_data}\n")