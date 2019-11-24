#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from ast import literal_eval
import ast
import surprise
from surprise import Reader, Dataset, SVD, model_selection
import pickle
import os.path

Run = False

if __name__ == "__main__":
    Run = True
    print("process file cop")

if not os.path.isfile('cop.txt'):
    Run = True
    print('process file cop')

if Run:
    md = pd. read_csv('movies_metadata.csv')
    ratings = pd.read_csv('ratings.csv')
    links = pd.read_csv('links.csv')
    links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')

    md = md.drop([19730, 29503, 35587])
    md = md[md['release_date'].notnull()]
    md['id'] = md['id'].astype('int')

    full_md = md[md['id'].isin(links)]

def get_genre(df):
    """
    This function is to get information about genres
    Input: dataframe
    Output: list
    """
    genres = []
    for n in range(len(df)):
        genre = []
        for id_name in ast.literal_eval(df.genres.to_list()[n]):
            genre.append(id_name['name'])
        genres.append(genre)
    return genres

def get_year(df):
    """
    This function is to get information about years
    Input: dataframe
    Output: list
    """
    years = []
    for date in df.release_date.to_list():
        years.append(date.split('-')[0])
    return years

def get_countries(df):
    """
    This function is to get information about countries
    Full names of countries are adopted
    Input: dataframe
    Output: list
    """
    countries = []
    for n in range(len(df)):
        country = []
        for countryinfo in ast.literal_eval(df.production_countries.to_list()[n]):
            country.append(countryinfo['name'])
        countries.append(country)
    return countries

if Run:
    full_md['genres'] = get_genre(full_md)
    full_md['year'] = get_year(full_md)
    full_md['countries'] = get_countries(full_md)

    reader = Reader()
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    svd = SVD()
    model_selection.cross_validate(svd, data, measures=['RMSE', 'MAE'], cv = 5)

    trainset = data.build_full_trainset()
    svd.fit(trainset)

    movie_id_sort = sorted(set(ratings.movieId))

def get_recommended_movies(user_id):
    '''
    Input: user id (integer)
    Output: A dataframe contains 10 recommended movies (information about these movie included)
    '''
    already_watched = list(ratings[ratings['userId'] == user_id]['movieId'])
    predicted_est = {}
    id_set = []
    for i in movie_id_sort:
        if i not in already_watched:
            predicted_est[i] = svd.predict(user_id, i).est
        else:
            predicted_est[i] = 0
    predicted_est = sorted(predicted_est.items(), key = lambda x:x[1], reverse = True)
    for i in predicted_est:
        if len(id_set) < 10:
            if i[0] in full_md['id'].to_list():
                id_set.append(i[0])
    recommendation = full_md[full_md['id'].isin(id_set)]
    return recommendation


class collaborative:
    def __init__(self, user_recommendation_dic):
        self.user_recommendation_dic = dic

def save_recommendation_file():
    dic = {'0': [0]}
    for i in range(467):
        print('creating recommendation for ' )
        print(i)
        print('\n')
        recommendation = get_recommended_movies(i)
        #print(recommendation.index.values)
        titles  = recommendation['title'].values.tolist()
        dic[i] = titles
    return dic

if Run:
    dic = save_recommendation_file()
    cop = collaborative(dic)
    file = open('cop.txt','wb')
    pickle.dump(cop, file)

# Futurework1:
# If we recommend movies just based on the similarity between regardless of ratings and popularity, we'll recommend bad movies to users. Thus we can build a machanism to filter bad movies combined with the content recommender system.
