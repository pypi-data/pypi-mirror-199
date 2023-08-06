from __future__ import annotations

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class Result:
    @typechecked
    def __init__(self, attributes: list[tc.Variable | tuple[tc.Variable, str]]) -> None:
        """
        Parameters
        ----------
        attributes : list[Variable | tuple[Variable, str]]
        """
        assert (
            attributes is not None and len(attributes) > 0
        ), "Must return some variables / attributes."
        self.attributes = attributes

    @typechecked
    def __repr__(self) -> str:
        output = "["
        for x in self.attributes:
            if isinstance(x, tc.Variable):
                output += f"\\text{{{x.name}}}, "
            elif isinstance(x, tuple):
                variable, attribute = x
                output += f"\\text{{{variable.name}.{attribute}}}, "
        output = output[: -len(", ")]
        output += "]"
        return output
