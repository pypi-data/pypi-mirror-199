from dataclasses import dataclass
from typing import Any, Dict

from factory import factory_register


@dataclass
class Phecode_Pvalue_Distributions:

    name: str = "Phecode_Pvalue_Distributions"

    def analyze(self, **kwargs) -> Dict[str, Any]:
        """execute method"""
        raise NotImplementedError

    def write(self, **kwargs) -> None:
        raise NotImplementedError


def initialize() -> None:
    factory_register("phecode_pvalue_distributions", Phecode_Pvalue_Distributions)
