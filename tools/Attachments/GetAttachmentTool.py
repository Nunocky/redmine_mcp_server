from fastmcp.tools.tool import Tool

from tools.Attachments.get_attachment_tool import get_attachment

GetAttachmentTool = Tool.from_function(
    get_attachment,
    name="get_attachment",
    description="Retrieves Redmine attachment information.",
)
