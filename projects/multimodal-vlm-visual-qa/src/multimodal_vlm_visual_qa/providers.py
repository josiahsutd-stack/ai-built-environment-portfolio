from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .schemas import StructuredExtraction, VQAResponse, validate_image_bytes


@dataclass
class MockVLMProvider:
    name: str = "mock-vlm"

    def answer(self, image_bytes: bytes, question: str) -> VQAResponse:
        image_type = validate_image_bytes(image_bytes)
        question_l = question.lower().strip()
        digest = hashlib.sha256(image_bytes[:2048]).hexdigest()[:8]
        extraction = StructuredExtraction(
            detected_objects=["image_region", "visual_layout", image_type],
            visible_text=["synthetic/mock OCR placeholder"] if "text" in question_l else [],
            defects=(
                ["possible surface scratch"]
                if "defect" in question_l or "scratch" in question_l
                else []
            ),
            key_values={"image_fingerprint": digest, "mode": "mock"},
        )
        if "json" in question_l or "extract" in question_l:
            answer = "Structured visual extraction completed in mock mode."
        elif "chart" in question_l or "trend" in question_l:
            answer = "The image appears to contain a visual pattern; mock mode reports a likely upward or highlighted trend if chart elements are present."
        else:
            answer = "Mock VLM analyzed the uploaded image and produced a cautious answer without claiming real visual recognition."
        uncertainty = "Mock mode does not inspect semantic image content; use a real VLM provider for production analysis."
        return VQAResponse(
            answer=answer,
            structured_json=extraction,
            confidence=0.62,
            uncertainty=uncertainty,
            observations=[
                f"Accepted {image_type} image bytes.",
                "Returned schema-constrained output.",
                "Confidence is intentionally conservative in mock mode.",
            ],
            provider=self.name,
        )


@dataclass
class LocalVLMProvider:
    name: str = "local-vlm-placeholder"

    def answer(self, image_bytes: bytes, question: str) -> VQAResponse:
        return MockVLMProvider(name=self.name).answer(image_bytes, question)


@dataclass
class OpenAICompatibleVLMProvider:
    name: str = "openai-compatible-vlm-placeholder"

    def answer(self, image_bytes: bytes, question: str) -> VQAResponse:
        return MockVLMProvider(name=self.name).answer(image_bytes, question)
