import dash
import dash_bootstrap_components as dbc
from dash import html
import requests
import pandas as pd
from dash import dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from dash import dash_table

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)

app.title = 'Proposições de interesse do jornalismo que tramitam no Congresso'
server = app.server

PLOTLY_LOGO = "https://www.portaldosjornalistas.com.br/wp-content/uploads/2019/09/Abraji.png"


navbar = dbc.Navbar(
        [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = PLOTLY_LOGO, height = "70px"), ),
                        
                        dbc.Col(
             dbc.NavbarBrand("Proposições de interesse do jornalismo que tramitam no Congresso", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            ),
             ),

                    ],
                    align="center",
                    className="g-10",
                ),
            
            dbc.Row(
            [
        dbc.Col(
        dbc.Button(id = 'button', children = "Conheça a Abraji", color = "primary",  href = 'https://www.abraji.org.br/'), 
            )        
    ],
            # add a top margin to make things look nice when the navbar
            # isn't expanded (mt-3) remove the margin on medium or
            # larger screens (mt-md-0) when the navbar is expanded.
            # keep button and search box on same row (flex-nowrap).
            # align everything on the right with left margin (ms-auto).
     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)
            
         ],
)


app.layout = html.Div(id = 'parent', children = [navbar])


if __name__ == "__main__":
    app.run_server()
