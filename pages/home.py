import dash
from dash import html, dcc

dash.register_page(__name__, path="/")  # Register as the home page

def layout():
    return html.Div(className="mahan", children=[
    html.Div([
        html.H1("Welcome to BullsAI", className="home-title"),
        html.P("This is the home page of your application.", className="home-subtitle"),
        
        html.Div(
            [
                html.A("About Page", href="/about", className="nav-link"),
                html.A("Graphing Page", href="/graphing", className="nav-link"),
                html.A("Login", href="/login", className="nav-link"),
                html.A("Logout", href="/logout", className="nav-link"),
            ],
            className="nav-container"
        ),

        html.Div(id="user-info", className="user-info"),
    ], className="home-container")])
