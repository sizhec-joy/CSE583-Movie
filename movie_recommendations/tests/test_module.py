#!/usr/bin/env python
# coding: utf-8

# Simple recommender
# Input: A list of 5 constraints in order, constraints = [genre,year,country,director,actor]. Each element in the input list is either a string or None type
# Output: A dataframe contains 10 recommended movies (information about these movie included)
# Here users input two constraints on genre and year, we use the "get_recommended_movies" function in module Simple_Recommeder to give output.

import Simple_Recommender as sr

print(sr.get_recommended_movies(['Romance','1996',None,None,None])

# Content based recommender
# Input: Movie name: str (The movie id should be in link.csv, keywords.csv, credits.csv at the same time)
# Output: A dataframe contains 10 recommended movies (information about these movie included)
# Here users input a movie name, we use the "get_recommended_movies" function in module Content to give output.

import Content

print(Content.get_recommended_movies('The Dark Knight'))

# Collaborative filtering: user based recommender
# Input: User id: int (The user id should be in original dataset)
# Output: A dataframe contains 10 recommended movies (information about these movie included)
# Here users input his/her own id, we use the "get_recommended_movies" function in module Collaborative to give recommendations.

import Collaborative

print(Collaborative.get_recommended_movies(50))
