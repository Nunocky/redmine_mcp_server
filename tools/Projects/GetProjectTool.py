from fastmcp.tools.tool import Tool

from tools.Projects.get_project_tool import get_project

GetProjectTool = Tool.from_function(
    get_project,
    name="get_project",
    description="Get Redmine project information",
)
