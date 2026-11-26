import unittest
from recommend import recommend


class RecommendationTests(unittest.TestCase):
    def test_rising_demand(self):
        result = recommend([0.31, 0.42, 0.55, 0.66, 0.78], 2, max_replicas=5)
        self.assertEqual(result["recommended_replicas"], 3)
        self.assertTrue(result["requires_operator_review"])

    def test_guardrails(self):
        self.assertEqual(recommend([0.1, 0.1, 0.1], 5)["recommended_replicas"], 4)
        self.assertEqual(recommend([0.8, 0.9, 1.0], 2, max_replicas=2)["recommended_replicas"], 2)
        self.assertEqual(recommend([0, 0, 0], 1)["recommended_replicas"], 1)

    def test_bad_input(self):
        for samples in [[], [0, 0, 2], [0, 0, float("nan")]]:
            with self.assertRaises(ValueError):
                recommend(samples, 2)
        with self.assertRaises(ValueError):
            recommend([0, 0, 0], 0)


if __name__ == "__main__":
    unittest.main()
