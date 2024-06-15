import duckdb
import pandas as pd
from contextlib import contextmanager

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

    def get_dim_rome(self):

        query = f"""

            SELECT
                *
            FROM
                emploi.dim_rome
            ORDER BY
                code_3

        """

        with self._connect() as con:
            con.execute(query)
            data = con.cursor().execute(query).df().to_dict('records')

        return data