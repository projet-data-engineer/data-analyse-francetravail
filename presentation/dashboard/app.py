import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table, dash
import sys
sys.path.append('..')
from db import Db


_db = Db()

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)



app.layout = [
    html.Div(children='My First App with Data'),
    #dash_table.DataTable(data=_db.get_nb_offre_famille_metier().to_dict('records'), page_size=100),
    dbc.Table.from_dataframe(_db.get_nb_offre_famille_metier(), striped=True, bordered=True, hover=True)

    
]

if __name__ == "__main__":
    app.run_server()