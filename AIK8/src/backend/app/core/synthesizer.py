from app.evidence.models import Evidence
from app.llm.provider import LLMProvider


class ReportSynthesizer:
    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    async def synthesize(self, question: str, evidence: tuple[Evidence, ...]) -> str:
        draft = await self.provider.synthesize(question, evidence)
        available_ids = {item.id for item in evidence}
        citations = {citation for citation in draft.split() if citation.startswith("[E")}
        invalid = citations - {f"[{item}]" for item in available_ids}
        if invalid:
            raise ValueError(f"Report contains citations without evidence: {', '.join(sorted(invalid))}")
        return draft
