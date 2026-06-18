from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOCS = [
    "README.md",
    "profile-readme.md",
    "docs/general-ai-engineering-positioning.md",
    "docs/ai-skills-matrix.md",
    "docs/resume-project-bullets-general-ai.md",
    "docs/recruiter-snippets-general-ai.md",
    "docs/project-priority-roadmap.md",
    "portfolio-site/pages/skills-matrix.html",
    "portfolio-site/pages/recruiter-view.html",
]


def main() -> None:
    missing = [path for path in REQUIRED_DOCS if not (ROOT / path).exists()]
    project_missing = [
        str(project / "README.md")
        for project in sorted((ROOT / "projects").iterdir())
        if project.is_dir() and not (project / "README.md").exists()
    ]
    if missing or project_missing:
        details = "\n".join(missing + project_missing)
        raise SystemExit(f"Missing required documentation:\n{details}")
    print("Project documentation checks passed.")


if __name__ == "__main__":
    main()
