# Movie Recommender System

#### Contributors:
  - Sizhe Chen
  - Yandi Jin
  - Miaoran Li
  - Shuhan Xia
  - Jing Xu

## About

This project aims to recommend tailored movie information to users based on their needs.

## Background

The movie industry has witnessed its prosperity for the last two decades.There are new movies produced everyday and we now have more film choices than ever before. However, it also becomes hard to tell if one movie is better than the other. So we want to create a movie recommender system to help our users pick the right high-quality movie that’s in their favors.

## User profile

Our system is designed for film lovers who have difficulty deciding which movie to watch. There is no technical prerequisite so that all potential users are able to navigate through the system.

## Data sources

Our dataset contains 5 main files:

**movies_metadata.csv:** Contains information for 45,000 movies. Features include posters, backdrops, budget, revenue, release dates, languages, production countries and companies etc.

**keywords.csv:** Contains the movie plot keywords.

**credits.csv:** Consists of cast and crew Information.

**links.csv:** Contains the TMDB and IMDB IDs of all the movies.

**ratings.csv:** Contains 27,000,000 ratings and 1,100,000 tag applications applied to 58,000 movies by 280,000 users.Use cases. 

## Project structure
```
|-- movie_recommendations
|   |   | assets
|   |   |   | detail_collapsible.css
|   |   |   | overlay.css
|   |   |   | responsive-sidebar.css
|   |   |   | title.css
|   |   | movies-dataset
|   |   |   | source
|   |   |   |   | collaborative_result.csv
|   |   |   |   | cop.txt
|   |   |   | movies_metadata.csv.zip
|   |   |   | ratings.csv
|   |   |   | ...
|   |   | main_display.py
|   |   | app.py
|   |   | display_content_base.py
|   |   | display_final_movie.py
|   |   | display_popularity.py
|   |   | display_recomm.py
|   |   | get_movie_info.py
|   |   | global_record.py
|   |   | grab_list.py
|   |   | simple_recommender.py
|   |   | content_based.py
|   |   | userbased_filtering.py
|   |   | test
|   |   |   | test_recommendation.py
|-- docs
|   | Component Specification.md
|   | Functional_specification.md
|-- exmaple
|   | example.md
|-- LICENSE
|-- README.md
|-- setup.py
|-- .gitignore
```

## How to use
1.Clone the repository.

```git clone https://github.com/xiashuhan/CSE583project-Group9.git```

2.Install the package.

```python3 setup.py install```

**3.Unzip credits.csv.zip and movies_metadata.csv.zip files.** 

4.Run main_display.py and obtain the url.

```python3 main_display.py```

5.Run the url in your browser and get to the user's interface.

#### For more detailed package demo, see [example](https://github.com/xiashuhan/movie_recommendations/blob/master/example/Example.md)

