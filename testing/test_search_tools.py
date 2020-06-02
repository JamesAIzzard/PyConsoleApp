from unittest import TestCase

from pyconsoleapp import search_tools

class TestScoreSimilarity(TestCase):

    def test_scores_match_correctly(self):
        words = ["one", "two", "three", "four"]
        search_term = "one"
        score = search_tools.score_similarity(words, search_term)
        self.assertEqual(score["one"], 1.0)