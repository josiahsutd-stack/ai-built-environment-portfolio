from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.extend([str(PROJECT_ROOT / "src"), str(REPO_ROOT)])

from aec_code_compliance_rag.public_sources import download_public_sources  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Singapore public AEC source corpus.")
    parser.add_argument("--force", action="store_true", help="Re-download existing files.")
    args = parser.parse_args()
    report = download_public_sources(
        PROJECT_ROOT / "public_sources" / "sources.json", force=args.force
    )
    print(json.dumps(report, indent=2))
    if report["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
