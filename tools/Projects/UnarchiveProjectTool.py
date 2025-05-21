from fastmcp.tools.tool import Tool

from tools.Projects.unarchive_project import unarchive_project

UnarchiveProjectTool = Tool.from_function(
    unarchive_project,
    name="unarchive_project",
    description="Unarchive a Redmine project",
)
