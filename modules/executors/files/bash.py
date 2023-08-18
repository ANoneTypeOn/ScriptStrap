import subprocess
from typing import Iterable, Any

from modules.dataclasses.process import ProcessOutput


class BashModule:
    def execute(self, command: str, args: str | Iterable[Any] = "") -> ProcessOutput:
        """This function is used to execute single commands"""
        command_ready = f"{command} {self.iterable_to_str(args)}"
        executed = subprocess.run(command_ready, shell=True, capture_output=True)

        output = executed.stdout.decode() or executed.stderr.decode()

        if output is None or output == "":
            return ProcessOutput(command=command_ready, error=True, output=output)

        return ProcessOutput(command=command_ready, error=False, output=output)

    def execute_many(
        self, cmds: Iterable[str | tuple[str, str]]
    ) -> tuple[ProcessOutput]:
        """This function will"""
        result = []

        for cmd in cmds:
            if isinstance(cmd, str):
                result.append(self.execute(cmd))

            elif isinstance(cmd, tuple):
                result.append(self.execute(cmd[0], cmd[1:]))

            else:
                raise ValueError(f"""Argument "cmds" contains invalid value: {cmd}""")

        return tuple(result)

    @staticmethod
    def iterable_to_str(target: Iterable[Any]) -> str:
        """This method is used to create string of args from list of unknown types.
        If value cannot be interpreted as string, then exception will be raised."""
        result = ""

        for obj in target:
            # Left without try-except to print output of original exception unchanged to simplify debugging
            result += str(obj)

        return result
