from fastmcp.tools.tool import Tool

from tools.Attachments.upload_attachment import upload_attachment

UploadAttachmentTool = Tool.from_function(
    upload_attachment,
    name="upload_attachment",
    description="Redmineにファイルをアップロードし添付ファイルトークンを取得します",
)
