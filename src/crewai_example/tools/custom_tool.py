from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
from sandboxai import Sandbox


class RunIPythonCellArgs(BaseModel):
    code: str = Field(..., description="The code to execute.")
    dependencies: List[str] = Field(..., description="List of python dependencies needed to execute the code.")

class RunIPythonCell(BaseTool):
    name: str = "Run"
    description: str = (
        "Run python and shell commands in an ipython cell. Shell commands should be on a new line and start with a !."
    )
    args_schema: Type[BaseModel] = RunIPythonCellArgs

    def _run(self, code: str, dependencies: List[str]) -> str:
        if dependencies:
            deps_string = ' '.join(dependencies)
            code_with_deps =f"! pip install {deps_string}\n{code}"
        with Sandbox(embedded=True) as sb:
            result = sb.run_ipython_cell(input=code_with_deps)
            return result.output

class RunShellCommandArgs(BaseModel):
    command: str = Field(..., description="The bash commands to execute.")

class RunShellCommand(BaseTool):
    name: str = "Run"
    description: str = (
        "Run bash shell commands in a sandbox."
    )
    args_schema: Type[BaseModel] = RunShellCommandArgs

    def _run(self, command: str) -> str:
        with Sandbox(embedded=True) as sb:
            result = sb.run_shell_command(command=command)
            return result.output

class RunGCloudCommandArgs(BaseModel):
    command: str = Field(..., description="The bash commands to execute.")

class RunGCloudCommand(BaseTool):
    name: str = "Run"
    description: str = (
        "Run gcloud commands in a sandbox. gcloud is already installed. You can run it for example like this `gcloud --help`"
    )
    args_schema: Type[BaseModel] = RunGCloudCommandArgs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sandbox = Sandbox(embedded=True, image="substratusai/sandboxai-gcloudbox")

    def _run(self, command: str) -> str:
        result = self._sandbox.run_shell_command(command=command)
        return result.output
