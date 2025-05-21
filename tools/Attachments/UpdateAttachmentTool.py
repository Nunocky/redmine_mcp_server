from fastmcp.tools.tool import Tool

from tools.Attachments.update_attachment import update_attachment

UpdateAttachmentTool = Tool.from_function(
    update_attachment,
    name="update_attachment",
    description="Updates Redmine attachment information (PATCH).",
)
