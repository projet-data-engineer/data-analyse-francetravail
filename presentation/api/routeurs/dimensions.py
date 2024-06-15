from fastapi import APIRouter
import sys
sys.path.append('..')
from commun.db import Db
from commun.models import Rome

router = APIRouter()

_db = Db()

@router.get("/rome/", tags=["Dimensions"])
async def get_dim_rome() -> list[Rome]:
    return _db.get_dim_rome()
