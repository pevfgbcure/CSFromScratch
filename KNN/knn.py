import csv
from collections import Counter
from pathlib import Path
from typing import Protocol, Self

import numpy as np


class DataPoint(Protocol):
    """Protocol for data points used in KNN classification."""

    kind: str

    @classmethod
    def from_string_data(cls, data: list[str]) -> Self:
        """Create a data point from a list of string values.

        Args:
            data: List of string values representing the data point.

        Returns:
            An instance of the data point.
        """
        ...

    def distance(self, other: Self) -> float:
        """Calculate the Euclidean distance between two data points.

        Args:
            other: The other data point to calculate the distance to.

        Returns:
            The Euclidean distance as a float.
        """
        ...


class KNN[DP: DataPoint]:
    """K-Nearest Neighbors classifier."""

    def __init__(self, data_point_type: type[DP], file_path: str | Path, has_header: bool = True) -> None:
        """Initialize the KNN classifier with data from a CSV file.

        Args:
            data_point_type: The class type for data points.
            file_path: Path to the CSV file containing the training data.
            has_header: Whether the CSV file has a header row.
        """
        self.data_point_type = data_point_type
        self.data_points = []
        self._read_csv(file_path, has_header)

    def _read_csv(self, file_path: str | Path, has_header: bool) -> None:
        """Read data points from a CSV file.

        Args:
            file_path: Path to the CSV file.
            has_header: Whether the CSV file has a header row.
        """
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            if has_header:
                _ = next(reader)
            for row in reader:
                self.data_points.append(self.data_point_type.from_string_data(row))

    def nearest(self, k: int, data_point: DP) -> list[DP]:
        """Find the k nearest neighbors to a data point.

        Args:
            k: The number of nearest neighbors to find.
            data_point: The data point to find neighbors for.

        Returns:
            A list of the k nearest data points.
        """
        return sorted(self.data_points, key=data_point.distance)[:k]

    def classify(self, k: int, data_point: DP) -> str:
        """Classify a data point using the K-Nearest Neighbors algorithm.

        Args:
            k: The number of nearest neighbors to use for classification.
            data_point: The data point to classify.

        Returns:
            The predicted class label (kind) of the data point.
        """
        neighbors = self.nearest(k, data_point)
        return Counter(neighbor.kind for neighbor in neighbors).most_common(1)[0][0]

    def predict(self, k: int, data_point: DP, property_name: str) -> float:
        """Predict a scalar property value using the K-Nearest Neighbors algorithm.

        Args:
            k: The number of nearest neighbors to use for prediction.
            data_point: The data point to predict for.
            property_name: The name of the property to predict.

        Returns:
            The predicted value of the specified property.
        """
        neighbors = self.nearest(k, data_point)
        return sum([getattr(neighbor, property_name) for neighbor in neighbors]) / len(neighbors)

    def predict_array(self, k: int, data_point: DP, property_name: str) -> np.ndarray:
        """Predict an array property value using the K-Nearest Neighbors algorithm.

        Args:
            k: The number of nearest neighbors to use for prediction.
            data_point: The data point to predict for.
            property_name: The name of the property to predict.

        Returns:
            The predicted value of the specified property.
        """
        neighbors = self.nearest(k, data_point)
        return np.sum([getattr(neighbor, property_name) for neighbor in neighbors], axis=0) / len(neighbors)
