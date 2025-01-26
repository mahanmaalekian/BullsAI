import dash
from dash import html, dcc
from flask import Flask, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import os

# Flask server
server = Flask(__name__)
server.secret_key = os.environ.get("APP_SECRET_KEY", "your-secret-key")

# Dash app
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    use_pages=True,  # Enable multipage support
)
app.title = "Auth0 Dash App"

# Auth0 configuration
auth0_domain = os.environ.get("AUTH0_DOMAIN", "your-auth0-domain")
auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "your-client-id")
auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "your-client-secret")

oauth = OAuth(server)
auth0 = oauth.register(
    "auth0",
    client_id=auth0_client_id,
    client_secret=auth0_client_secret,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{auth0_domain}/.well-known/openid-configuration",
)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        id="hidden-shit",
        children=[
            html.A("Home", href="/"),
            html.A("About", href="/about"),
            html.A("Graphing", href="/graphing"),
            html.A("Login", href="/login"),
            html.A("Logout", href="/logout"),
        ]
    ),
    html.Div(id="user-info", children=[]),  # Display user-specific information
    dash.page_container  # This renders the appropriate page based on the URL
])

# Flask routes for authentication
@server.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@server.route("/callback")
def callback():
    token = auth0.authorize_access_token()
    session["user"] = token["userinfo"]
    return redirect("/")  # Redirect to the Dash app home page

@server.route("/logout")
def logout():
    session.clear()
    return redirect(f"https://{auth0_domain}/v2/logout?client_id={auth0_client_id}&returnTo=http://localhost:8050")

# Dash callback to display user info
@app.callback(
    dash.Output("user-info", "children"),
    [dash.Input("url", "pathname")]
)
def display_user_info(pathname):
    user = session.get("user")
    if user:
        return html.Div([
            html.P(f"Logged in as: {user['name']}"),
            html.P(f"Email: {user['email']}"),
        ])
    else:
        return html.P("You are not logged in. Please log in to access the app.")

if __name__ == "__main__":
    app.run_server(debug=False)
