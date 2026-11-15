from app.agent.decision import parse_action
from app.agent.planner import Planner
from app.errors import LLMOutputError
from app.llm.provider import MockLLMProvider


def test_mock_planner_returns_three_steps():
    items, response = Planner(MockLLMProvider()).plan("Tìm quy định", ("search_documents", "read_document"))
    assert len(items) == 3
    assert items[0].idx == 1
    assert response.provider == "mock"


def test_planner_discards_unallowed_tool_hint():
    items, _ = Planner(MockLLMProvider()).plan("Tìm quy định", ("search_documents",))
    assert items[2].tool_hint is None


def test_action_parser_rejects_unallowed_tool():
    try:
        parse_action(
            '{"kind":"tool","tool":"delete_all_documents","arguments":{}}',
            allowed_tools=("search_documents",),
            plan_idx=1,
        )
    except LLMOutputError:
        pass
    else:
        raise AssertionError("expected disallowed tool to be rejected")


def test_action_parser_accepts_finish():
    action = parse_action('{"kind":"finish","rationale":"enough"}', allowed_tools=("search_documents",), plan_idx=2)
    assert action.is_finish
    assert action.plan_idx == 2
