from fastmcp.tools.tool import Tool

from tools.Projects.archive_project_tool import archive_project

ArchiveProjectTool = Tool.from_function(
    archive_project,
    name="archive_project",
    description="Archive a Redmine project",
)
