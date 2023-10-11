from modules.executors.basic.executors import BasicExecutor
from modules.executors.basic.errors import ErrorRule, ErrorRulesGroup, ProcessOutput

import re


class BashErrorRule(ErrorRule):
    """This class is used to define error rules that is compatible only with current executor"""


class NoCommand(BashErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This pattern will search for "command not found" at the end of string"""
        process_output.error = bool(
            re.search(r"command not found$", process_output.output, re.M | re.I)
        )

        return process_output.error


class UnboundVariable(BashErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This pattern will search for "unbound variable" at the end of string"""
        process_output.error = bool(
            re.search(r"unbound variable$", process_output.output, re.M | re.I)
        )

        return process_output.error


class LineError(BashErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This pattern will search for lines with something like ": line 666: syntax error" inside them"""
        search = re.search(r": line \d+: \w+ error", process_output.output, re.I)

        process_output.error = bool(search)
        # TODO: cover with test

        return process_output.error


class CannotExecuteError(BashErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This pattern will search for "cannot execute binary file" at the end of string"""

        process_output.error = bool(
            re.search(
                r"cannot execute binary file$", process_output.output, re.M | re.I
            )
        )

        # TODO: cover with test

        return process_output.error


class PermissionDenied(BashErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This pattern will search for "Permission denied" at the end of string"""

        process_output.error = bool(
            re.search(r"permission denied$", process_output.output, re.M | re.I)
        )
        # TODO: cover with test

        return process_output.error


class MissingLiteral(BashErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        """This pattern will search for "cannot execute binary file" at the end of string"""

        process_output.error = bool(
            re.search(r"bash: \D: missing `\D'", process_output.output, re.I)
        )
        # TODO: cover with test

        return process_output.error


class BashExecutor(BasicExecutor):
    override_checks = True  # To override check of binary
    execution_binary = ""  # Empty due to the fact that the implementation is using shell to execute other binaries

    file_extensions = (".sh", ".shell")
    error_rules_group = ErrorRulesGroup(BashErrorRule)
