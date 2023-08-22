from modules.dataclasses.process import ProcessOutput

from abc import ABC
from typing import Iterable, Any

from os import PathLike


class BasicExecutor(ABC):
    file_extensions: tuple
    execution_binary: str | PathLike

    def execute(self, command: str, args: str | Iterable[Any] = "") -> ProcessOutput:
        raise NotImplementedError("This method is not implemented by default")

    def execute_many(
        self, cmds: Iterable[str | tuple[str, str]]
    ) -> tuple[ProcessOutput]:
        """This function is used to execute a lot of commands at once"""
        raise NotImplementedError("This method is not implemented by default")

    def execute_file(self, filepath: str | PathLike) -> ProcessOutput:
        """This function is used to execute a file with acceptable file extension"""
        raise NotImplementedError("This method is not implemented by default")

    def execute_many_files(
        self, filepaths: Iterable[str | PathLike]
    ) -> tuple[ProcessOutput]:
        """This function is used to execute a lot of files with acceptable file extensions"""
        raise NotImplementedError("This method is not implemented by default")

    @staticmethod
    def args_merger(target: Iterable[Any]) -> str:
        """This method is used to create string of args from list of unknown types.
        If value cannot be interpreted as string, then exception will be raised."""
        result = ""

        for obj in target:
            # Left without try-except to print output of original exception unchanged to simplify debugging
            result += str(obj)

        return result
