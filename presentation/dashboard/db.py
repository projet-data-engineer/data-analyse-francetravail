import duckdb
import pandas as pd
from contextlib import contextmanager
import pandas as pd

class Db:

    """ Classe en charge de requêter l'entrepôt DuckDB"""

    @contextmanager
    def _connect(self):

        con = None
        try:
            con = duckdb.connect(
                database="../../stockage/entrepot.duckdb",
                read_only=True,
                config={"access_mode": "READ_ONLY"},
            )
            yield con
        finally:
            if con:
                con.close()
    
    def get_nb_offre_famille_metier(self) -> pd.DataFrame:

        query = f"""

            SELECT
                rome.code_1 AS code, 
                rome.libelle_1 AS libelle,
                COUNT(*) AS nombre
            FROM
                entrepot.emploi.fait_offre_emploi AS offre
            JOIN
                entrepot.emploi.dim_rome AS rome 
            ON
                offre.code_rome = rome.code_3
            GROUP BY 
                rome.code_1,rome.libelle_1
            ORDER BY
                COUNT(*) DESC 

        """

        with self._connect() as con:
            con.execute(query)
            data = con.cursor().execute(query).df()

        return data