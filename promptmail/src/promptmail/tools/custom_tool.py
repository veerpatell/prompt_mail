from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from typing import ClassVar

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."



class InputTool(BaseTool):
    name: ClassVar[str] = "get_input"
    description: str = "Prompt the user for input."

    def _run(self, prompt: str) -> str:
        return input(prompt)

input_tool = InputTool()
