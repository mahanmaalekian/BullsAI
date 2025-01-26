import dash
from dash import html, dcc

dash.register_page(__name__, path="/")  # Register as the home page

def layout():
    return html.Div([
        html.H1("Welcome to the Auth0 Dash App", style={"textAlign": "center"}),
        html.P("This is the home page of your application.", style={"textAlign": "center"}),
        
        html.Div(
            [
                html.A("About Page", href="/about", style={"marginRight": "15px"}),
                html.A("Graphing Page", href="/graphing", style={"marginRight": "15px"}),
                html.A("Login", href="/login", style={"marginRight": "15px"}),
                html.A("Logout", href="/logout"),
            ],
            style={"textAlign": "center", "marginTop": "20px"},
        ),

        html.Div(id="user-info", style={"marginTop": "20px", "textAlign": "center"}),
    ])
