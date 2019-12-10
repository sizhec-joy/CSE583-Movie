## Component Specification

#### **(a).Software components**

- **Simple Filter:**
  - **What it does:** get recommendation based on user’s input of different movie attributes
  - **Inputs it requires:** 5 filters (genre/year/country/director/actor)
  - **Outputs it provides:** A data frame of top 10 movies based on weighted ratings
  
- **Content-based Filter:** 
  - **What it does:** get recommendation based on movie similarities
  - **Inputs it requires:** a movie title
  - **Outputs it provides:** A data frame of top 10 movies based on similarities to the given movie

- **User based Filter:** 
  - **What it does:** get recommendation based on user similarities
  - **Inputs it requires:** a user id
  - **Outputs it provides:** A data frame of top 10 movies based on similarities to the given user

- **Visualization manager:** 
  -  **What it does:** Display information (i.e. poster, movie overview, average rating, etc.)  of filtered or recommended movies in a user interface. In the use case of prediction, it also displays rating/prediction results.
  -  **Inputs it requires:** In the use case of prediction, the input is a dataframe of recommendation results.
  -  **Outputs it provides:** ![img](https://lh3.googleusercontent.com/92ne2UboVFU89ka2z93iO7TIF2E2Jx9nYQ4pKzIyV29uliIwOFAjIu37NxRVmOl7q3Cnu_hKYWq8slQCoNj5F7bdjkTP3M1h8B8yqanD4WAbP8dArlCTWDqC6-fQrnXPz1WHDi1D)



#### **(b).Interactions to accomplish use cases**

- For the first use case, the simple filter is used. The user enters 5 filters, if the filter is not specified, it is None by default. The simple recommender will first get all movies satisfy the specific conditions. We use IMDB's weighted rating formula to calculate weighted ratings for movies. Then all we have to do is to sort selected movies based on weighted ratings and display the top 10 movies in the list. We get a data frame of 10 recommended movies from the simple recommender and pass it to visualization manager, which can display the names, posters and introductions of the movies.

  - i.e. Simple Filter ——> Visualization Manager
- For the second use case, a movie name entered by the user will be passed to the content-based filter. The filter will calculate the similarities between the given movie and all other movies. The measurement of similarity is the cosine distance based on movie cast, crew, keywords and genre. Then the content-based filter will generate a data frame of 10 movies with top similarities. Finally, the visualization manager will show the users the recommended movies based on content similarity with detailed information.		
  - i.e. Content-based Filter ——> Visualization Manager

 - For the third use case, given a user id, the filter will first calculate the similarities between this user and all other users based on the movies they have already reviewed. Then it will predict the rating this user may give to a certain movie based on the user similarity and their ratings on the movie. Finally, a data frame of 10 movies with top predicted ratings will be passed to the visualization manager and the visualization manager will display these movies to the user.		
  - i.e. User-based Filter ——> Visualization Manager

