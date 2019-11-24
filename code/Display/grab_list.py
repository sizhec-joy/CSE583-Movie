import csv
import sys
import pickle
genre_set = {'Foreign'}
#year_set = {}
country_set = {'United States of America'}
director_set = {'Mervyn LeRoy'}
actor_set = {'Sho Kosugi'}
director_dic = {'Mervyn LeRoy': 0}
actor_dic = {'Sho Kosugi': 0}
name_set = {'Stagecoach'}
id_set = {2}
id_title_set = {'Annie Hall': 703}
max_count = 50000
pop_director = 10
pop_actor = 30

def process_genre(row):
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
    substring = row['title']
    index = 100000
    if substring is None:
        return
    if len(substring) > 0 and substring[0].isalpha():
        name_set.add(substring)

def process_id(row):
    substring = row['id']
    if len(substring) > 0 and substring.isnumeric():
        id_set.add(int(substring))

def process_title_id(row):
    substring = row['id']
    substringg = row['title']
    index = 100000
    if substring is None or substringg is None:
        return
    if len(substringg) > 0 and substringg[0].isalpha() and len(substring) > 0 and substring.isnumeric():
        id_title_set[substringg] = int(substring)


def process_country(row):
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
            director_dic[director]  = director_dic[director] + 1;
            if director_dic[director] > pop_director:
                director_set.add(director)
        else:
            director_dic[director] = 1


def process_cast(row):
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
               pass;
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

    '''
    index = substring.find('name\'')
    substring = substring[index + 8:]
    index = substring.find('\'')
    director = substring[0:index]
    if director is not None:
        director_set.add(director)
'''

def read_csv():
    file = open('meta.txt','rb')
    obs = pickle.load(file)
    return obs

def read_csv_c():
    with open('movies_metadata.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            process_genre(row)
            process_country(row)
            process_name(row)
            process_id(row)
            process_title_id(row)

    with open('credits.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            process_director(row)
            process_cast(row)
"""
country_set = {'United States of America'}
director_set = {'Mervyn LeRoy'}
actor_set = {'Sho Kosugi'}
director_dic = {'Mervyn LeRoy': 0}
actor_dic = {'Sho Kosugi': 0}
name_set = {'Stagecoach'}
id_set = {2}
id_title_set = {'Annie Hall': 703}
"""
class object_save:
    def __init__(self, genre_set, country_set, director_set, actor_set, director_dic, actor_dic, name_set, id_set, id_title_set):
        self.country_set = sorted(country_set)
        self.genre_set = sorted(genre_set)
        self.director_set = sorted(director_set)
        self.actor_set = sorted(actor_set)
        self.director_dic = (director_dic)
        self.actor_dic = (actor_dic)
        self.name_set = sorted(name_set)
        self.id_set = sorted(id_set)
        self.id_title_set = (id_title_set)


def save_file():

    obs = object_save(genre_set, country_set, director_set, actor_set, director_dic, actor_dic, name_set, id_set, id_title_set)
    file = open('meta.txt','wb')
    pickle.dump(obs, file)
    print('file saved: meta.txt')


if __name__ == "__main__":
    read_csv_c()
    #print(id_title_set)
    save_file()
#read_csv()
#print(id_title_set)
#print(name_set)
#print(genre_set)
#print(country_set)
#print(director_set)
#print(actor_set)
