import subprocess
from typing import Iterable, Any
from os import PathLike

from modules.dataclasses.process import ProcessOutput
from modules.executors.base.basic import BasicExecutor


class BashModule(BasicExecutor):
    file_extensions = (".sh", ".shell")
    execution_binary = "/usr/bin/bash"

    def execute(self, command: str, args: str | Iterable[Any] = "") -> ProcessOutput:
        """This function is used to execute single commands"""
        command_ready = f"{command} {self.args_merger(args)}"
        executed = subprocess.run(command_ready, shell=True, capture_output=True)

        output = executed.stdout.decode() or executed.stderr.decode()

        return ProcessOutput(command=command_ready, error=False, output=output)

    def execute_many(
        self, cmds: Iterable[str | tuple[str, str]]
    ) -> tuple[ProcessOutput]:
        """This function is used to execute a lot of commands at once"""
        result = []

        for cmd in cmds:
            if isinstance(cmd, str):
                result.append(self.execute(cmd))

            elif isinstance(cmd, tuple):
                result.append(self.execute(cmd[0], cmd[1:]))

            else:
                raise ValueError(f"""Argument "cmds" contains invalid value: {cmd}""")

        return tuple(result)

    def execute_file(self, filepath: str | PathLike) -> ProcessOutput:
        command_ready = f"{self.execution_binary} {filepath}"
        executed = subprocess.run(command_ready, shell=True, capture_output=True)

        output = executed.stdout.decode() or executed.stderr.decode()

        # TODO: Implement ErrorRules
        return ProcessOutput(command=command_ready, error=False, output=output)

    def execute_many_files(
        self, filepaths: Iterable[str | PathLike]
    ) -> tuple[ProcessOutput]:
        return tuple(map(self.execute_file, filepaths))
