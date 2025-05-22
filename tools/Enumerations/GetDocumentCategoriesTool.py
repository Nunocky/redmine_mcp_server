from fastmcp.tools.tool import Tool

from tools.Enumerations.get_document_categories import get_document_categories

GetDocumentCategoriesTool = Tool.from_function(
    get_document_categories,
    name="get_document_categories",
    description="Retrieves a list of document categories from Redmine.",
)
