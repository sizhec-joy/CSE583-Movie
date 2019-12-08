# Movie Recommender System

This project aims to recommend tailored movie information to users based on their needs.

- **Contributors:** 
  - Sizhe Chen
  - Yandi Jin
  - Miaoran Li
  - Shuhan Xia
  - Jing Xu

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
|   |   |   | credits.csv.zip
|   |   |   | keywords.csv
|   |   |   | links.csv
|   |   |   | links_small.csv
|   |   |   | movies_metadata.csv.zip
|   |   |   | ratings.csv
|   |   | app.py
|   |   | content_based.py
|   |   | display_content_base.py
|   |   | display_final_movie.py
|   |   | display_popularity.py
|   |   | display_recomm.py
|   |   | get_movie_info.py
|   |   | global_record.py
|   |   | grab_list.py
|   |   | main_display.py
|   |   | simple_recommender.py
|   |   | userbased_filtering.py
|   |   | test
|   |   |   | test_recommendation.py
|-- docs
|   | Component Specification.md
|   | Functional_specification.md
|-- LICENSE
|-- README.md
|-- setup.py
|-- .gitignore
```

## How to use
1.Clone the repository.

2.Run main_display.py and obtain the url.

3.Run the url in your browser and get to the user's interface.
