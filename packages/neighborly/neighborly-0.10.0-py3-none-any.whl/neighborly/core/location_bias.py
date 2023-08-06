"""
location_frequency_rule.py

This module provides interface and classes that help characters determine
where within a settlement they choose to frequent
"""
from __future__ import annotations

import dataclasses
from typing import Iterator, List, Optional, Protocol

from neighborly.core.ecs import GameObject


class ILocationBiasRule(Protocol):
    """LocationBiasRules define what locations characters are likely to frequent"""

    def __call__(self, character: GameObject, location: GameObject) -> Optional[int]:
        """
        Calculate a weight modifier for a character frequenting a location

        Parameters
        ----------
        character: GameObject
            The character to check
        location: GameObject
            The location to check

        Returns
        -------
        Optional[int]
            Optionally returns an integer value representing a weight modifier for
            how likely the given character would be to frequent the given location
            based on some precondition(s)
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class LocationBiasRuleInfo:
    """
    Information about a location bias rule

    Attributes
    ----------
    rule: ILocationBiasRule
        The callable function that implements the rule
    description: str
        A text description of the rule
    """

    rule: ILocationBiasRule
    description: str = ""


class LocationBiasRules:
    """Repository of active rules that determine what location characters frequent"""

    _rules: List[LocationBiasRuleInfo] = []

    @classmethod
    def add(cls, rule: ILocationBiasRule, description: str = "") -> None:
        cls._rules.append(LocationBiasRuleInfo(rule, description))

    @classmethod
    def iter_rules(cls) -> Iterator[LocationBiasRuleInfo]:
        return cls._rules.__iter__()
