"""Actions that you can take on components."""
from typing import Dict
from typing import Union

from .comparison import Comparison


def decompose(
    comparison: Comparison, intermediate: bool = False
) -> Dict[Comparison, Union[int, float]]:
    """Return the relative responsibilities for the differences in `comparison`.

    Args:
        comparison: The `Comparison` to decompose.
        intermediate: Whether to output decompositions of the
                      "intermediate" comparisons (true),
                      or only the leaves of the "decomp tree" (false).

    Notes:
        The values of the dict will sum to 1.

    Returns:
        Dict of `Comparison` to a float the represents the percent
        contribution of that `Comparison` to the comparison input to the function.
        The percent is in decimal form: i.e. 0.2=20%.

    """

    def decompose_recur(
        results: Dict[Comparison, Union[int, float]]
    ) -> Dict[Comparison, Union[int, float]]:
        if not any(comparison_._relationship for comparison_ in results):
            return results

        if intermediate:
            new_results = {k: v for k, v in results.items()}
        else:
            new_results = {}

        for comparison_ in results:
            relationship = comparison_._relationship
            if relationship is not None and not all(
                el in results for el in relationship.elements
            ):
                contribution_base: Union[int, float] = results[comparison_]
                subcomparison_contributions = relationship.contribution_pct()

                new_contributions = {
                    subcmp: contribution_base * subcmp_contrib
                    for subcmp, subcmp_contrib in subcomparison_contributions.items()
                }
                new_results.update(decompose_recur(new_contributions))
            else:
                new_results.update({comparison_: results[comparison_]})
        return new_results

    return decompose_recur(results={comparison: 1})
