from fastmcp.tools.tool import Tool

from tools.Projects.delete_project import delete_project

DeleteProjectTool = Tool.from_function(
    delete_project,
    name="delete_project",
    description="Delete a Redmine project",
)
