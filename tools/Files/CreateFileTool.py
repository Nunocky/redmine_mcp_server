from fastmcp.tools.tool import Tool
from tools.Files.create_file import create_file

CreateFileTool = Tool.from_function(
    create_file,
    name="create_file",
    description="Registers a new file in the specified Redmine project. Arguments: redmine_url, api_key, project_id, file.",
)
