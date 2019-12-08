import pickle
import os.path
import ast
import pandas as pd
from surprise import Reader, Dataset, SVD, model_selection

Run = False

if __name__ == "__main__":
    Run = True
    print("process file cop")

if not os.path.isfile('cop.txt'):
    Run = True
    print('process file cop')

if Run:
    META = pd.read_csv('../movies-dataset/movies_metadata.csv')
    RATINGS = pd.read_csv('../movies-dataset/ratings.csv')
    LINKS = pd.read_csv('../movies-dataset/links.csv')
    LINKS = LINKS[LINKS['tmdbId'].notnull()]['tmdbId'].astype('int')

    META = META.drop([19730, 29503, 35587])
    META = META[META['release_date'].notnull()]
    META['id'] = META['id'].astype('int')

    FULL_META = META[META['id'].isin(LINKS)]

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
        for countryinfo in ast.literal_eval(dataframe.production_countries.to_list()[row_number]):
            country.append(countryinfo['name'])
        countries.append(country)
    return countries

if Run:
    FULL_META['genres'] = get_genre(FULL_META)
    FULL_META['year'] = get_year(FULL_META)
    FULL_META['countries'] = get_countries(FULL_META)

    READER = Reader()
    DATA = Dataset.load_from_df(RATINGS[['userId', 'movieId', 'rating']], READER)
    SVD = SVD()
    model_selection.cross_validate(SVD, DATA, measures=['RMSE', 'MAE'], cv=5)

    TRAINSET = DATA.build_full_trainset()
    SVD.fit(TRAINSET)

    MOVIE_ID_SORT = sorted(set(RATINGS.movieId))

def get_recommended_movies(user_id):
    '''
    Input: user id (integer)
    Output: A dataframe contains 10 recommended movies (information about these movie included)
    '''
    already_watched = list(RATINGS[RATINGS['userId'] == user_id]['movieId'])
    predicted_est = {}
    id_set = []
    for i in MOVIE_ID_SORT:
        if i not in already_watched:
            predicted_est[i] = SVD.predict(user_id, i).est
        else:
            predicted_est[i] = 0
    predicted_est = sorted(predicted_est.items(), key=lambda x: x[1], reverse=True)
    for i in predicted_est:
        if len(id_set) < 10:
            if i[0] in FULL_META['id'].to_list():
                id_set.append(i[0])
    recommendation = FULL_META[FULL_META['id'].isin(id_set)][['title', 'id']].values.tolist()
    return recommendation

def save_recommendation_file():
    '''
    save recommendation result
    '''
    dic = {'0': [0]}
    for i in range(467):
        print('creating recommendation for ')
        print(i)
        print('\n')
        recommendation = get_recommended_movies(i)
        #print(recommendation.index.values)
        titles = recommendation['title'].values.tolist()
        dic[i] = titles
    return dic

class Collaborative:
    '''
    User_based recommendation
    '''
    def __init__(self, user_recommendation_dic):
        self.user_recommendation_dic = DIC

if Run:
    DIC = save_recommendation_file()
    COLLA = Collaborative(DIC)
    FILE = open('cop.txt', 'wb')
    pickle.dump(COLLA, FILE)
