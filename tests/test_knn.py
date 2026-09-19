import unittest
from pathlib import Path

from KNN.fish import Fish
from KNN.knn import KNN


class FishTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_file = Path(__file__).resolve().parent.parent / "KNN" / "datasets" / "fish" / "fish.csv"

    def test_nearest(self):
        """Test finding the nearest neighbors of a data point."""
        k: int = 3
        fish_knn = KNN(Fish, self.data_file)
        test_fish: Fish = Fish("", 0.0, 30.0, 32.5, 38.0, 12.0, 5.0)
        nearest_fish: list[Fish] = fish_knn.nearest(k, test_fish)
        self.assertEqual(len(nearest_fish), k)
        expected_fish = [
            Fish("Bream", 340.0, 29.5, 32.0, 37.3, 13.9129, 5.0728),
            Fish("Bream", 500.0, 29.1, 31.5, 36.4, 13.7592, 4.368),
            Fish("Bream", 700.0, 30.4, 33.0, 38.3, 14.8604, 5.2854),
        ]
        self.assertEqual(nearest_fish, expected_fish)

    def test_classify(self):
        """Test classifying a data point."""
        k: int = 5
        fish_knn = KNN(Fish, self.data_file)
        test_fish: Fish = Fish("", 0.0, 20.0, 23.5, 24.0, 10.0, 4.0)
        classify_fish: str = fish_knn.classify(k, test_fish)
        self.assertEqual(classify_fish, "Parkki")


if __name__ == "__main__":
    unittest.main()
