# Movie Recommender System

- **Contributors:** 
  - Sizhe Chen
  - Yandi Jin
  - Miaoran Li
  - Shuhan Xia
  - Jing Xu

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

#### Use Cases

**The objective of the user interaction:** Get 10 movies he/she may like

**Use case 1:**

**For Simple filtering:**

​	**User input:** 5 filters: genre, year, country, director, actor 

​	**System output:** Recommended movies based on movie popularity

**Use case 2:**

**For Content based filtering:**

​	**User input:** Movie title

​	**System output:** Recommended movies based on the similarity to the given movie

**Use case 3:**

**For collaborative filtering:**

​	**User input:** User id

​	**System output:** Recommended movies by user based filtering and item based filtering. For user-based recommendation, the system recommends movies to the user that similar users like. 
![img](https://lh4.googleusercontent.com/RJmo8OrXxaQEqj7T__PjD2s_tCYHkKu-OFG1Oo9GKZ0sTE27OqylQ62R1q5MkAuWj1KNI_bYItuoyoaSkQloaXuYvOGYYfWZbxAHwYgx026Q-t1_pifpiG7vPxUWAjT0JrlnJjC9)

## Component Specification

**(a). Simple Filter:**

**What it does:** Based on user’s input of different movie attributes (e.g. director, release year, language, etc.), filter out movies that satisfy the specific conditions and get recommended movies among them.

**Inputs it requires:** 5 filters (genre/year/country/director/actor)

**Outputs it provides:** A data frame of top 10 movies based on weighted ratings

**(b). Content-based Filter:** 

**What it does:** Recommend movies based on a specific movie

**Inputs it requires:** A  movie title

**Outputs it provides:** A data frame of top 10 movies based on similarities to the given movie

**(c). User-based Filter:** 

**What it does:** Recommend movies to a specific user

**Inputs it requires:** A  user id

**Outputs it provides:** A data frame of 10 movies with top predicted ratings

**(d). Visualization manager:** 

**What it does:** Display information (poster, movie overview, average rating, etc.)  of filtered or recommended movies in a user interface.

**Inputs it requires:** A data frame of recommended movies

**Outputs it provides:** A website displays the recommended movies with names, posters and introductions
![img](https://lh3.googleusercontent.com/92ne2UboVFU89ka2z93iO7TIF2E2Jx9nYQ4pKzIyV29uliIwOFAjIu37NxRVmOl7q3Cnu_hKYWq8slQCoNj5F7bdjkTP3M1h8B8yqanD4WAbP8dArlCTWDqC6-fQrnXPz1WHDi1D)

