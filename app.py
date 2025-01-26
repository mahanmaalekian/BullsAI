from dash import Dash, html, dcc, page_registry, page_container

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        id="hidden-shit",
        children=
        [
        html.A(href="/", children=[
        ]),

        html.A("About", href="/about"),
        html.A("Graphing", href="/graphing"),
    ]),
    page_container  # This renders the appropriate page based on the URL.
])

if __name__ == "__main__":
    app.run_server(debug=True)