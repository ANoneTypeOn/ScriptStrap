import subprocess

from modules.dataclasses.process import ProcessOutput


def execute(command: str, args: str = "") -> ProcessOutput:
    command_ready = f"{command} {args}"
    output = subprocess.run(command_ready, shell=True, capture_output=True)

    if output.stderr is None:
        return ProcessOutput(command=command_ready, error=output.stderr, output=output.stdout.decode())

    return ProcessOutput(command=command_ready, error=None, output=output.stdout.decode())
