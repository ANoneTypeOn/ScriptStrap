from modules.executors.basic.executors import BasicExecutor
from modules.executors.basic.errors import ErrorRule, ErrorRulesGroup, ProcessOutput

import re


class PHPErrorRule(ErrorRule):
    """This class is used to define error rules that is compatible only with current executor"""


class ExceptionOccurred(PHPErrorRule):
    @staticmethod
    def check(process_output: ProcessOutput) -> bool:
        process_output.error = bool(
            re.search(r"PHP \D error:", process_output.output).group(0)
        )

        # TODO: cover with test

        return process_output.error


class PHPExecutor(BasicExecutor):
    file_extensions = (".php", ".php4", ".php5", ".phtml", ".ctp")
    execution_binary = "/usr/bin/php"
    error_rules_group = ErrorRulesGroup(PHPErrorRule)
