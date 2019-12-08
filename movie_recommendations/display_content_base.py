import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from content_based import ContentRecommendation
from app import app
import display_final_movie
import global_record
import grab_list


NUM_MOVIE_RATE = 8
NUM_FINAL_RECOMMEND = 10
TEST = True

FILE = open('cp.txt', 'rb')
CP = pickle.load(FILE)
print('computing similarity')
if TEST:
    CP.generate_cosine_sim()

COLORS = {
    'background': '#111111',
    'text': '#000080'
}

OB = grab_list.read_csv()
NAME_SET = OB.NAME_SET
ID_SET = OB.ID_SET
ID_TITLE_SET = OB.ID_TITLE_SET
NAME_VAL = []
count = 0
for val in NAME_SET:
    count = count + 1
    if count > grab_list.max_count:
        break
    NAME_VAL.append({'label': val, 'value': val})
#year_val = [{'label': 'All', 'value': 'All'}]
#year_val.extend([{'label': str(i), 'value': i} for i in np.arange(1970, 2017, 1)])
#year_val = []
#year_val.extend([{'label': str(i), 'value': i} for i in np.arange(1900, 2017, 1)])


def add_search_bar():
    movie_div = display_final_movie.add_final_movies(zip(range(NUM_FINAL_RECOMMEND),
                                                         global_record.initial_movie_id_list[10:(10+NUM_FINAL_RECOMMEND)]))
    search_bar = html.Div(
        children=[
            html.Div(children='Please type a movie',
                     style={'text-align': 'center',
                            'font-size': '16px',
                            'margin-bottom': '20px'}),
            html.Div(dcc.Dropdown(
                id='movie_search_dropdown',
                options=NAME_VAL,
                # multi=True,
                placeholder="Please select/type a movie"),
                     style={'text-align': 'center', 'font-size': '16px'})
        ]
    )
    app_filter_tab = html.Div(children=[])
    app_filter_tab.children.append(html.Div(html.H1('Content-based Filtering'),
                                            className='wrap'))
    app_filter_tab.children.append(html.Div(search_bar, style={'margin-top': '15px'}))
    search_button_div = html.Div(html.Button(id='search_similar_button',
                                             children='Find Similar Movies',
                                             style={'font-size': '13px'}),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '20px',
                                        'width': '40%',
                                        'margin-left': '30%',
                                        'text-align': 'center'})
    app_filter_tab.children.append(search_button_div)
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
            recommend = CP.get_recommended_movies(list_filter)
            #print(recommend)
            movie_names = recommend['title'].values.tolist()
            #print(movie_names)
            list_next_movie_id = []
            for mn in movie_names:
                #print(mn)
                #print(ID_TITLE_SET[mn])
                if mn in ID_TITLE_SET:
                    list_next_movie_id.append(int(ID_TITLE_SET[mn]))
            #print(list_next_movie_id)
            ls = []
            for ids in list_next_movie_id:
                if ids in ID_SET:
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
