from fastmcp.tools.tool import Tool

from tools.Projects.create_project import create_project

CreateProjectTool = Tool.from_function(
    create_project,
    name="create_project",
    description="Create a Redmine project",
)
