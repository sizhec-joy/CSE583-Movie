import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
from Content import content_recommendation
from app import app
import display_final_movie
import global_record
import grab_list
import pickle

num_movie_rate = 8
num_final_recommend = 10
test = True

file = open('cp.txt','rb')
cp = pickle.load(file)
print('computing similarity')
if test:
    cp.generate_cosine_sim()

colors = {
    'background': '#111111',
    'text': '#000080'
}

ob = grab_list.read_csv()
name_set = ob.name_set
id_set = ob.id_set
id_title_set = ob.id_title_set
name_val = []
count = 0
for val in name_set:
    count = count + 1
    if count > grab_list.max_count:
        break
    name_val.append({'label': val, 'value': val})
#year_val = [{'label': 'All', 'value': 'All'}]
#year_val.extend([{'label': str(i), 'value': i} for i in np.arange(1970, 2017, 1)])
#year_val = []
#year_val.extend([{'label': str(i), 'value': i} for i in np.arange(1900, 2017, 1)])


def add_search_bar():
    movie_div = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                         global_record.initial_movie_id_list[10:(10+num_final_recommend)]))
    search_bar = html.Div(
        children=[
            html.Div(children='Please type a movie',
                     style={'text-align': 'center',
                            'font-size': '16px',
                            'margin-bottom': '20px'}),
            html.Div(dcc.Dropdown(
                id='movie_search_dropdown',
                options=name_val,
                # multi=True,
                placeholder="Please select/type a movie"))
        ]
    )
    app_filter_tab = html.Div(children=[])
    app_filter_tab.children.append(html.Div(search_bar, style={'margin-top': '50px'}))
    search_button_div = html.Div(html.Button(id='search_similar_button', children='Find Similar Movies'),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '100px',
                                        'width': '40%',
                                        'margin-left': '30%',
                                        'text-align': 'center'})
    app_filter_tab.children.append(search_button_div)
    app_filter_tab.children.append(html.Div("List of movies:"))
    app_filter_tab.children.append(html.Div(id='content_base_main_div', children=movie_div))
    return app_filter_tab


def call_back_filter():
    list_state = [State('movie_search_dropdown', 'value')]
    @app.callback(
        Output('content_base_main_div', 'children'),
        [Input('search_similar_button', 'n_clicks')],
        list_state)
    def update_multi_output(n_clicks, *input_value):
        ctx = dash.callback_context
        if not ctx.triggered:
            user_click = 'No clicks yet'
        else:
            user_click = ctx.triggered[0]['prop_id'].split('.')[0]
        if n_clicks is not None and n_clicks > 0:
            list_filter = str(list(input_value)[0])
            print(list_filter)
            recommend = cp.get_recommended_movies(list_filter)
            #print(recommend)
            movie_names = recommend['title'].values.tolist()
            #print(movie_names)
            list_next_movie_id = []
            for mn in movie_names:
                #print(mn)
                #print(id_title_set[mn])
                if mn in id_title_set:
                    list_next_movie_id.append(int(id_title_set[mn]))
            #print(list_next_movie_id)
            ls = []
            for ids in list_next_movie_id:
                if ids in id_set:
                    ls.append(ids)
            #list_next_movie_id = [862 if r == 2000 else 2 for r in list_filter]
            list_next_movie_id = ls
            print(list_next_movie_id)
            result = display_final_movie.add_final_movies(zip(range(len(list_next_movie_id)), list_next_movie_id))
            return result
        else:
            raise PreventUpdate


def main():
    return add_search_bar()


if __name__ == '__main__':
    main()
