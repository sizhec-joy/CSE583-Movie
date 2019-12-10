## Functional Specification

#### Background

The movie industry has witnessed its prosperity for the last two decades.There are new movies produced everyday and we now have more film choices than ever before. However, it also becomes hard to tell if one movie is better than the other. So we want to create a movie recommender system to help our users pick the right high-quality movie that’s in their favors.

#### User profile

Our system is designed for film lovers who have difficulty deciding which movie to watch. There is no technical prerequisite so that all potential users are able to navigate through the system.

#### Data sources

Our dataset contains 5 main files:

**movies_metadata.csv:** Contains information for 45,000 movies. Features include posters, backdrops, budget, revenue, release dates, languages, production countries and companies etc.

**keywords.csv:** Contains the movie plot keywords.

**credits.csv:** Consists of cast and crew Information.

**links.csv:** Contains the TMDB and IMDB IDs of all the movies.

**ratings.csv:** Contains 27,000,000 ratings and 1,100,000 tag applications applied to 58,000 movies by 280,000 users.Use cases. 

#### Use case

**The objective of the user interaction:** Get 10 movies he/she may like

- **For Simple filtering:**

  - **User input:** genre, year, country, director, actors

  - **System output:** Recommended movies based on movie popularity. 

- **For Content based filtering:**

  - **User input:** Movie's title

  - **System output:** Recommended movies based on the similarity among other movies and the movie input.

- **For collaborative filtering:**

  - **User input:** User id

  - **System output:** Recommended movies by user based filtering. For user-based recommendation, the system recommends movies to the user that similar users like. 


