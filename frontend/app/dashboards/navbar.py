from dash import html
import dash_bootstrap_components as dbc

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    html.Img(src="/static/img/logo.png", height="30px"),
                    href="/dashboard/",
                    className="ms-2",
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink([html.Img(src="/static/img/home-icon.svg", height="20px", className="me-2 d-none d-md-inline"), "Inicio"], href="/dashboard/", id="navbar-home")),
                            dbc.NavItem(dbc.NavLink([html.Img(src="/static/img/user-icon.svg", height="20px", className="me-2 d-none d-md-inline"), "Mi Cuenta"], href="#", id="navbar-account")),
                            dbc.NavItem(dbc.NavLink([html.Img(src="/static/img/exit-icon.svg", height="20px", className="me-2 d-none d-md-inline"), "Salir"], href="/auth/logout", id="navbar-logout", external_link=True)),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color="white",
        light=True,
        className="border-bottom border-light shadow-sm",
        expand="md",
    )