from fastapi import FastAPI
from routeurs import dimensions

api = FastAPI(
    title='API Entrepôt emploi',
    description="Analyse des offres d'emploi de France Travail",
    version="1.0.1",
    openapi_tags=[
        {
            "name": "Dimensions",
            "description": "Table de dimensions de l'entrepôt de données"
        }
    ]
)

api.include_router(dimensions.router)