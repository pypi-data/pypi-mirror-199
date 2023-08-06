"""Error types used by the library"""
from typing import List, Dict
from tes_lib.constants import EVENT_SOURCE_KEY, EVENT_TYPE_KEY, EVENT_ID_KEY
from tes_lib.expectation import Expectation, PartialMatch
from tes_lib.formatting import indentation


class TesLibError(RuntimeError):
    """Raised when an expected library error occurs"""

    pass


class ExpectationError(AssertionError):
    """Raised when the provided expectations are not valid"""

    pass


class EventNotFoundError(AssertionError):
    """Raised when an expected event was not found"""

    def __init__(self, expectations):
        self.message = "Failed to find an event for the {} expectations provided.".format(
            len(expectations)
        )
        self.expectations = expectations

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class ExtendedEventNotFoundError(EventNotFoundError):
    """Raised when an expected event was not found"""

    def __init__(
        self,
        expectations: List[Expectation],
        extended_event_debug_info: List[PartialMatch],
        maximum_events_to_output: int,
        maximum_expectations_per_event_to_output: int,
    ):
        super().__init__(expectations)
        self.extended_event_debug_info = extended_event_debug_info
        self.maximum_errors_to_output = maximum_events_to_output
        self.maximum_expectations_per_event_to_output = maximum_expectations_per_event_to_output

    def __str__(self) -> str:
        msg = super().__str__()

        event_source_string = ""
        event_type_string = ""
        for expectation in self.expectations:
            if expectation.event_field_name == EVENT_SOURCE_KEY:
                event_source_string = "\n{}Expected event source: {}.".format(
                    indentation(1), expectation.comparison_value
                )

            if expectation.event_field_name == EVENT_TYPE_KEY:
                event_type_string = "\n{}Expected event type: {}.".format(
                    indentation(1), expectation.comparison_value
                )

        msg += event_source_string + event_type_string

        output = 0

        if len(self.extended_event_debug_info) > 0:
            msg += "\n"

            for event_debug in self.extended_event_debug_info:
                msg += "\n{}Event ID: {}".format(indentation(1), event_debug.event[EVENT_ID_KEY])
                event_count = 0
                for expectation_failure in event_debug.expectation_failures:
                    msg += "\n{}{}".format(indentation(2), expectation_failure)

                    event_count += 1

                    if event_count >= self.maximum_expectations_per_event_to_output:
                        break

                if (
                    len(event_debug.expectation_failures)
                    > self.maximum_expectations_per_event_to_output
                ):
                    extra_expectations = (
                        len(event_debug.expectation_failures)
                        - self.maximum_expectations_per_event_to_output
                    )
                    plural = ""
                    if extra_expectations > 1:
                        plural = "s"

                    msg += "\n{}{} more failing expectation{} ...".format(
                        indentation(2), extra_expectations, plural
                    )

                output += 1

                if output >= self.maximum_errors_to_output:
                    break

            if output >= self.maximum_errors_to_output:
                extra_events = len(self.extended_event_debug_info) - self.maximum_errors_to_output
                plural = ""
                if extra_events > 1:
                    plural = "s"
                msg += "\n{}{} more partially matched event{} ...".format(
                    indentation(1), extra_events, plural
                )

        msg += "\n\nSee the logging output for full details"

        return msg


class UnexpectedEventFoundError(AssertionError):
    """Raised when an unexpected event is found"""

    def __init__(
        self,
        expectations: List[Expectation],
        unexpected_event: Dict,
    ):
        super().__init__("An unexpected event matching the expectations was found with event id:")
        self.expectations = expectations
        self.unexpected_event = unexpected_event

    def __str__(self) -> str:
        msg = super().__str__()
        msg += " {}".format(self.unexpected_event[EVENT_ID_KEY])

        for expectation in self.expectations:
            msg += "\n{}{}".format(indentation(1), expectation)

        return msg
