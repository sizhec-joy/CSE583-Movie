import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import get_movie_info

colors = {
    'background': '#111111',
    'text': '#000080'
}
num_movie_rate = 8
num_final_recommend = 10


def add_final_movies(zipped_list):
    result = [html.Div("List of movies recommended:")]
    for item in zipped_list:
        item_index = item[0]
        item_movie_id = item[1]
        item_json = get_movie_info.get_movie_json(item_movie_id)

        name = item_json[get_movie_info.MovieJsonKeys.name]
        poster = get_movie_info.poster_url_constant + item_json[get_movie_info.MovieJsonKeys.poster_url]
        overview = item_json[get_movie_info.MovieJsonKeys.overview]
        vote_average = item_json[get_movie_info.MovieJsonKeys.vote_average]
        genres = ', '.join([elem['name'] for elem in item_json[get_movie_info.MovieJsonKeys.genres]])
        homepage = item_json[get_movie_info.MovieJsonKeys.homepage]
        if homepage is None:
            homepage_div = html.Div('Homepage: N/A')
        else:
            homepage_div = html.Div(['Homepage: ',
                                     html.A(children=homepage,
                                            href=homepage,
                                            style={'color': 'white'})])
        release_date = item_json[get_movie_info.MovieJsonKeys.release_date]
        popularity = item_json[get_movie_info.MovieJsonKeys.popularity]
        runtime = item_json[get_movie_info.MovieJsonKeys.runtime]

        result.append(
            html.Div([
                html.Div(
                    id='movie_title_{}'.format(item_index),
                    children=name,
                    style={
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
                                           style={'font-size': '12px'}),
                                       style={'transform': 'translate(-2.5%, -100%)'})]),
                html.Details(children=[html.Summary(children='Movie Detail'),
                                       html.Div(children=[
                                           html.Div(children=f'Average vote: {vote_average}'),
                                           html.Div(children=f'Genres: {genres}'),
                                           homepage_div,
                                           html.Div(children=f'Release Date: {release_date}'),
                                           html.Div(children=f'Popularity: {popularity}'),
                                           html.Div(children=f'Runtime: {runtime}')],
                                           style={'white-space': 'pre-line',
                                                  'background-color': '#2B60DE',
                                                  'color': 'white',
                                                  'padding': '2px 6px',
                                                  'margin-left': '10%'}
                                       )])
            ], style={'margin': '15px', 'width': '30%', 'display': 'inline-block'})
        )
    for i in range(num_movie_rate):
        result.append(
            dcc.Dropdown(
                id='rating_{}'.format(i),
                options=[{'label': str(i), 'value': i} for i in np.arange(0, 5.5, 0.5)],
                placeholder="Please select a rating",
                style={'display': 'none'}))
    return result

