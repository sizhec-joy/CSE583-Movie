'''
this is a display module
'''
from ast import literal_eval
from collections import defaultdict
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
from app import APP
import global_record
import grab_list
import display_final_movie

COLORS = {
    'background': '#111111',
    'text': '#000080'
}
num_final_recommend = 10
COP = defaultdict(list)
df = pd.read_csv('../movies-dataset/source/collaborative_result.csv',
                 header=None, index_col=0, converters={1: literal_eval})
for row in df.iterrows():
    # print([item for item in row[1][0]])
    tmp_list = list(row[1])
    COP[int(row[0])] = [item[0] for item in tmp_list[0]]

obs = grab_list.read_csv()
id_set = obs.id_set
id_title_set = obs.id_title_set


user_val = []
user_val.extend([{'label': str(i), 'value': i} for i in np.arange(1, 467, 1)])


def main():
    '''
    this is the main function
    '''
    movie_div = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                         global_record.initial_movie_id_list[10:(10+num_final_recommend)]))
    global_record.set_curr_movie_id_list(global_record.initial_movie_id_list)
    search_bar = html.Div(
        children=[
            html.Div(children='Please type a user ID',
                     style={'text-align': 'center',
                            'font-size': '16px',
                            'margin-bottom': '20px'}),
            html.Div(dcc.Input(
                id='user_id_dropdown'.format(),
                type='number',
                placeholder="Please enter a user id",
                style={'font-size': '13px',
                       'width': '100%'}
            ))
        ]
    )
    search_button_div = html.Div(html.Button(id='user_id_button',
                                             children='Find User',
                                             style={'font-size': '13px'}),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '20px',
                                        'width': '40%',
                                        'margin-left': '30%',
                                        'text-align': 'center'})
    app_recommender_tab = html.Div(children=[])
    app_recommender_tab.children.append(html.Div(html.H1('User-based Filtering'),
                                                 className='wrap'))
    app_recommender_tab.children.append(html.Div(search_bar, style={'margin-top': '15px'}))
    app_recommender_tab.children.append(search_button_div)
    app_recommender_tab.children.append(html.Div(id='recommend_main_div', children=movie_div))
    return app_recommender_tab


def call_back_recom():
    '''
    this is the call back function
    '''
    list_state = [State('user_id_dropdown', 'value')]

    @APP.callback(
        Output('recommend_main_div', 'children'),
        [Input('user_id_button', 'n_clicks')],
        list_state)
    def update_multi_output(n_clicks, *input_value):
        ctx = dash.callback_context
        if not ctx.triggered:
            user_click = 'No clicks yet'
        else:
            user_click = ctx.triggered[0]['prop_id'].split('.')[0]
        if n_clicks is not None and n_clicks > 0:
            list_filter = list(input_value)
            user_id = int(list_filter[0])
            print(user_id)
            list_next_movie_id = []
            movie_names = COP[user_id]
            # movie_names = COP.user_recommendation_dic[user_id]
            for mn in movie_names:
                print(mn)
                if mn in id_title_set:
                #print(id_title_set[mn])
                    list_next_movie_id.append(int(id_title_set[mn]))
            print(list_next_movie_id)
            ls = []
            for ids in list_next_movie_id:
                if ids in id_set:
                    ls.append(ids)
            list_next_movie_id = ls
            num_movie_rate = len(list_next_movie_id)
            print(list_next_movie_id)
            result = display_final_movie.add_final_movies(zip(range(num_movie_rate), list_next_movie_id))
            return result
        else:
            raise PreventUpdate


if __name__ == '__main__':
    main()
