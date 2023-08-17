from dataclasses import dataclass


@dataclass(slots=True, eq=False, repr=False)
class ProcessOutput:
    command: str

    error: str | None
    output: str | None


# This class should be used when there's no error occurred and output have positive results
@dataclass(slots=True, eq=False, repr=False)
class SanitizedProcessOutput:
    command: str
    output: str
