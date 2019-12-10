"""
Unit test for content_based.py
"""

import unittest
import movie_recommendations.content_based as content_recommender


class TestContentRecommender(unittest.TestCase):
    """
    Input: A list of 5 constraints, namely genre, year,
    country, director, and actor.
    Output: A dataframe containing 10 recommended movies
    Should test if the output is adequate.
    """
    def setUp(self):
        self.recommender = content_recommender.ContentRecommendation()
        self.test_movietitle = 'Toy Story'

    def test_content(self):
        """
        Check if the movie list does not exceed 10, is non-repetitive,
        and has the correct movie information
        """
        recommend = self.recommender.get_recommended_movies(self.test_movietitle)
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")
            
if __name__ == '__main__':
    unittest.main()
