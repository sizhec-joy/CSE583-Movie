import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import get_movie_info
from app import app
from dash.dependencies import Input, Output, State

colors = {
    'background': '#111111',
    'text': '#000000'
}
num_movie_rate = 8
num_final_recommend = 10


def get_info(item_json):
    name = item_json[get_movie_info.MovieJsonKeys.name]
    poster = get_movie_info.poster_url_constant + item_json[get_movie_info.MovieJsonKeys.poster_url]
    overview = item_json[get_movie_info.MovieJsonKeys.overview]
    vote_average = item_json[get_movie_info.MovieJsonKeys.vote_average]
    list_genres = item_json[get_movie_info.MovieJsonKeys.genres]
    if len(list_genres) > 5:
        genres1 = ', '.join([elem['name'] for elem in list_genres[:4]]) + ','
        genres2 = ', '.join([elem['name'] for elem in list_genres[4:]])
        genres_div = html.Div(children=[
            html.Div(children='Genres:', className='alignleft'),
            html.Div(children=f'{genres1}', className='alignright'),
            html.Div(children=f'{genres2}', className='alignright')],
            style={'clear': 'both'})
    else:
        genres = ', '.join([elem['name'] for elem in list_genres])
        genres_div = html.Div(children=[
            html.Div(children='Genres:', className='alignleft'),
            html.Div(children=f'{genres}', className='alignright')],
            style={'clear': 'both'})
    release_date = item_json[get_movie_info.MovieJsonKeys.release_date]
    popularity = item_json[get_movie_info.MovieJsonKeys.popularity]
    runtime = item_json[get_movie_info.MovieJsonKeys.runtime]
    return name, poster, overview, vote_average, release_date, runtime, popularity, genres_div


def add_final_movies(zipped_list):
    result = []
    for item in zipped_list:
        item_index = item[0]
        item_movie_id = item[1]
        item_json = get_movie_info.get_movie_json(item_movie_id)
        try:
            name, poster, overview, vote_average, release_date, runtime, popularity, genres_div = get_info(item_json)
        except (TypeError, KeyError):
            continue
        result.append(
            html.Div([
                html.Div(
                    id='movie_title_{}'.format(item_index),
                    children=name,
                    style={
                        'font-size': '15px',
                        'margin': '5px',
                        'textAlign': 'center',
                        'color': colors['text']}),
                html.Div(
                    className='container',
                    children=[html.Img(className='image',
                                       id='image_{}'.format(item_index),
                                       src=poster,
                                       style={'height': '410px'}),
                              html.Div(className='middle',
                                       children=html.Div(
                                           className='text',
                                           children=f'Movie overview: {overview}',
                                           style={'font-size': '13px'}),
                                       style={'transform': 'translate(-2.5%, -100%)'})]),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children='Average vote:', className='alignleft'),
                        html.Div(f'{vote_average}', className='alignright')],
                        style={'clear': 'both'}),
                    genres_div,
                    html.Div(children=[
                        html.Div(children='Release Date: ', className='alignleft'),
                        html.Div(children=f'{release_date}', className='alignright')],
                        style={'clear': 'both'}),
                    html.Div(children=[
                        html.Div(children='Popularity: ', className='alignleft'),
                        html.Div(children=f'{popularity}', className='alignright')],
                        style={'clear': 'both'}),
                    html.Div(children=[
                        html.Div(children='Runtime: ', className='alignleft'),
                        html.Div(children=f'{runtime}', className='alignright')],
                        style={'clear': 'both'})],
                    style={'width': '90%',
                           'margin-left': '5%',
                           'margin-right': '5%'}
                )
        ], style={'margin': '15px', 'margin-top': '80px', 'width': '30%', 'display': 'inline-block'}))
    return result
