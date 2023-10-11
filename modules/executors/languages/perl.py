from modules.executors.basic.executors import BasicExecutor
from modules.executors.basic.errors import ErrorRule, ErrorRulesGroup, ProcessOutput

import re


class PerlErrorRule(ErrorRule):
    """This class is used to define error rules that is compatible only with current executor"""


# TODO: Add errors
class ExceptionOccurred(PerlErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        process_output.error = process_output.output.startswith(
            "Traceback (most recent call last):"
        )

        # TODO: cover with test

        return process_output.error


class PearlExecutor(BasicExecutor):
    file_extensions = (".pl", ".pm", ".pod", ".t", ".PL", ".psgi")
    execution_binary = "/usr/bin/perl"
    error_rules_group = ErrorRulesGroup(PerlErrorRule)
