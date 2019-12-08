"""
Unit test for simple_recommender.py
"""

import unittest
import movie_recommendations.simple_recommender as simple_recommender


class TestSimpleRecommender(unittest.TestCase):
    """
    Input: A list of 5 constraints, namely genre, year,
    country, director, and actor.
    Output: A dataframe containing 10 recommended movies
    Should test if the output is adequate.
    """
    def setUp(self):
        self.recommender = simple_recommender.simple_recommendation()
        self.test_filter = ['Romance', '1996', 'United States of America', 'Quentin Tarantino', 'Brad Pitt']

    def test_genres(self):
        """
        Check if the movie list does not exceed 10, is non-repetitive,
        and has the correct genre information
        """
        recommend = self.recommender.get_recommended_movies([self.test_filter[0], None, None, None, None])
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")
        for i in range(recommend.shape[0]):
            self.assertIn(self.test_filter[0], recommend["genres"][i], msg="Wrong movies")

    def test_year(self):
        """
        Check if the movie list does not exceed 10, is non-repetitive,
        and has the correct year information
        """
        recommend = self.recommender.get_recommended_movies([None, self.test_filter[1], None, None, None])
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")
        for i in range(recommend.shape[0]):
            self.assertEqual(self.test_filter[1], recommend["year"][i], msg="Wrong movies")

    def test_countries(self):
        """
        Check if the movie list does not exceed 10, is non-repetitive,
        and has the correct country information
        """
        recommend = self.recommender.get_recommended_movies([None, None, self.test_filter[2], None, None])
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")
        for i in range(recommend.shape[0]):
            self.assertIn(self.test_filter[2], recommend["countries"][i], msg="Wrong movies")

    def test_director(self):
        """
        Check if the movie list does not exceed 10, is non-repetitive,
        and has the correct director information
        """
        recommend = self.recommender.get_recommended_movies([None, None, None, self.test_filter[3], None])
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")
        for i in range(recommend.shape[0]):
            self.assertIn(self.test_filter[3], recommend["director"][i], msg="Wrong movies")

    def test_cast(self):
        """
        Check if the movie list does not exceed 10, is non-repetitive,
        and has the correct cast information
        """
        recommend = self.recommender.get_recommended_movies([None, None, None, None, self.test_filter[4]])
        self.assertTrue(recommend.shape[0] <= 10, msg="More than 10 movies")
        self.assertEqual(len(recommend["title"]), len(set(recommend["title"])), msg="Repetitive movies")
        for i in range(recommend.shape[0]):
            self.assertIn(self.test_filter[4], recommend["cast"][i], msg="Wrong movies")


if __name__ == '__main__':
    unittest.main()
