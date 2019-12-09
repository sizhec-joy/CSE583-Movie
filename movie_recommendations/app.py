"""
This file initialize a dash app
"""
import dash
import dash_bootstrap_components as dbc

EXTERNAL_STYLESHEETS = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP]

APP = dash.Dash(__name__,
                external_stylesheets=EXTERNAL_STYLESHEETS)

SERVER = APP.server
APP.config['suppress_callback_exceptions'] = True

APP.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
