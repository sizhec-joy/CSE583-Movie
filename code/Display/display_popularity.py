import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
import grab_list
from app import app
import display_final_movie
import global_record
from Simple_Recommender import simple_recommendation
import pickle

file = open('sp.txt','rb')
sp = pickle.load(file)


num_movie_rate = 8
num_final_recommend = 10

colors = {
    'background': '#111111',
    'text': '#000080'
}

filter_options = ['Genre', 'Year', 'Country', 'Director', 'Actors']

year_val = []
year_val.extend([{'label': str(i), 'value': i} for i in np.arange(1900, 2017, 1)])

grab_list.read_csv()
genre_set = sorted(grab_list.genre_set)
country_set = sorted(grab_list.country_set)
director_set = sorted(grab_list.director_set)
actor_set = sorted(grab_list.actor_set)
id_set = sorted(grab_list.id_set)
id_title_set = (grab_list.id_title_set)

genre_val = []
country_val = []
director_val = []
actor_val = []
for val in genre_set:
    genre_val.append({'label': val, 'value': val})
for val in country_set:
    country_val.append({'label': val, 'value': val})
count = 0
for val in director_set:
    count = count + 1
    if count > grab_list.max_count:
        break
    director_val.append({'label': val, 'value': val})
count = 0
for val in actor_set:
    count = count + 1
    if count > grab_list.max_count:
        break
    actor_val.append({'label': val, 'value': val})


'''
def set_genre_set(set):
    genre_set = set
    print(genre_set)
'''
def get_option(f):
    if f == 'Genre':
        return genre_val
    elif f == 'Country':
        return country_val
    elif f == 'Director':
        return director_val
    elif f == 'Actors':
        return actor_val
    else:
        return year_val

def add_popularity_filter():
    movie_div = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                         global_record.initial_movie_id_list[10:(10+num_final_recommend)]))
    filter_drop_down = []
    for f in filter_options:
        filter_drop_down.append(html.Div(
            children=[
                html.Div("Please Select a {}".format(f),
                         style={'text-align': 'center',
                                'font-size': '12px'}),
                dcc.Dropdown(
                    id=f,
                    options=get_option(f),
                    value="All",
                    # multi=True,
                    placeholder="Please select a " + str(f))],
            style={
                'width': '15%',
                'margin-left': '4%',
                # 'padding-left': '10%',
                # 'padding-right': '10%',
                'display': 'inline-block',
                'color': colors['text']}))

    app_popularity_tab = html.Div(children=[])
    app_popularity_tab.children.append(html.Div(filter_drop_down, style={'margin-top': '50px'}))
    filter_button_div = html.Div(html.Button(id='popularity_filter_button', children='Filter'),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '100px',
                                        'width': '40%',
                                        'padding-left': '45%',
                                        'padding-right': '15%'})
    app_popularity_tab.children.append(filter_button_div)
    app_popularity_tab.children.append(html.Div("List of movies:"))
    app_popularity_tab.children.append(html.Div(id='popularity_main_div', children=movie_div))
    return app_popularity_tab


def call_back_popularity_filter():
    list_state = [State(f'{f}', 'value') for f in filter_options]
    @app.callback(
        Output('popularity_main_div', 'children'),
        [Input('popularity_filter_button', 'n_clicks')],
        list_state)
    def update_multi_output(n_clicks, *input_value):
        ctx = dash.callback_context
        if not ctx.triggered:
            user_click = 'No clicks yet'
        else:
            user_click = ctx.triggered[0]['prop_id'].split('.')[0]
        if n_clicks is not None and n_clicks > 0:
            list_filter = list(input_value)
            print(list_filter)
            for i in range(len(list_filter)):
                if list_filter[i] == "All":
                    list_filter[i] = None
            print(list_filter)
            recommend = sp.get_recommended_movies(list_filter)
            print(recommend)
            movie_names = recommend['title'].values.tolist()
            print(movie_names)
            list_next_movie_id = []
            for mn in movie_names:
                print(mn)
                print(id_title_set[mn])
                list_next_movie_id.append(id_title_set[mn])
            print(list_next_movie_id)
            ls = []
            for ids in list_next_movie_id:
                if ids in id_set:
                    ls.append(ids)
            # TODO: call backend to filter here (param is a list: 'Genre', 'Year', 'Country', 'Director', 'Actors')
            #list_next_movie_id = [862 if r == 2000 else 2 for r in list_filter]
            list_next_movie_id = ls
            print(list_next_movie_id)
            result = display_final_movie.add_final_movies(zip(range(len(list_next_movie_id)), list_next_movie_id))
            return result
        else:
            raise PreventUpdate


def main():
    return add_popularity_filter()


if __name__ == "__main__":
    main()
