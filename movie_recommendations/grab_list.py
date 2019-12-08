'''
this is a function
'''

import csv
import sys
import pickle
import os.path


max_count = 50000
pop_director = 10
pop_actor = 30


genre_set = {'Foreign'}
country_set = {'United States of America'}
director_set = {'Mervyn LeRoy'}
actor_set = {'Sho Kosugi'}
director_dic = {'Mervyn LeRoy': 0}
actor_dic = {'Sho Kosugi': 0}
name_set = {'Stagecoach'}
id_set = {2}
id_title_set = {'Annie Hall': 703}


Run = False
if not os.path.isfile('meta.txt'):
    Run = True
    print('process file meta')
if __name__ == "__main__":
    Run = True
    print("process file meta")


def process_genre(row):
    '''
    this is a function
    '''
    substring = row['genres']
    index = 100000
    if substring is None:
        return
    while index > 0:
        index = substring.find('name')
        if index > 0:
            substring = substring[index + 8:]
            index_end = substring.find('\'')
            genre = substring[0:index_end]
            genre_set.add(genre)


def process_name(row):
    '''
    this is a function
    '''
    substring = row['title']
    if substring is None:
        return
    if len(substring) > 0 and substring[0].isalpha():
        name_set.add(substring)


def process_id(row):
    '''
    this is a function
    '''
    substring = row['id']
    if len(substring) > 0 and substring.isnumeric():
        id_set.add(int(substring))


def process_title_id(row):
    '''
    this is a function
    '''
    substring = row['id']
    substringg = row['title']
    if substring is None or substringg is None:
        return
    if len(substringg) > 0 and substringg[0].isalpha() and len(substring) > 0 and substring.isnumeric():
        id_title_set[substringg] = int(substring)


def process_country(row):
    '''
    this is a function
    '''
    substring = row['production_countries']
    if substring is None:
        return
    index = 100000
    while index > 0:
        index = substring.find('name')
        if index > 0:
            substring = substring[index + 8:]
            index_end = substring.find('\'')
            country = substring[0:index_end]
            country_set.add(country)


def process_director(row):
    '''
    this is a function
    '''
    substring = row['crew']
    if substring is None:
        return
    index = substring.find('\'Director\'')
    substring = substring[index + 21:]
    index = substring.find('\'')
    director = substring[0:index]
    if director is None or len(director) < 1:
        return
    if director[0] == ' ':
        director = director[1:]
    if director is not None and director[0].isalpha():
        if director in director_dic:
            director_dic[director] = director_dic[director] + 1
            if director_dic[director] > pop_director:
                director_set.add(director)
        else:
            director_dic[director] = 1


def process_cast(row):
    '''
    this is a function
    '''
    substring = row['cast']
    if substring is None:
        return
    index = 100000
    while index > 0:
        index = substring.find('name')
        if index > 0:
            substring = substring[index + 8:]
            index_end = substring.find('\'')
            actor = substring[0:index_end]
            if actor is None or len(actor) < 1:
                pass
            else:
                if actor[0] == ' ':
                    actor = actor[1:]
                if  len(actor) > 0 and actor[0].isalpha():
                    if actor in actor_dic:
                        actor_dic[actor] = actor_dic[actor] + 1
                        if actor_dic[actor] > pop_actor:
                            actor_set.add(actor)
                    else:
                        actor_dic[actor] = 1


def read_csv():
    '''
    this is a function
    '''
    file = open('meta.txt', 'rb')
    obs = pickle.load(file)
    return obs


def read_csv_c():
    '''
    this is a function
    '''
    with open('./movies-dataset/movies_metadata.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            process_genre(row)
            process_country(row)
            process_name(row)
            process_id(row)
            process_title_id(row)

    with open('./movies-dataset/credits.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            process_director(row)
            process_cast(row)


class object_save:
    '''
    this is a class
    '''
    def __init__(self, genre_set_o, country_set_o, director_set_o, actor_set_o, director_dic_o, actor_dic_o, name_set_o, id_set_o, id_title_set_o):
        self.country_set = sorted(country_set_o)
        self.genre_set = sorted(genre_set_o)
        self.director_set = sorted(director_set_o)
        self.actor_set = sorted(actor_set_o)
        self.director_dic = (director_dic_o)
        self.actor_dic = (actor_dic_o)
        self.name_set = sorted(name_set_o)
        self.id_set = sorted(id_set_o)
        self.id_title_set = (id_title_set_o)


def save_file():
    '''
    this is a function
    '''
    obs = object_save(genre_set, country_set, director_set, actor_set, director_dic, actor_dic, name_set, id_set, id_title_set)
    file = open('meta.txt', 'wb')
    pickle.dump(obs, file)
    print('file saved: meta.txt')


if Run:
    '''
    this is a function
    '''
    read_csv_c()
    save_file()

#read_csv()
#print(id_title_set)
#print(name_set)
#print(genre_set)
#print(country_set)
#print(director_set)
#print(actor_set)
