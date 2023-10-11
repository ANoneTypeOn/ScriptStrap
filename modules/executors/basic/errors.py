from abc import ABC
from typing import Any

from modules.executors.basic.process import ProcessOutput


class ErrorRule(ABC):
    """Basic error rule class. Error rules is used to find errors in outputs."""

    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This method is used to check if given process_output contains something, that is satisfying current rule

        :return: Returns True if rule detected an error, otherwise returns False"""
        raise NotImplementedError("This method is not implemented by default")


class ErrorRulesGroup(ABC):
    participants: tuple[Any]

    def __init__(self, basic: Any):
        self.participants = tuple(basic.__subclasses__())

    def check(self, process_output: ProcessOutput) -> None:
        """This method is used to check if given process_output contains something, that is satisfying given rules"""
        for rule in self.participants:
            if rule.check(process_output):
                process_output.error = True
                break
