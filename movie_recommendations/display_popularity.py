"""
This displays the simple filtering page
"""
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
import grab_list
from app import APP
import display_final_movie
import global_record
from simple_recommender import SimpleRecommendation

FILE = open('sp.txt', 'rb')
SP = pickle.load(FILE)


NUM_FINAL_RECOMMEND = 10

COLOR = {
    'background': '#111111',
    'text': '#000000'
}

FILTER_OPTIONS = ['Genre', 'Year', 'Country', 'Director', 'Actors']

YEAR_VAL = []
YEAR_VAL.extend([{'label': str(i), 'value': i} for i in np.arange(1900, 2017, 1)])

OBS = grab_list.read_csv()
GENRE_SET = OBS.genre_set
COUNTRY_SET = OBS.country_set
DIRECTOR_SET = OBS.director_set
ACTOR_SET = OBS.actor_set
ID_SET = OBS.id_set
ID_TITLE_SET = OBS.id_title_set

GENRE_VAL = []
COUNTRY_VAL = []
DIRECTOR_VAL = []
ACTOR_VAL = []
for val in GENRE_SET:
    GENRE_VAL.append({'label': val, 'value': val})
for val in COUNTRY_SET:
    COUNTRY_VAL.append({'label': val, 'value': val})
COUNT = 0
for val in DIRECTOR_SET:
    COUNT = COUNT + 1
    if COUNT > grab_list.max_count:
        break
    DIRECTOR_VAL.append({'label': val, 'value': val})
COUNT = 0
for val in ACTOR_SET:
    COUNT = COUNT + 1
    if COUNT > grab_list.max_count:
        break
    ACTOR_VAL.append({'label': val, 'value': val})


def get_option(filter_option):
    """
    get a list of all options for one of Genre, Country, Director, Actor, Year
    :param filter_option: one of Genre, Country, Director, Actor, Year
    :return: a list of all options to be picked for this particular filter_option
    """
    if filter_option == 'Genre':
        return GENRE_VAL
    elif filter_option == 'Country':
        return COUNTRY_VAL
    elif filter_option == 'Director':
        return DIRECTOR_VAL
    elif filter_option == 'Actors':
        return ACTOR_VAL
    else:
        return YEAR_VAL


def add_popularity_filter():
    """
    :return: a html div with all content to be displayed for the simple filtering,
             including, a div with drop down boxes, filter button, and movies with their info
    """
    movie_div = display_final_movie.add_final_movies(
        zip(range(NUM_FINAL_RECOMMEND),
            global_record.INITIAL_MOVIE_ID_LIST[10:(10 + NUM_FINAL_RECOMMEND)]))
    filter_drop_down = []
    for filter_option in FILTER_OPTIONS:
        filter_drop_down.append(html.Div(
            children=[
                html.Div(str(filter_option),
                         style={'text-align': 'center',
                                'font-size': '14px',
                                'margin-bottom': '20px'}),
                dcc.Dropdown(
                    id=filter_option,
                    options=get_option(filter_option),
                    value="All",
                    # multi=True,
                    style={'text-align': 'left',
                           'font-size': '12px'},
                    placeholder="Select a " + str(filter_option))],
            style={
                'width': '15%',
                'margin-left': '4%',
                # 'padding-left': '10%',
                # 'padding-right': '10%',
                'display': 'inline-block',
                'color': COLOR['text']}))

    app_popularity_tab = html.Div(children=[])
    app_popularity_tab.children.append(html.Div(html.H1('Simple Filtering'),
                                                className='wrap'))
    app_popularity_tab.children.append(html.Div(filter_drop_down, style={'margin-top': '10px'}))
    filter_button_div = html.Div(html.Button(id='popularity_filter_button',
                                             children='Filter',
                                             style={'font-size': '13px'}),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '20px',
                                        'width': '40%',
                                        'padding-left': '45%',
                                        'padding-right': '15%'})
    app_popularity_tab.children.append(filter_button_div)
    app_popularity_tab.children.append(html.Div(id='popularity_main_div', children=movie_div))
    return app_popularity_tab


def call_back_popularity_filter():
    """
    A call back function for the filter button in the html div.
    :return: a updated html div with after the filter button is clicked
    """
    list_state = [State(f'{f}', 'value') for f in FILTER_OPTIONS]
    @APP.callback(
        Output('popularity_main_div', 'children'),
        [Input('popularity_filter_button', 'n_clicks')],
        list_state)
    def update_multi_output(n_clicks, *input_value):
        if n_clicks is not None and n_clicks > 0:
            list_filter = list(input_value)
            #print(list_filter)
            for i in range(len(list_filter)):
                list_filter[i] = str(list_filter[i])
                if list_filter[i] == "All":
                    list_filter[i] = None
            #print(list_filter)
            recommend = SP.get_recommended_movies(list_filter)
            #print(recommend)
            movie_names = recommend['title'].values.tolist()
            #print(movie_names)
            list_next_movie_id = []
            for movie_name in movie_names:
                if movie_name in ID_TITLE_SET:
                    list_next_movie_id.append(int(ID_TITLE_SET[movie_name]))
            print(list_next_movie_id)
            list_movie_id = []
            for ids in list_next_movie_id:
                if ids in ID_SET:
                    list_movie_id.append(ids)
            list_next_movie_id = list_movie_id
            result = display_final_movie.add_final_movies(
                zip(range(len(list_next_movie_id)),
                    list_next_movie_id))
            return result
        else:
            raise PreventUpdate


def main():
    return add_popularity_filter()


if __name__ == "__main__":
    main()
