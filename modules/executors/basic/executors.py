import subprocess
import os

from typing import Iterable, Any

from modules.executors.basic.errors import ErrorRulesGroup
from modules.executors.basic.process import ProcessOutput


class BasicExecutor:
    file_extensions: tuple
    execution_binary: str | os.PathLike

    # TODO: Find way to define basic ErrorRulesGroup class as typehint without warnings
    error_rules_group: ErrorRulesGroup
    override_checks: bool = False

    def __init__(self):
        if self.override_checks:
            return

        if os.access(self.execution_binary, os.X_OK):
            raise PermissionError(
                f"Binary {self.execution_binary} is not executable. Executor is ignored."
            )

    def execute(self, command: str, args: str | Iterable[Any] = "") -> ProcessOutput:
        """This function is used to execute single commands"""
        command_ready = f"{self.execution_binary} {command} {self.args_merger(args)}"
        executed = subprocess.run(command_ready, shell=True, capture_output=True)

        return ProcessOutput(
            command=command_ready,
            output=executed,
            error_rules_group=self.error_rules_group,
        )

    def execute_many(
        self, cmds: Iterable[str | tuple[str, str]]
    ) -> tuple[ProcessOutput]:
        """This method is used to execute a lot of commands at once"""
        result = []

        for pos, cmd in enumerate(cmds):
            if isinstance(cmd, str):
                result.append(self.execute(cmd))

            elif isinstance(cmd, tuple):
                result.append(self.execute(cmd[0], cmd[1:]))

            else:
                raise ValueError(
                    f"""Arg "cmds" contains invalid value on position "{pos}": {cmd}"""
                )

        return tuple(result)

    def execute_file(self, filepath: str | os.PathLike) -> ProcessOutput:
        """This method is used to execute a file"""
        command_ready = f"{self.execution_binary} {filepath}"
        executed = subprocess.run(command_ready, shell=True, capture_output=True)

        return ProcessOutput(
            command=command_ready,
            error_rules_group=self.error_rules_group,
            output=executed,
        )

    def execute_many_files(
        self, filepaths: Iterable[str | os.PathLike]
    ) -> tuple[ProcessOutput]:
        """This method is used to execute a lot of languages at once"""
        return tuple(map(self.execute_file, filepaths))

    @staticmethod
    def args_merger(target: Iterable[Any]) -> str:
        """This method is used to create string of args from list of unknown types.
        If value cannot be interpreted as string, then exception will be raised."""
        result = ""

        for obj in target:
            # Left without try-except to print output of original exception unchanged to simplify debugging
            result += str(obj) + "\n"

        return result
