from __future__ import annotations

from typeguard import typechecked

import relational_calculus.domain_calculus as dc


class Result:
    @typechecked
    def __init__(self, variables: list[dc.Variable]) -> None:
        """
        Parameters
        ----------
        variables : list[Variable]
            The variables that should be returned.
        """
        if len(variables) == 0:
            raise Exception("Must return at least one variable")
        self.variables = variables

    @typechecked
    def __repr__(self) -> str:
        output = ""
        for variable in self.variables:
            output += f"\\text{{{variable.name}}}, "
        output = output[:-2]  # remove last ', '
        return output
