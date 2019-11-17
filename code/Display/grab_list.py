import csv
import sys
genre_set = {'Foreign'}
#year_set = {}
country_set = {'United States of America'}
director_set = {'Mervyn LeRoy'}
actor_set = {'Sho Kosugi'}
director_dic = {'Mervyn LeRoy': 0}
actor_dic = {'Sho Kosugi': 0}
name_set = {'Stagecoach'}
max_count = 1000
pop_director = 20
pop_actor = 100

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
    with open('movies_metadata.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            process_genre(row)
            process_country(row)
            process_name(row)
           
    with open('credits.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            process_director(row)
            process_cast(row)

#print(name_set)
#print(genre_set)
#print(country_set)
#print(director_set)
#print(actor_set)
