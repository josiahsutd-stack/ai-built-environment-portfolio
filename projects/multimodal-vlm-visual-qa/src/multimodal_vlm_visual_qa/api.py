from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .providers import MockVLMProvider

app = FastAPI(title="Multimodal VLM Visual QA")


class VQARequest(BaseModel):
    image_base64_placeholder: str
    question: str


@app.post("/analyze")
def analyze(payload: VQARequest) -> dict[str, object]:
    image_bytes = b"\x89PNG\r\n\x1a\n" + payload.image_base64_placeholder.encode()
    return MockVLMProvider().answer(image_bytes, payload.question).model_dump()
