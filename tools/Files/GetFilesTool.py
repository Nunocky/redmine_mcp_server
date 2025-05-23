from fastmcp.tools.tool import Tool
from tools.Files.get_files import get_files

GetFilesTool = Tool.from_function(
    get_files,
    name="get_files",
    description="Retrieves a list of files for the specified Redmine project. Arguments: redmine_url, api_key, project_id.",
)
