'''
This module is used for content-based filtering
'''


import os.path
from ast import literal_eval
import pickle
import pandas as pd
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer


Run = False
if __name__ == "__main__":
    Run = True
    print("process FILE CP")

if not os.path.isfile('CP.txt'):
    Run = True
    print("process FILE CP")


if Run:
    MD = pd.read_csv('movies-dataset/movies_metadata.csv')
    MD['genres'] = MD['genres'].fillna('[]')
    MD['genres'] = MD['genres'].apply(literal_eval)
    MD['genres'] = MD['genres'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    VOTE_COUNTS = MD[MD['vote_count'].notnull()]['vote_count'].astype('int')
    VOTE_AVERAGES = MD[MD['vote_average'].notnull()]['vote_average'].astype('int')
    C = VOTE_AVERAGES.mean()
    M = VOTE_COUNTS.quantile(0.95)
    MD['year'] = pd.to_datetime(MD['release_date'], errors='coerce')
    MD['year'] = MD['year'].apply(lambda x: str(x).split('-')[0] if x != numpy.nan else numpy.nan)
    LINKS = pd.read_csv('movies-dataset/links.csv')
    LINKS = LINKS[LINKS['tmdbId'].notnull()]['tmdbId'].astype('int')

    MD = MD.drop([19730, 29503, 35587])
    MD['id'] = MD['id'].astype('int')

    FULL_MATRIX = MD[MD['id'].isin(LINKS)]


    # Build a content based recommender system based on a combination of movie cast, crew, keywords, genre
    # Here we merge dataset "credits.csv" and dataset "keywords.csv"

    CREDITS = pd.read_csv('movies-dataset/credits.csv')
    KEYWORDS = pd.read_csv('movies-dataset/keywords.csv')

    KEYWORDS['id'] = KEYWORDS['id'].astype('int')
    CREDITS['id'] = CREDITS['id'].astype('int')
    MD['id'] = MD['id'].astype('int')

    MD = MD.merge(CREDITS, on='id')
    MD = MD.merge(KEYWORDS, on='id')

    FULL_MATRIX = MD[MD['id'].isin(LINKS)]

    FULL_MATRIX['cast'] = FULL_MATRIX['cast'].apply(literal_eval)
    FULL_MATRIX['crew'] = FULL_MATRIX['crew'].apply(literal_eval)
    FULL_MATRIX['keywords'] = FULL_MATRIX['keywords'].apply(literal_eval)


def get_director_name(x):
    '''
    Get director name
    Input: a row of dataframe
    Output: a string
    '''
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return numpy.nan

def string_pre(x):
    '''
    Turn strings into lower case
    Input: a string
    Output: a lower case string
    '''
    return str.lower(x.replace(" ", ""))

if Run:
    FULL_MATRIX['director'] = FULL_MATRIX['crew'].apply(get_director_name)

    FULL_MATRIX['cast'] = FULL_MATRIX['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    FULL_MATRIX['cast'] = FULL_MATRIX['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)

    FULL_MATRIX['keywords'] = FULL_MATRIX['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    FULL_MATRIX['cast'] = FULL_MATRIX['cast'].apply(lambda x: [string_pre(i) for i in x])
    FULL_MATRIX['director'] = FULL_MATRIX['director'].astype('str').apply(lambda x: string_pre(x))
    FULL_MATRIX['director'] = FULL_MATRIX['director'].apply(lambda x: [x])

    S = FULL_MATRIX.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
    S.name = 'keyword'

    S = S.value_counts()
    S = S[S > 1]

def filter_keywords(x):
    '''
    Get unique keywords list
    Input: a list
    Output: a list without repeated word
    '''
    words = []
    for i in x:
        if i in S:
            words.append(i)
    return words

if Run:
    STEMMER = SnowballStemmer('english')

    FULL_MATRIX['keywords'] = FULL_MATRIX['keywords'].apply(filter_keywords)
    FULL_MATRIX['keywords'] = FULL_MATRIX['keywords'].apply(lambda x: [STEMMER.stem(i) for i in x])
    FULL_MATRIX['keywords'] = FULL_MATRIX['keywords'].apply(lambda x: [string_pre(i) for i in x])

    FULL_MATRIX['comb'] = FULL_MATRIX['keywords'] + FULL_MATRIX['cast'] + FULL_MATRIX['director'] + FULL_MATRIX['genres']
    FULL_MATRIX['comb'] = FULL_MATRIX['comb'].apply(lambda x: ' '.join(x))

    WORD_COUNT = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    COUNT_MATRIX_S = WORD_COUNT.fit_transform(FULL_MATRIX['comb'])
    cosine_sim = cosine_similarity(COUNT_MATRIX_S, COUNT_MATRIX_S)

    FULL_MATRIX = FULL_MATRIX.reset_index()
    TITLES = FULL_MATRIX['title']
    INDICES = pd.Series(FULL_MATRIX.index, index=FULL_MATRIX['title'])

class ContentRecommendation:
    '''
    This class is to calcualte the similarities amont other movies and the given movie;
    also it filters out recommended movies
    '''
    def __init__(self, FULL_MATRIX, TITLES, INDICES):
        self.FULL_MATRIX = FULL_MATRIX
        self.TITLES = TITLES
        self.INDICES = INDICES
        self.cosine_sim = None
    def generate_cosine_sim(self):
        '''Generate cosine distance'''
        if self.cosine_sim is None:
            count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
            count_matrix = count.fit_transform(self.FULL_MATRIX['comb'])
            self.cosine_sim = cosine_similarity(count_matrix, count_matrix)
    def get_recommendations(self, title):
        '''According to input title, filter out top similar movies'''
        idx = self.INDICES[title]
        if type(idx) == numpy.int64:
            pass
        else:
            if len(list(idx)) > 1:
                idx = list(idx)[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        movie_indices = [i[0] for i in sim_scores]
        ans = []
        for movie in self.TITLES.iloc[movie_indices]:
            if movie not in ans:
                ans.append(movie)
            if len(ans) == 10:
                return ans
        return ans
    def get_recommended_movies(self, movie):
        '''Extract movies from existing movie database frame'''
        list = self.get_recommendations(movie)
        ans = self.FULL_MATRIX[self.FULL_MATRIX['title'].isin(list)].drop_duplicates(subset=['title'])
        return ans

if Run:
    CP = ContentRecommendation(FULL_MATRIX, TITLES, INDICES)
    FILE = open('CP.txt', 'wb')
    pickle.dump(CP, FILE)
# Futurework1:
# If we recommend movies just based on the similarity between regardless of ratings and popularity，
# we'll recommend bad movies to users.
# Thus we can build a machanism to filter bad movies combined with the content recommender system.
