from fastmcp.tools.tool import Tool

from tools.Attachments.delete_attachment_tool import delete_attachment

DeleteAttachmentTool = Tool.from_function(
    delete_attachment,
    name="delete_attachment",
    description="Deletes an attachment from Redmine.",
)
