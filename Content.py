#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import warnings; warnings.simplefilter('ignore')

md = pd.read_csv('movies_metadata.csv')
md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
m = vote_counts.quantile(0.95)
md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
links = pd.read_csv('links.csv')
links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')

md = md.drop([19730, 29503, 35587])
md['id'] = md['id'].astype('int')

full_md = md[md['id'].isin(links)]


# Build a content based recommender system based on a combination of movie cast, crew, keywords, genre
# Here we merge dataset "credits.csv" and dataset "keywords.csv"

credits = pd.read_csv('credits.csv')
keywords = pd.read_csv('keywords.csv')

keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
md['id'] = md['id'].astype('int')

md = md.merge(credits, on='id')
md = md.merge(keywords, on='id')

full_md = md[md['id'].isin(links)]

full_md['cast'] = full_md['cast'].apply(literal_eval)
full_md['crew'] = full_md['crew'].apply(literal_eval)
full_md['keywords'] = full_md['keywords'].apply(literal_eval)


def get_director_name(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def string_pre(x):
    return str.lower(x.replace(" ",""))

full_md['director'] = full_md['crew'].apply(get_director_name)

full_md['cast'] = full_md['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
full_md['cast'] = full_md['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)

full_md['keywords'] = full_md['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
full_md['cast'] = full_md['cast'].apply(lambda x: [string_pre(i) for i in x])
full_md['director'] = full_md['director'].astype('str').apply(lambda x: string_pre(x))
full_md['director'] = full_md['director'].apply(lambda x: [x])

s = full_md.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'

s = s.value_counts()
s = s[s > 1]

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

stemmer = SnowballStemmer('english')

full_md['keywords'] = full_md['keywords'].apply(filter_keywords)
full_md['keywords'] = full_md['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
full_md['keywords'] = full_md['keywords'].apply(lambda x: [string_pre(i) for i in x])

full_md['comb'] = full_md['keywords'] + full_md['cast'] + full_md['director'] + full_md['genres']
full_md['comb'] = full_md['comb'].apply(lambda x: ' '.join(x))

count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix = count.fit_transform(full_md['comb'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

full_md = full_md.reset_index()
titles = full_md['title']
indices = pd.Series(full_md.index, index=full_md['title'])

class content_recommendation:
    def __init__(self, full_md, titles, cosine_sim, indices):
        self.full_md = full_md
        self.titles = titles
        self.cosine_sim = cosine_sim
        self.indices = indices
    def get_recommendations(self, title):
        idx = self.indices[title]
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
        for movie in self.titles.iloc[movie_indices]:
            if movie not in ans:
                ans.append(movie)
            if len(ans) == 10:
                return ans
        return ans
    def get_recommended_movies(self, movie):
        list = self.get_recommendations(movie)
        return self.full_md[self.full_md['title'].isin(list)]


cp = content_recommendation(full_md, titles, cosine_sim, indices)
# Futurework1:
# If we recommend movies just based on the similarity between regardless of ratings and popularity, we'll recommend bad movies to users. Thus we can build a machanism to filter bad movies combined with the content recommender system.
