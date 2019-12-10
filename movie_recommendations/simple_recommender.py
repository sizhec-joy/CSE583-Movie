import os.path
import ast
import pickle
import pandas as pd

Run = False

if not os.path.isfile('sp.txt'):
    Run = True
    print('process file sp')

if __name__ == "__main__":
    Run = True
    print("process file sp")


# functions to extract certain information in the data
def get_genre(dataframe):
    """
    This function is to get information about genres
    Input: dataframe
    Output: list
    """
    genres = []
    for row_number in range(len(dataframe)):
        genre = []
        for id_name in ast.literal_eval(dataframe.genres.to_list()[row_number]):
            genre.append(id_name['name'])
        genres.append(genre)
    return genres


def get_director(dataframe):
    """
    This function is to get information about directors
    Input: dataframe
    Output: list
    """
    directors = []
    for row_number in range(len(dataframe)):
        director = []
        for crew_info in ast.literal_eval(dataframe.crew.to_list()[row_number]):
            if crew_info['job'] == 'Director':
                director.append(crew_info['name'])
                break
        directors.append(director)
    return directors


def get_cast(dataframe):
    """
    This function is to get information about actors
    Input: dataframe
    Output: list
    """
    casts = []
    for row_number in range(len(dataframe)):
        cast = []
        for cast_info in ast.literal_eval(dataframe.cast.to_list()[row_number]):
            cast.append(cast_info['name'])
        casts.append(cast)
    return casts


def get_year(dataframe):
    """
    This function is to get information about years
    Input: dataframe
    Output: list
    """
    years = []
    for date in dataframe.release_date.to_list():
        years.append(date.split('-')[0])
    return years


def get_countries(dataframe):
    """
    This function is to get information about countries
    Full names of countries are adopted
    Input: dataframe
    Output: list
    """
    countries = []
    for row_number in range(len(dataframe)):
        country = []
        for country_info in ast.literal_eval(dataframe.production_countries.to_list()[row_number]):
            country.append(country_info['name'])
        countries.append(country)
    return countries


def weighted_rating(dataframe, mean_value, quantile_value):
    """
    This function is to calculate weighted ratings
    Input: A dataframe you want to calculate weighted ratings for, values of mean and quantile
    Output: A list of weighted ratings
    """
    count_vote = dataframe['vote_count']
    average_vote = dataframe['vote_average']
    return (count_vote / (count_vote + mean_value) * average_vote) + (mean_value / (mean_value + count_vote) * quantile_value)

class SimpleRecommendation:
    '''
    This is simple recommedation algorithm.
    '''
    def __init__(self):
        meta_data = pd.read_csv('movies-dataset/movies_metadata.csv')
        credits = pd.read_csv('movies-dataset/credits.csv')
        # drop some inappropriate records
        meta_data = meta_data[meta_data['release_date'].notnull()]
        meta_data = meta_data.drop([19730, 29503, 35587])
        # merge data
        credits['id'] = credits['id'].astype('int')
        meta_data['id'] = meta_data['id'].astype('int')
        meta_data = meta_data.merge(credits, on='id')
        self.meta_data = meta_data
        self.meta_data['genres'] = get_genre(self.meta_data)
        print(self.meta_data['genres'])
        self.meta_data['director'] = get_director(self.meta_data)
        print(self.meta_data['director'])
        self.meta_data['cast'] = get_cast(self.meta_data)
        print(self.meta_data['cast'])
        self.meta_data['year'] = get_year(self.meta_data)
        print(self.meta_data['year'])
        self.meta_data['countries'] = get_countries(self.meta_data)
        print(self.meta_data['countries'])
        col_genre = self.meta_data.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
        col_genre.name = 'genre'
        col_director = self.meta_data.apply(lambda x: pd.Series(x['director']), axis=1).stack().reset_index(level=1, drop=True)
        col_director.name = 'director'
        col_actor = self.meta_data.apply(lambda x: pd.Series(x['cast']), axis=1).stack().reset_index(level=1, drop=True)
        col_actor.name = 'actor'
        col_country = self.meta_data.apply(lambda x: pd.Series(x['countries']), axis=1).stack().reset_index(level=1, drop=True)
        col_country.name = 'country'
        self.meta_data_new = self.meta_data.drop(['genres', 'director', 'cast', 'countries'], axis=1).join(col_genre)
        self.meta_data_new = self.meta_data_new.join(col_director)
        self.meta_data_new = self.meta_data_new.join(col_actor)
        self.meta_data_new = self.meta_data_new.join(col_country)

    def get_recommended_movies(self, constraints, percentile=0.8):
        '''
        This function is to get 10 recommended movies
        Input: A list of 5 filters [genre, year, country, director, actor]
        Output: A dataframe of top 10 recommendations
        '''
        constraint_names = ['genre', 'year', 'country', 'director', 'actor']
        data_frame = self.meta_data_new
        for i in range(len(constraints)):
            if constraints[i]:
                data_frame = data_frame[data_frame[constraint_names[i]] == constraints[i]]
        vote_counts = data_frame[data_frame['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = data_frame[data_frame['vote_average'].notnull()]['vote_average'].astype('int')
        vote_mean = vote_averages.mean()
        vote_quantile = vote_counts.quantile(percentile)
        qualified = data_frame[(data_frame['vote_count'] >= vote_quantile) & (data_frame['vote_count'].notnull()) & (data_frame['vote_average'].notnull())][['id', 'genre', 'year', 'country', 'director', 'actor', 'vote_count', 'vote_average', 'popularity']]
        qualified['vote_count'] = qualified['vote_count'].astype('int')
        qualified['vote_average'] = qualified['vote_average'].astype('int')
        qualified['wr'] = weighted_rating(qualified, vote_quantile, vote_mean)
        qualified_list = qualified.sort_values('wr', ascending=False).drop_duplicates(subset=['id', 'year', 'vote_count', 'vote_average', 'popularity'], keep='first').id.to_list()
        id_set = []
        for id_num in qualified_list:
            if len(id_set) < 10:
                if self.meta_data['id'].to_list():
                    id_set.append(id_num)
        recommendation = self.meta_data[self.meta_data['id'].isin(id_set)][['title', 'genres', 'year', 'countries', 'director', 'cast', 'vote_count', 'vote_average', 'popularity']]
        return recommendation

if Run:
    SIMPLE = SimpleRecommendation()
    FILE = open('sp.txt', 'wb')
    pickle.dump(SIMPLE, FILE)
#print(sp.md)
