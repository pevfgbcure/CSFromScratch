from dataclasses import dataclass
from typing import Self

from KNN.knn import DataPoint


@dataclass
class Fish(DataPoint):
    """Data point representing a fish for KNN classification."""

    kind: str
    weight: float
    length1: float
    length2: float
    length3: float
    height: float
    width: float

    @classmethod
    def from_string_data(cls, data: list[str]) -> Self:
        """Create a Fish instance from a list of string values.

        Args:
            data: List of string values containing fish attributes in the order:
                kind, weight, length1, length2, length3, height, width

        Returns:
            Fish instance with attributes converted to appropriate types.
        """
        return cls(
            kind=data[0],
            weight=float(data[1]),
            length1=float(data[2]),
            length2=float(data[3]),
            length3=float(data[4]),
            height=float(data[5]),
            width=float(data[6]),
        )

    def distance(self, other: Self) -> float:
        """Calculate Euclidean distance between this fish and another.

        Args:
            other: Another Fish instance to calculate distance to.

        Returns:
            Euclidean distance as a float.
        """
        return (
            (self.length1 - other.length1) ** 2
            + (self.length2 - other.length2) ** 2
            + (self.length3 - other.length3) ** 2
            + (self.height - other.height) ** 2
            + (self.width - other.width) ** 2
        ) ** 0.5
