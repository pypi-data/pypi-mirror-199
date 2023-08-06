"""Comparison class."""
from __future__ import annotations

from numbers import Real
from typing import Any
from typing import Dict

from . import relationships


# Create a generic variable that can be 'Parent', or any subclass.


class Comparison:
    """A Comparison of a variable of interest between state `x` and state `y`."""

    def __init__(
        self,
        name: str,
        x: int | float,
        y: int | float,
        tags: Dict[str, str] | None = None,
        id: str | None = None,
    ):
        """A Comparison of a variable of interest between state `x` and state `y`."""
        self.name = name
        self.tags = tags
        self.x = x
        self.y = y
        self._relationship: relationships._TermRelationship | None = None

    def diff_abs(self) -> int | float:
        """Return the absolute difference between `x` and `y`."""
        return self.x - self.y

    def diff_pct(self) -> int | float:
        """Return the difference between `x` and `y` as a percentage.

        Notes:
            Percentages are returned as a decimal. E.g. 0.2 is 20%.

        """
        return self.diff_abs() / self.y

    @classmethod
    def _from_relationship(
        cls,
        rel: relationships._TermRelationship,
        tags: Dict[Any, Any] | None = None,
    ) -> Comparison:
        """Create a Comparison object from a relationship."""
        name: str = rel._name()
        instance: Comparison = cls(name, x=rel.x, y=rel.y, tags=tags)
        instance._relationship = rel
        return instance

    def __repr__(self) -> str:
        return f"Comparison({self.name}, x={self.x}, y={self.y})"

    def __add__(self, other: Comparison) -> Comparison:
        return Comparison._from_relationship(
            relationships._AdditionRelationship(self, other)
        )

    def __radd__(self, other: Comparison | Real) -> Comparison:
        if isinstance(other, Real):
            if other == 0:
                # sum([Component, Component]) will first add 0 + component
                return self
            raise ValueError
        other_comparison: Comparison = other
        return Comparison._from_relationship(
            relationships._AdditionRelationship(other_comparison, self)
        )

    def __mul__(self, other: Comparison) -> Comparison:
        return Comparison._from_relationship(
            relationships._MultiplicationRelationship(self, other)
        )

    def __rmul__(self, other: Comparison) -> Comparison:
        return Comparison._from_relationship(
            relationships._MultiplicationRelationship(other, self)
        )

    def __truediv__(self, other: Comparison) -> Comparison:
        return Comparison._from_relationship(
            relationships._DivisionRelationship(self, other)
        )

    def __rtruediv__(self, other: Comparison) -> Comparison:
        return Comparison._from_relationship(
            relationships._DivisionRelationship(other, self)
        )

    def __sub__(self, other: Comparison) -> Comparison:
        return Comparison._from_relationship(
            relationships._SubtractionRelationship(self, other)
        )


class Constant(Comparison):
    """Placeholder to allow operations of Comparisons involving constants."""

    def __init__(
        self,
        name: str,
        value: float,
        tags: Dict[str, str] | None = None,
        id: None | str = None,
    ):
        """Placeholder to allow operations of Comparisons involving constants."""
        super().__init__(name, x=value, y=value, tags=tags, id=id)
