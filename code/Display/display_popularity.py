import dash_html_components as html
import display_final_movie
import global_record


num_movie_rate = 8
num_final_recommend = 10


def main():
    movie_div = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                         global_record.initial_movie_id_list[10:(10+num_final_recommend)]))
    app_popularity_tab = html.Div([
        # html.H1(children='Movie Recommendation System'),
        html.Div("List of movies:"),
        # TODO: initial movie_id list to be changed
        html.Div(id='popularity_main_div', children=movie_div)])
    return app_popularity_tab


if __name__ == "__main__":
    main()
