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
1. Clone the repository.

```git clone https://github.com/xiashuhan/CSE583project-Group9.git```

2. Install the package.

```python setup.py install```

3.Run main_display.py and obtain the url.

4.Run the url in your browser and get to the user's interface.

#### For more detailed package demo, see [example](https://github.com/xiashuhan/CSE583project-Group9/tree/master/example)

