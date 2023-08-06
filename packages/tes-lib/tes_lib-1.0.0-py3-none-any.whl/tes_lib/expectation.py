"""
Expectation definition
"""
from typing import Any, Callable, List, Dict
from enum import Enum


class Expectation:
    """
    Expectation definition - should be used with the event helper functions
    """

    def __init__(
        self, event_field_name: str, comparison_function: Callable, comparison_value: Any
    ) -> None:
        self.event_field_name = event_field_name
        self.comparison_function = comparison_function
        self.comparison_value = comparison_value

    def __repr__(self):
        return "{} {}('{}': {})".format(
            self.event_field_name,
            self.comparison_function.__name__,
            self.comparison_value,
            type(self.comparison_value).__name__,
        )


class ExpectationFailureType(Enum):
    COMPARISON_FAILURE = 1
    FIELD_NOT_FOUND = 2


class FailedExpectation:
    """
    A wrapper around an expectation that has failed with additional information
    """

    def __init__(
        self,
        expectation: Expectation,
        failure_type: ExpectationFailureType,
        event_value: Any = None,
    ) -> None:
        self.expectation = expectation
        self.failure_type = failure_type
        self.event_value = event_value

    def __repr__(self):
        if self.failure_type == ExpectationFailureType.FIELD_NOT_FOUND:
            return "ExpectationFailure: {} field not found".format(
                self.expectation,
            )

        # COMPARISON_FAILURE logic is the default behaviour
        return "ExpectationFailure: {} got '{}': {}".format(
            self.expectation,
            self.event_value,
            type(self.event_value).__name__,
        )


class PartialMatch:
    def __init__(self, event: Dict, expectation_failures: List[FailedExpectation]) -> None:
        self.event = event
        self.expectation_failures = expectation_failures
