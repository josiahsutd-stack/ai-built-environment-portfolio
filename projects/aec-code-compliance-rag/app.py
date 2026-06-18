from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.extend([str(PROJECT_ROOT / "src"), str(REPO_ROOT)])

import streamlit as st

from aec_code_compliance_rag import build_assistant_from_paths

st.set_page_config(page_title="AEC Code Compliance RAG", page_icon="AI", layout="wide")

st.title("AEC Code Compliance RAG Assistant")
st.caption("Synthetic demo data. Not legal, code, or professional compliance advice.")

docs = sorted((PROJECT_ROOT / "sample_data").glob("*.md"))
assistant = build_assistant_from_paths(docs)

question = st.text_input(
    "Ask a design-standard question",
    value="What clear width should be checked for high traffic accessible routes?",
)
k = st.slider("Retrieved sources", min_value=1, max_value=6, value=4)

if st.button("Answer", type="primary") or question:
    result = assistant.answer(question, k=k)
    st.subheader("Grounded answer")
    st.write(result["answer"])
    st.caption(
        f"Retrieved {result['retrieval']['result_count']} chunks "
        f"(top score {result['retrieval'].get('top_score', 0)})."
    )
    st.subheader("Sources")
    for source in result["sources"]:
        title = (
            f"{source['citation_id']} | {source['heading']} | "
            f"{source['clause_id']} | score {source['score']}"
        )
        with st.expander(title):
            st.write(source["reference"])
            st.write(f"Chunk: `{source['chunk_id']}`")
            if source["page"]:
                st.write(f"Demo page marker: {source['page']}")
            st.write(source["excerpt"])
