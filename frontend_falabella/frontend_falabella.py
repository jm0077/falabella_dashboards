from flask import Flask, render_template
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objs as go

# Configurar Flask
server = Flask(__name__)

# Ruta principal para renderizar la página HTML
@server.route('/')
def index():
    return render_template('index.html')

# Configurar Dash dentro de Flask
app = Dash(
    __name__, 
    server=server, 
    routes_pathname_prefix='/dashboard/',  
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap']
)

# Definir el layout de la aplicación Dash con estilos mejorados
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Pago Total del Último Periodo:", className="text-right", style={'font-family': 'Montserrat', 'font-weight': '600'}), width=6),
        dbc.Col(html.H2(id='pago-total-mes', className="text-left text-primary", style={'font-family': 'Montserrat', 'font-weight': '600'}), width=6)
    ], align='center'), 
    dbc.Row([
        dbc.Col(html.H2("Movimientos del último periodo", className="text-center", style={'font-family': 'Montserrat', 'font-weight': '600'}), width=12),
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='movimientos-table',
            style_cell={
                'font-family': 'Montserrat',
                'font-weight': '400',
                'textAlign': 'center',
                'padding': '5px',
            },
            style_header={
                'fontWeight': '600',
                'backgroundColor': 'rgb(230, 230, 230)',
                'color': 'black'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Total (S/)'},
                    'fontWeight': 'bold',
                    'color': 'red'
                }
            ],
            style_as_list_view=True
        ), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.H2("Facturación de los últimos 12 periodos", className="text-center", style={'font-family': 'Montserrat', 'font-weight': '600'}))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='consumption-graph'), width=12)
    ])
], fluid=True)

# Callback para actualizar el pago total y movimientos del último periodo
@app.callback(
    [Output('pago-total-mes', 'children'),
     Output('movimientos-table', 'data'),
     Output('movimientos-table', 'columns')],
    Input('pago-total-mes', 'id')
)
def update_latest_period(_):
    try:
        response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/latest-period-data")
        response.raise_for_status()
        data = response.json()

        pago_total_mes = f"S/. {data['pago_total_mes']:.2f}"
        movimientos = data['movimientos']

        for mov in movimientos:
            mov['fecha_transaccion'] = pd.to_datetime(mov['fecha_transaccion']).strftime('%Y-%m-%d')
            mov['fecha_proceso'] = pd.to_datetime(mov['fecha_proceso']).strftime('%Y-%m-%d')

        columns = [
            {"name": "Fecha de transacción", "id": "fecha_transaccion"},
            {"name": "Fecha de proceso", "id": "fecha_proceso"},
            {"name": "Detalle", "id": "detalle"},
            {"name": "Monto (S/)", "id": "monto"},
            {"name": "Cuota cargada", "id": "cuota_cargada"},
            {"name": "% TEA", "id": "porcentaje_tea"},
            {"name": "Capital (S/)", "id": "capital"},
            {"name": "Interés (S/)", "id": "interes"},
            {"name": "Total (S/)", "id": "total"}
        ]

        return pago_total_mes, movimientos, columns

    except requests.exceptions.RequestException as e:
        return "Error al cargar datos", [], []

# Callback para actualizar el gráfico de consumo por periodo
@app.callback(
    Output('consumption-graph', 'figure'),
    Input('consumption-graph', 'id')
)
def update_graph(_):
    try:
        response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/consumption-data")
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)

        figure = go.Figure(data=[
            go.Bar(x=df['periodo'], y=df['pago_total_mes'], marker_color='rgb(58, 123, 213)')
        ])

        figure.update_layout(
            xaxis_title="Periodo de Facturación",
            yaxis_title="Pago Total (S/)",
            font=dict(family="Montserrat", size=14),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=40, b=40),
            height=400
        )

        return figure

    except requests.exceptions.RequestException as e:
        return go.Figure()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
