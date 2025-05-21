from fastmcp.tools.tool import Tool

from tools.Projects.update_project import update_project

UpdateProjectTool = Tool.from_function(
    update_project,
    name="update_project",
    description="Update Redmine project information",
)
