import dash
import dash_bootstrap_components as dbc
from dash import html
import requests
import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input,Output
from dash import dash_table
import gspread
import gspread_dataframe as gd
import base64
import json
import io
import os


app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)

# Credenciais de planilhas
conteudo_codificado = os.environ["GOOGLE_SHEET_CREDENTIALS1"]
conteudo = base64.b64decode(conteudo_codificado)
credentials = json.loads(conteudo)
gc = gspread.service_account_from_dict(credentials)

# Acesso dados da Câmara
ws = gc.open('proposicoes_jornalismo_camara').worksheet("Página1")

data = ws.get_all_values()
headers = data.pop(0)
df_camara = pd.DataFrame(data, columns=headers)
df_camara = df_camara.drop_duplicates(['id'], keep='last')

conta_tipos = df_camara.groupby(['tema_principal'])['id'].count().sort_values(ascending=False).reset_index()
conta_tipos.columns = ['tema_principal', 'total_de_proposicoes']

figura1 = go.Figure([go.Bar(x = conta_tipos['tema_principal'], y = conta_tipos['total_de_proposicoes'], marker_color = 'darkgoldenrod')])

figura1.update_layout(title = 'Total de tipos de proposições em tramitação na Câmara',
                  xaxis_title = 'Temas principais das proposições',
                  yaxis_title = 'Total encontradas'
                  )

# Senado
ws = gc.open('proposicoes_jornalismo_senado').worksheet("Página1")

data = ws.get_all_values()
headers = data.pop(0)
df_senado = pd.DataFrame(data, columns=headers)
df_senado = df_senado.drop_duplicates(['CodigoMateria'], keep='last')

conta_tiposs = df_senado.groupby(['tema_principal'])['CodigoMateria'].count().sort_values(ascending=False).reset_index()
conta_tiposs.columns = ['tema_principal', 'total_de_proposicoes']

figura2 = go.Figure([go.Bar(x = conta_tiposs['tema_principal'], y = conta_tiposs['total_de_proposicoes'], marker_color = 'chartreuse')])

figura2.update_layout(title = 'Total de tipos de proposições em tramitação no Senado',
                  xaxis_title = 'Temas principais das proposições',
                  yaxis_title = 'Total encontradas'
                  )


app.title = 'Proposições de interesse do jornalismo que tramitam no Congresso'
server = app.server

PLOTLY_LOGO = "https://www.portaldosjornalistas.com.br/wp-content/uploads/2019/09/Abraji.png"


navbar = dbc.Navbar(
        [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = PLOTLY_LOGO, height = "70px"), ),
                        
                        dbc.Col(
             dbc.NavbarBrand("Proposições de interesse do jornalismo que tramitam no Congresso - versão beta", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
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
            
     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)
            
         ],
)

html.Br()
html.Br()

body_app = dbc.Container([
             
        dbc.Row( html.Marquee("As informações sobre proposições na Câmara e no Senado são buscadas todo dia às 17h nas respectivas APIs. Se nas ementas existem palavras-chave de interesse são alterados as planilhas e gráficos do projeto"), style = {'color':'green'}),
        
        html.Br(),
        html.Br(),
        
        dbc.Row([html.Div(html.H4('Como o Legislativo federal tem debatido temas de interesse do jornalismo em termos de proposições - ano de 2022'),
                      style = {'textAlign':'center','fontWeight':'bold','family':'georgia','width':'100%'})]),

        html.Br(),
        html.Br(),
        
        dbc.Row([dbc.Col(dcc.Graph(id = 'graph-camara', figure = figura1), style = {'height':'450px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6),
                 dbc.Col(dcc.Graph(id = 'graph-senado', figure = figura2), style = {'height':'450px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6)
             ]),
  
        html.Br(),
        html.Br(),
        html.Br(),
  
        dbc.Row([html.Div([
            html.P('Veja neste link a planilha de proposições do Senado (https://docs.google.com/spreadsheets/d/1uewesjTrM4nr1BU5Jsg5yySNH1kqJ27VvlIA7EixZ1o/edit?usp=sharing). Veja neste link a planilha de proposições da Câmara (https://docs.google.com/spreadsheets/d/1n1PeVA3wjtoP0_gbX-y6KJHrGoM4CyQIpKpmDjcqfgo/edit?usp=sharing)')         
        ])
        ]),
  
        html.Br(),
  
        dbc.Row([html.Div([
            html.P('No momento eu procuro estas palavras-chave JORNALISMO, JORNALISTA, JORNALISTAS, COMUNICADORES, IMPRENSA, VERIFICADORES DE FATOS, CHECAGEM DE FATOS, FAKE NEWS, DESINFORMAÇÃO, TRANSPARÊNCIA NA INTERNET, RADIODIFUSÃO, LIBERDADE DE EXPRESSÃO E INFORMAÇÕES DE INTERESSE COLETIVO.')         
        ])
        ]),
  
        html.Br(),
  
        dbc.Row([html.Div([
            html.P("E também receba notificações por Telegram de novas proposições e outros projetos da Abraji - digite '/start' no robô da Abraji:"),
            dcc.Link(html.A('@abrajibot'), href="https://telegram.me/abrajibot")
        ])
        ]), 
  
        html.Br(),
  
        dbc.Row([html.Div([
            html.P("Para mais detalhes e dúvidas escreva: "), dcc.Link(html.A('reinaldo@abraji.org.br'), href="reinaldo@abraji.org.br")
        ])
        ])
  

         ],fluid = True)



app.layout = html.Div(id = 'parent', children = [navbar, body_app])


if __name__ == "__main__":
    app.run_server()
