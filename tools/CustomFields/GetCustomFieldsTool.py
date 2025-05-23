from fastmcp.tools.tool import Tool

from tools.CustomFields.get_custom_fields import get_custom_fields

GetCustomFieldsTool = Tool.from_function(
    get_custom_fields,
    name="get_custom_fields",
    description="Get Redmine custom fields definitions",
)
