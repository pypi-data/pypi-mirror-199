"""Module to hold relationships between terms."""
from __future__ import annotations

import operator
from functools import wraps
from math import log
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Dict


if TYPE_CHECKING:
    from .comparison import Comparison

RT_contribution_pct = Dict["Comparison", float]


def _pre_post_process(
    function: Callable[[Any], Any]
) -> Callable[[Callable[..., RT_contribution_pct]], Callable[..., RT_contribution_pct]]:
    """Wrap the pct contribution to invert the operator."""

    def wrap(
        f: Callable[..., RT_contribution_pct]
    ) -> Callable[..., RT_contribution_pct]:
        @wraps(f)
        def wrapped_f(self: _TermRelationship) -> RT_contribution_pct:
            right_x_cache = self.right.x
            right_y_cache = self.right.y
            self.right.x = function(self.right.x)
            self.right.y = function(self.right.y)
            try:
                return f(self)
            finally:
                self.right.x = right_x_cache
                self.right.y = right_y_cache

        return wrapped_f

    return wrap


class _TermRelationship:
    op: Callable[[Any, Any], Any]
    sign: str

    def __init__(self, left: Comparison, right: Comparison):
        self.left = left
        self.right = right

    @property
    def elements(self) -> list[Comparison]:
        return [self.left, self.right]

    def contribution_pct(self) -> RT_contribution_pct:
        raise NotImplementedError

    @property
    def x(self) -> Any:
        return self.op(self.left.x, self.right.x)

    @property
    def y(self) -> Any:
        return self.op(self.left.y, self.right.y)

    def _name(self) -> str:
        return self.sign.join([el.name for el in self.elements])


class _AdditionRelationship(_TermRelationship):
    op = operator.add
    sign = "+"

    def contribution_pct(self) -> Dict[Comparison, float]:
        left_diff = self.left.diff_abs()
        right_diff = self.right.diff_abs()
        total = left_diff + right_diff

        if total == 0:
            if left_diff == 0 and right_diff == 0:
                return {self.left: 0.5, self.right: 0.5}
            return {
                self.left: left_diff / abs(left_diff),
                self.right: right_diff / abs(right_diff),
            }
        return {self.left: left_diff / total, self.right: right_diff / total}


class _MultiplicationRelationship(_TermRelationship):
    op = operator.mul
    sign = "*"

    def contribution_pct(self) -> Dict[Comparison, float]:
        total_x = self.left.x * self.right.x
        total_y = self.left.y * self.right.y

        if total_x == 0 and total_y == 0:
            return {self.left: 0.5, self.right: 0.5}

        if total_x == 0:
            # x is 0, so we went from something to 0

            if self.left.x == 0 and self.right.x == 0:
                # both Terms went to 0, so they share 50/50 contribution
                return {self.left: 0.5, self.right: 0.5}

            if self.left.x == 0:
                return {self.left: 1, self.right: 0}
            if self.right.x == 0:
                return {self.left: 0, self.right: 1}

        if total_y == 0:
            # we went from 0 to something
            # this methodology at least has the property
            # that if left stays the same, and right goes from 0->X,
            # right gets all the contribution
            if self.left.y == 0 and self.right.y == 0:
                return {self.left: 0.5, self.right: 0.5}
            try:
                left_contrib = log(self.left.x / self.left.y)
            except ZeroDivisionError:
                left_contrib = log(self.left.x + 1)

            try:
                right_contrib = log(self.right.x / self.right.y)
            except ZeroDivisionError:
                right_contrib = log(self.right.x + 1)

            total = left_contrib + right_contrib
            return {self.left: left_contrib / total, self.right: right_contrib / total}

        # the situation at this point in execution is total_y > 0 and total_x > 0
        left_contrib = log(self.left.x / self.left.y)
        right_contrib = log(self.right.x / self.right.y)

        total_diff = log(total_x / total_y)

        if total_diff == 0:
            # avoid DivideByZero error
            return {self.left: 0.5, self.right: 0.5}
        return {
            self.left: left_contrib / total_diff,
            self.right: right_contrib / total_diff,
        }


class _SubtractionRelationship(_AdditionRelationship):
    op = operator.sub
    sign = "-"

    @_pre_post_process(lambda x: -x)
    def contribution_pct(self) -> Dict[Comparison, float]:
        return super().contribution_pct()


class _DivisionRelationship(_MultiplicationRelationship):
    op = operator.truediv
    sign = "/"

    @_pre_post_process(lambda x: 1 / x)
    def contribution_pct(self) -> Dict[Comparison, float]:
        return super().contribution_pct()
