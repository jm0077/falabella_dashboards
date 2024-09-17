from dash import html
import dash_bootstrap_components as dbc

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo a la izquierda
                dbc.NavbarBrand(
                    html.Img(src="/static/img/logo.png", height="30px"),
                    href="/dashboard/",
                ),
                # Elementos de navegación a la derecha
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink([html.Img(src="/static/img/home-icon.svg", height="20px", className="me-2"), "Inicio"], href="/dashboard/", id="navbar-home")),
                        dbc.NavItem(dbc.NavLink([html.Img(src="/static/img/user-icon.svg", height="20px", className="me-2"), "Mi Cuenta"], href="#", id="navbar-account")),
                        dbc.NavItem(dbc.NavLink([html.Img(src="/static/img/exit-icon.svg", height="20px", className="me-2"), "Salir"], href="/logout", id="navbar-logout", external_link=True)),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
            ]
        ),
        color="white",
        light=True,
        className="border-bottom border-light shadow-sm",
    )