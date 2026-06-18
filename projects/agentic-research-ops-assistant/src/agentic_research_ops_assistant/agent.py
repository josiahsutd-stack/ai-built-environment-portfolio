from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from shared.ai import TfidfVectorStore, get_llm_provider


class ToolCall(BaseModel):
    name: str
    args: dict[str, str] = Field(default_factory=dict)
    output: str


class AgentTrace(BaseModel):
    task: str
    plan: list[str]
    tool_calls: list[ToolCall]
    citations: list[str]
    approval_required: bool
    final_report: str


class ResearchAgent:
    def __init__(self, docs_dir: str | Path, memory_path: str | Path | None = None) -> None:
        self.docs_dir = Path(docs_dir)
        self.memory_path = Path(memory_path or self.docs_dir.parent / "agent_memory.json")
        self.provider = get_llm_provider()
        self.docs = {
            path.name: path.read_text(encoding="utf-8") for path in self.docs_dir.glob("*.md")
        }
        self.store = TfidfVectorStore()
        self.store.add_texts(self.docs.values(), sources=self.docs.keys())

    def plan(self, task: str) -> list[str]:
        return [
            "search_local_docs",
            "summarize_document",
            "extract_entities",
            "compare_sources",
            "create_report",
            "ask_human_approval",
            "save_memory",
        ]

    def search_local_docs(self, query: str) -> list[tuple[str, str]]:
        return [(result.source, result.text) for result in self.store.search(query, k=3)]

    def summarize_document(self, text: str) -> str:
        return text.strip().replace("\n", " ")[:360]

    def extract_entities(self, text: str) -> list[str]:
        keywords = ["AI", "deployment", "multimodal", "model", "workflow", "monitoring", "edge"]
        return [keyword for keyword in keywords if keyword.lower() in text.lower()]

    def compare_sources(self, sources: list[tuple[str, str]]) -> str:
        names = ", ".join(source for source, _text in sources) or "no sources"
        return f"Compared evidence from: {names}."

    def create_report(self, task: str, sources: list[tuple[str, str]]) -> str:
        evidence = "\n".join(
            f"- {source}: {self.summarize_document(text)}" for source, text in sources
        )
        return f"# Research Brief\n\nTask: {task}\n\n## Cited Findings\n\n{evidence}\n\n## Recommendation\n\nUse the cited evidence as a starting point and request human approval before finalizing."

    def ask_human_approval(self) -> str:
        return "Human approval required before sending or publishing the report."

    def save_memory(self, trace: AgentTrace) -> None:
        self.memory_path.write_text(trace.model_dump_json(indent=2), encoding="utf-8")

    def retrieve_memory(self) -> dict[str, object]:
        if not self.memory_path.exists():
            return {}
        return json.loads(self.memory_path.read_text(encoding="utf-8"))

    def run(self, task: str) -> AgentTrace:
        plan = self.plan(task)
        sources = self.search_local_docs(task)
        tool_calls = [
            ToolCall(
                name="search_local_docs", args={"query": task}, output=f"{len(sources)} sources"
            ),
            ToolCall(
                name="summarize_document", output="Summaries generated for retrieved documents."
            ),
            ToolCall(
                name="extract_entities",
                output=", ".join(self.extract_entities(" ".join(t for _, t in sources))),
            ),
            ToolCall(name="compare_sources", output=self.compare_sources(sources)),
        ]
        report = self.create_report(task, sources)
        tool_calls.append(ToolCall(name="create_report", output=report[:160]))
        tool_calls.append(ToolCall(name="ask_human_approval", output=self.ask_human_approval()))
        trace = AgentTrace(
            task=task,
            plan=plan,
            tool_calls=tool_calls,
            citations=[source for source, _text in sources],
            approval_required=True,
            final_report=report,
        )
        self.save_memory(trace)
        return trace


def run_research_task(task: str, docs_dir: str | Path) -> AgentTrace:
    return ResearchAgent(docs_dir).run(task)
