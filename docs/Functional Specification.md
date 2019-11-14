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

**The objective of the user interaction:** Get 5 movies he/she may like

**For Demographic filtering:**

​	**User input:** None

​	**System output:** Recommended movies based on movie popularity. 

**For Content based filtering:**

​	**User input:** genre, director, description, actors

​	**System output:** Recommended movies based on movie popularity.

**For collaborative filtering:**

​	**User input:** None

​	**System output:** Recommended movies by user based filtering and item based filtering. For user-based recommendation, the system recommends movies to the user that similar users like. For item-based recommendation, the result is based on the similarity with the movies that the user rated. ![img](https://lh6.googleusercontent.com/psmMhX9QqeuVIzc0xB1oQ6RQVeY7m1vMEfpCUGtHIJR8YFnngNikmWpV8QL4FJeccZDHql9XnTT7cc7RGblxL6m5weGGWdyMRbiXQjv3Kh843IJLLVnW7pSNMkPvWLico8tLUTO9).
