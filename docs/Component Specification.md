## Component Specification

#### **(a).Software components**

- **Data manager:**
  - **What it does:** Based on user’s input of different movie attributes (e.g. director, release year, language, etc.), filter out movies from the whole movie dataset.
  - **Inputs it requires:** Pick movie attributes from Dropdown
  - **Outputs it provides:** A subset of movies satisfying user picked attributes
- **Prediction manager:** 
  - **What it does:** Predicting rating and popularity of a movie based on input information
  - **Inputs it requires:** Cast, country, crew, category, company, budget, runtime etc.
  - **Outputs it provides:** Predicted rating and popularity of a movie based on input information. 

- **Visualization manager:** 
  -  **What it does:** Display information (i.e. poster, movie overview, average rating, etc.)  of filtered or recommended movies in a user interface. In the use case of prediction, it also displays rating/prediction results.
  -  **Inputs it requires:** In the use case of prediction, the input is rating/prediction results.
  -  **Outputs it provides:** ![img](https://lh3.googleusercontent.com/92ne2UboVFU89ka2z93iO7TIF2E2Jx9nYQ4pKzIyV29uliIwOFAjIu37NxRVmOl7q3Cnu_hKYWq8slQCoNj5F7bdjkTP3M1h8B8yqanD4WAbP8dArlCTWDqC6-fQrnXPz1WHDi1D)



#### **(b).Interactions to accomplish use cases**

- Use case of movie recommendation system:** Data manager analyzes user’s previous movie ratings and extracts a list of similar movies that would be recommended to this user. Then visualization manager display information on recommended movies to the user.		
  - i.e. DATA MANAGER ——> VISUALIZATION MANAGER
- **Use case of rating/popularity prediction:** Users input cast, country, crew, category, company, budget, runtime, etc movie information, prediction manager predicts the rating and popularity of a movie based on input information.		
  - i.e. PREDICTION MANAGER ——> VISUALIZATION MANAGER

#### **(c).Preliminary plan**

- Complete data_manager.py to provide needed methods for data cleaning and preprocessing and return filtered and recommendation results based on movie attributes picked by users.
- Complete prediction_manager.py to predict rating and popularity of a movie based on its basic information.
- Complete visualization_manager.py to visualize selected data of movies with detailed descriptions (i.e. poster, movie overview, average rating, etc.).

