from subprocess import CompletedProcess

from dataclasses import dataclass
from typing import Any, Optional


class ProcessOutput:
    __slots__ = ("command", "error", "output", "error_rules_group")

    command: str

    error: bool
    output: str

    error_rules_group: Any

    def __init__(
        self,
        command: str,
        output: CompletedProcess,
        error_rules_group: Optional[Any] = None,
    ):
        self.command = command
        self.error = False
        self.output = (output.stderr or output.stdout).decode()
        self.error_rules_group = error_rules_group

        if output.returncode != 0:
            self.error = True

        elif error_rules_group is not None:
            error_rules_group.check(self)


# This class should be used when there's no error occurred and output have positive results
@dataclass(slots=True, eq=False, repr=False)
class SanitizedProcessOutput:
    command: str
    output: str
