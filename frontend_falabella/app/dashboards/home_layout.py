from dash import html

def create_home_layout():
    return html.Div([
        html.H1("Bienvenido a tu Centro Financiero", className="text-center mb-4"),
        html.Div([
            html.Div([
                html.A(
                    html.Img(src="https://www.bancofalabella.pe/assets/logo.svg", className="img-fluid"),
                    href="/dashboard/falabella/",
                    className="d-block"
                )
            ], className="col-md-6 text-center"),
            html.Div([
                html.A(
                    html.Img(src="https://cdn.aglty.io/scotiabank-peru/Global-Rebrand/logo.svg", className="img-fluid"),
                    href="/dashboard/scotiabank/",
                    className="d-block"
                )
            ], className="col-md-6 text-center")
        ], className="row justify-content-center")
    ], className="container mt-5")