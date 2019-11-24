import pandas as pd
import numpy as np
import ast
from ast import literal_eval



# functions to extract certain information in the data
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

def get_director(df):
    """
    This function is to get information about directors
    Input: dataframe
    Output: list
    """
    directors = []
    for n in range(len(df)):
        director = []
        for crewinfo in ast.literal_eval(df.crew.to_list()[n]):
            if crewinfo['job'] == 'Director':
                director.append(crewinfo['name'])
                break
        directors.append(director)
    return directors

def get_cast(df):
    """
    This function is to get information about actors
    Input: dataframe
    Output: list
    """
    cast = []
    for n in range(len(df)):
        ct = []
        for ctinfo in ast.literal_eval(df.cast.to_list()[n]):
            ct.append(ctinfo['name'])
        cast.append(ct)
    return cast

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

# extract and store information about genres, directors, actors, years, and countries




# extend a row with a list of genres/directors/actors/countries to several rows with only one genre/director/actor/countrie






class simple_recommendation:
    def __init__(self):
        md = pd.read_csv('movies_metadata.csv')
        credits = pd.read_csv('credits.csv')
        # drop some inappropriate records
        md = md[md['release_date'].notnull()]
        md = md.drop([19730, 29503, 35587])
        # merge data
        credits['id'] = credits['id'].astype('int')
        md['id'] = md['id'].astype('int')
        md = md.merge(credits, on='id')
        self.md = md
        self.md['genres'] = get_genre(self.md)
        print(self.md['genres'])
        self.md['director'] = get_director(self.md)
        print(self.md['director'])
        self.md['cast'] = get_cast(self.md)
        print(self.md['cast'])
        self.md['year'] = get_year(self.md)
        print(self.md['year'])
        self.md['countries'] = get_countries(self.md)
        print(self.md['countries'])
        col_genre = self.md.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
        col_genre.name = 'genre'
        col_director = self.md.apply(lambda x: pd.Series(x['director']),axis=1).stack().reset_index(level=1, drop=True)
        col_director.name = 'director'
        col_actor = self.md.apply(lambda x: pd.Series(x['cast']),axis=1).stack().reset_index(level=1, drop=True)
        col_actor.name = 'actor'
        col_country = self.md.apply(lambda x: pd.Series(x['countries']),axis=1).stack().reset_index(level=1, drop=True)
        col_country.name = 'country'
        self.md_new = self.md.drop(['genres','director','cast','countries'], axis=1).join(col_genre)
        self.md_new = self.md_new.join(col_director)
        self.md_new = self.md_new.join(col_actor)
        self.md_new = self.md_new.join(col_country)
    def weighted_rating(self, x):
        """
        This function is to calculate weighted ratings
        """
        m = self.m
        C = self.C
        v = x['vote_count']
        R = x['vote_average']
        return (v/(v+m) * R) + (m/(m+v) * C)
    def get_recommended_movies(self, constraints, percentile=0.8):
        """
        Input: constraints is a list of length 5
        constraints = [genre,year,country,director,actor]
        Each element in the input list is either a string or None type
        Output: A dataframe contains 10 recommended movies (information about these movie included)
        """
        constraint_names = ['genre','year','country','director','actor']
        for i in range(len(constraints)):
            if constraints[i]:
                df = self.md_new[self.md_new[constraint_names[i]] == constraints[i]]
        vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
        self.C = vote_averages.mean()
        self.m = vote_counts.quantile(percentile)
        m = self.m
        C = self.C
        qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title', 'genre','year','country','director','actor', 'vote_count', 'vote_average', 'popularity']]
        qualified['vote_count'] = qualified['vote_count'].astype('int')
        qualified['vote_average'] = qualified['vote_average'].astype('int')
        qualified['wr'] = qualified.apply(self.weighted_rating, axis=1)
        qualified_list = qualified.sort_values('wr', ascending=False).drop_duplicates(subset=['title', 'year','vote_count', 'vote_average', 'popularity'],keep='first').head(10).title.to_list()
        recommendation = self.md[self.md['title'].isin(qualified_list)][['title', 'genres','year','countries','director','cast', 'vote_count', 'vote_average', 'popularity']]
        return recommendation


#sp = simple_recommendation()
#print(sp.md)
