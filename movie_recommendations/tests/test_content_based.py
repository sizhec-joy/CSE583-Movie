import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()



# Content based recommender
# Input: Movie name: str (The movie id should be in link.csv, keywords.csv, credits.csv at the same time)
# Output: A dataframe contains 10 recommended movies (information about these movie included)
# Here users input a movie name, we use the "get_recommended_movies" function in module Content to give output.

import movie_recommendations.content_based as Content

print(Content.get_recommended_movies('The Dark Knight'))

# Collaborative filtering: user based recommender
# Input: User id: int (The user id should be in original dataset)
# Output: A dataframe contains 10 recommended movies (information about these movie included)
# Here users input his/her own id, we use the "get_recommended_movies" function in module Collaborative to give recommendations.

import movie_recommendations.Collaborative as Collaborative

print(Collaborative.get_recommended_movies(50))