from app.tools.base import ReadOnlyTool
from app.tools.document_search import DocumentSearchTool
from app.tools.http_get_api import HttpGetApiTool


def test_registered_tool_types_are_read_only() -> None:
    assert issubclass(DocumentSearchTool, ReadOnlyTool)
    assert issubclass(HttpGetApiTool, ReadOnlyTool)
    assert not hasattr(DocumentSearchTool, "write")
    assert not hasattr(HttpGetApiTool, "write")
