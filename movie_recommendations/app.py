import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

server = app.server
app.config['suppress_callback_exceptions'] = True

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
