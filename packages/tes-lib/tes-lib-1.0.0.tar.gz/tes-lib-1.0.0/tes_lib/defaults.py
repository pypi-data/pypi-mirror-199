"""Defaults that can be optionally overridden"""
from typing import Callable
from tes_lib.constants import (
    DEFAULT_REQUEST_TIMEOUT,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_MAXIMUM_POLL_TIME,
    DEFAULT_UNEXPECTED_EVENT_MAXIMUM_POLL_TIME,
    DEFAULT_EXTENDED_EVENT_DEBUG,
    DEFAULT_MAX_EVENTS_TO_OUTPUT,
    DEFAULT_MAX_EXPECTATIONS_PER_EVENT_TO_OUTPUT,
)

# pylint: disable=missing-function-docstring


# This exists only to shut mypy up
def _on_failure():
    pass


class Defaults:
    ON_FAILURE = _on_failure
    REQUEST_TIMEOUT = DEFAULT_REQUEST_TIMEOUT
    POLL_INTERVAL = DEFAULT_POLL_INTERVAL
    MAXIMUM_POLL_TIME = DEFAULT_MAXIMUM_POLL_TIME
    UNEXPECTED_EVENT_MAXIMUM_POLL_TIME = DEFAULT_UNEXPECTED_EVENT_MAXIMUM_POLL_TIME
    EXTENDED_EVENT_DEBUG_ON_EXPECTATION_FAILURE = DEFAULT_EXTENDED_EVENT_DEBUG
    MAXIMUM_EVENTS_TO_OUTPUT = DEFAULT_MAX_EVENTS_TO_OUTPUT
    MAXIMUM_EXPECTATIONS_PER_EVENT_TO_OUTPUT = DEFAULT_MAX_EXPECTATIONS_PER_EVENT_TO_OUTPUT


def setup_library_defaults(
    on_failure: Callable,
    request_timeout: float,
    poll_interval: float,
    maximum_poll_time: float,
    unexpected_event_maximum_poll_time: float,
    extended_event_debug_on_expectation_failure: bool,
    maximum_events_to_output: int,
    maximum_expectations_per_event_to_output: int,
):
    Defaults.ON_FAILURE = on_failure
    Defaults.REQUEST_TIMEOUT = request_timeout
    Defaults.POLL_INTERVAL = poll_interval
    Defaults.MAXIMUM_POLL_TIME = maximum_poll_time
    Defaults.UNEXPECTED_EVENT_MAXIMUM_POLL_TIME = unexpected_event_maximum_poll_time
    Defaults.EXTENDED_EVENT_DEBUG_ON_EXPECTATION_FAILURE = (
        extended_event_debug_on_expectation_failure
    )
    Defaults.MAXIMUM_EVENTS_TO_OUTPUT = maximum_events_to_output
    Defaults.MAXIMUM_EXPECTATIONS_PER_EVENT_TO_OUTPUT = maximum_expectations_per_event_to_output


def get_default_on_failure() -> Callable:
    return Defaults.ON_FAILURE


def get_default_poll_interval() -> float:
    return Defaults.POLL_INTERVAL


def get_default_request_timeout() -> float:
    return Defaults.REQUEST_TIMEOUT


def get_default_maximum_poll_time() -> float:
    return Defaults.MAXIMUM_POLL_TIME


def get_default_unexpected_event_maximum_poll_time() -> float:
    return Defaults.UNEXPECTED_EVENT_MAXIMUM_POLL_TIME


def get_default_extended_event_debug_on_expectation_failure() -> bool:
    return Defaults.EXTENDED_EVENT_DEBUG_ON_EXPECTATION_FAILURE


def get_default_maximum_events_to_output() -> int:
    return Defaults.MAXIMUM_EVENTS_TO_OUTPUT


def get_default_expectations_per_event_to_output() -> int:
    return Defaults.MAXIMUM_EXPECTATIONS_PER_EVENT_TO_OUTPUT
