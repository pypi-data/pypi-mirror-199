from __future__ import annotations

from typeguard import typechecked

import relational_calculus.domain_calculus as dc


class Variable:
    @typechecked
    def __init__(self, name: str) -> None:
        self.name = name.lower()

    @typechecked
    def __repr__(self) -> str:
        return f"\\text{{{self.name}}}"
