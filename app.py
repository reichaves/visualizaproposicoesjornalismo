import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
import dash_table

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)

PLOTLY_LOGO = "https://www.portaldosjornalistas.com.br/wp-content/uploads/2019/09/Abraji.png"


navbar = dbc.Navbar(
        [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = PLOTLY_LOGO, height = "70px"), ),
                        
                        dbc.Col(
             dbc.NavbarBrand("App Title", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            ),
             ),

                    ],
                    align="center",
                    className="g-10",
                ),
            
            dbc.Row(
            [
        dbc.Col(
        dbc.Button(id = 'button', children = "Click Me!", color = "primary"), 
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