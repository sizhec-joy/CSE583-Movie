"""
Unit test for user_based_recommender.py
"""

import unittest
import movie_recommendations.userbased_filtering as user_recommender


class TestUserRecommender(unittest.TestCase):
    """
    Input: A user id
    Output: A dataframe containing 10 recommended movies
    Should test if the output is adequate.
    """
    def setUp(self):
        self.recommender = user_recommender.Collabrotive()
        self.test_filter = 80

    def test_genres(self):
        """
        Check if the movie list does not exceed 10
        """
        recommend = self.recommender.get_recommended_movies(self.test_filter)
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")

if __name__ == '__main__':
    unittest.main()
