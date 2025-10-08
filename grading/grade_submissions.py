import argparse
import io
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import nbformat
import requests


GITHUB_ZIP_CANDIDATES = (
    "{base}/archive/refs/heads/main.zip",
    "{base}/archive/refs/heads/master.zip",
)


def normalize_repo_base_url(repo_url: str) -> str:
    """Return canonical GitHub repo base URL without trailing slash.

    Examples:
    - https://github.com/user/repo -> https://github.com/user/repo
    - https://github.com/user/repo/ -> https://github.com/user/repo
    - git@github.com:user/repo.git -> https://github.com/user/repo
    """
    url = repo_url.strip()
    if url.endswith(".git"):
        url = url[:-4]
    if url.startswith("git@github.com:"):
        # Convert SSH form to https
        user_repo = url.split(":", 1)[1]
        url = f"https://github.com/{user_repo}"
    url = url.rstrip("/")
    return url


def build_zip_urls(repo_url: str) -> List[str]:
    base = normalize_repo_base_url(repo_url)
    return [candidate.format(base=base) for candidate in GITHUB_ZIP_CANDIDATES]


def download_repo_zip(repo_url: str, timeout: int = 30) -> Tuple[Path, str]:
    """Download the repository as a zip, trying common branches.

    Returns (zip_path, resolved_zip_url). Raises RuntimeError on failure.
    """
    errors: List[str] = []
    for zip_url in build_zip_urls(repo_url):
        try:
            resp = requests.get(zip_url, timeout=timeout, stream=True)
            if resp.status_code == 200:
                tmp_fd, tmp_path = tempfile.mkstemp(suffix=".zip", prefix="repo_")
                os.close(tmp_fd)
                with open(tmp_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 128):
                        if chunk:
                            f.write(chunk)
                return Path(tmp_path), zip_url
            errors.append(f"{zip_url} -> HTTP {resp.status_code}")
        except Exception as exc:  # noqa: BLE001 broad but intentional for CLI resilience
            errors.append(f"{zip_url} -> {exc}")
    raise RuntimeError(
        "Could not download repository zip. Tried: " + "; ".join(errors)
    )


def extract_zip(zip_path: Path) -> Path:
    extract_dir = Path(tempfile.mkdtemp(prefix="repo_extract_"))
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    return extract_dir


def find_notebooks(root: Path) -> List[Path]:
    notebooks: List[Path] = []
    for path in root.rglob("*.ipynb"):
        # Skip checkpoints or hidden
        if ".ipynb_checkpoints" in path.parts:
            continue
        notebooks.append(path)
    return notebooks


def load_notebook_cells(nb_path: Path) -> List[str]:
    try:
        with nb_path.open("r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        sources: List[str] = []
        for cell in nb.cells:
            if cell.get("cell_type") == "code":
                src = cell.get("source") or ""
                if isinstance(src, list):
                    sources.append("".join(src))
                else:
                    sources.append(str(src))
        return sources
    except Exception:
        return []


API_HINT_PATTERNS = [
    re.compile(r"/breweries", re.I),
    re.compile(r"openbrewerydb", re.I),
    re.compile(r"178\.156\.206\.171:8000", re.I),
    re.compile(r"requests\s*\.\s*get\s*\(.*http", re.I),
]

PROCESSING_HINT_PATTERNS = [
    re.compile(r"response\s*\.\s*json\s*\(", re.I),
    re.compile(r"json\s*\(", re.I),
    re.compile(r"pandas", re.I),
    re.compile(r"for\s+.*in\s+.*:", re.I),
    re.compile(r"print\s*\(.*(name|city|state)", re.I),
]


def evaluate_notebooks(notebook_paths: List[Path]) -> Dict[str, object]:
    """Return rubric evaluation details and total score.

    Rubric (100 points total):
    - Notebooks present: 40 pts (>=1 .ipynb)
    - API usage detected: 40 pts (any API hint pattern in any code cell)
    - Basic processing present: 20 pts (any processing hint pattern)
    """
    details: Dict[str, object] = {
        "notebooks_found": len(notebook_paths),
        "api_usage_detected": False,
        "basic_processing_detected": False,
        "matched_api_examples": [],
        "matched_processing_examples": [],
    }

    score = 0

    # Notebooks present
    if notebook_paths:
        score += 40

    # Scan cells for signals
    matched_api: List[str] = []
    matched_processing: List[str] = []
    for nb_path in notebook_paths:
        for src in load_notebook_cells(nb_path):
            for pat in API_HINT_PATTERNS:
                m = pat.search(src)
                if m:
                    details["api_usage_detected"] = True
                    snippet = src[max(0, m.start() - 30) : m.end() + 30]
                    matched_api.append(snippet.strip())
            for pat in PROCESSING_HINT_PATTERNS:
                m = pat.search(src)
                if m:
                    details["basic_processing_detected"] = True
                    snippet = src[max(0, m.start() - 30) : m.end() + 30]
                    matched_processing.append(snippet.strip())

    if details["api_usage_detected"]:
        score += 40
    if details["basic_processing_detected"]:
        score += 20

    details["matched_api_examples"] = matched_api[:5]
    details["matched_processing_examples"] = matched_processing[:5]
    details["score_total"] = score
    details["score_breakdown"] = {
        "notebooks_present": 40 if notebook_paths else 0,
        "api_usage": 40 if details["api_usage_detected"] else 0,
        "basic_processing": 20 if details["basic_processing_detected"] else 0,
    }
    return details


def grade_repo(repo_url: str, timeout: int = 30) -> Dict[str, object]:
    temp_paths: List[Path] = []
    try:
        zip_path, resolved = download_repo_zip(repo_url, timeout=timeout)
        temp_paths.append(zip_path)
        extract_dir = extract_zip(zip_path)
        temp_paths.append(extract_dir)

        # Root of the extracted repo is usually a single subfolder
        candidates = [p for p in extract_dir.iterdir() if p.is_dir()]
        repo_root = candidates[0] if candidates else extract_dir

        notebooks = find_notebooks(repo_root)
        eval_details = evaluate_notebooks(notebooks)

        return {
            "repo_url": repo_url,
            "zip_url": resolved,
            "notebook_paths": [str(p.relative_to(repo_root)) for p in notebooks],
            "result": eval_details,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "repo_url": repo_url,
            "error": str(exc),
            "result": {
                "notebooks_found": 0,
                "api_usage_detected": False,
                "basic_processing_detected": False,
                "matched_api_examples": [],
                "matched_processing_examples": [],
                "score_total": 0,
                "score_breakdown": {
                    "notebooks_present": 0,
                    "api_usage": 0,
                    "basic_processing": 0,
                },
            },
        }
    finally:
        # Clean up temporary files
        for p in temp_paths:
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink(missing_ok=True)
            except Exception:
                pass


def write_outputs(results: List[Dict[str, object]], out_dir: Path, out_format: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    if out_format in ("json", "both"):
        json_path = out_dir / "grading_results.json"
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    if out_format in ("csv", "both"):
        # Minimal CSV: repo_url, score_total, notebooks_found, api_usage, basic_processing
        import csv

        csv_path = out_dir / "grading_results.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "repo_url",
                    "score_total",
                    "notebooks_found",
                    "api_usage_detected",
                    "basic_processing_detected",
                ]
            )
            for r in results:
                res = r.get("result", {})
                writer.writerow(
                    [
                        r.get("repo_url", ""),
                        res.get("score_total", 0),
                        res.get("notebooks_found", 0),
                        res.get("api_usage_detected", False),
                        res.get("basic_processing_detected", False),
                    ]
                )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Grade one or more GitHub repositories for BADM 554 Lab 4 notebooks"
    )
    parser.add_argument(
        "--urls",
        nargs="*",
        help="One or more GitHub repository URLs (e.g., https://github.com/user/repo)",
    )
    parser.add_argument(
        "--urls-file",
        type=str,
        help="Path to a text file with one GitHub repo URL per line",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Download timeout in seconds (per repo)",
    )
    parser.add_argument(
        "--out",
        choices=["json", "csv", "both"],
        default="both",
        help="Output format to write to the ./grading_results directory",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    urls: List[str] = []
    if args.urls:
        urls.extend(args.urls)
    if args.urls_file:
        with open(args.urls_file, "r", encoding="utf-8") as f:
            urls.extend([line.strip() for line in f if line.strip()])

    urls = [u for u in urls if u]
    if not urls:
        print("No repository URLs provided. Use --urls or --urls-file.", file=sys.stderr)
        return 2

    results: List[Dict[str, object]] = []
    for url in urls:
        print(f"Grading: {url} ...")
        result = grade_repo(url, timeout=args.timeout)
        results.append(result)
        score = result.get("result", {}).get("score_total", 0)
        print(f"  -> Score: {score}")

    # Print summary to stdout
    print("\nSummary:")
    for r in results:
        print(
            f"- {r.get('repo_url')}: {r.get('result', {}).get('score_total', 0)}"
        )

    # Write outputs to disk inside the grading/ directory
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir / "grading_results"
    write_outputs(results, out_dir, args.out)
    print(f"\nWrote results to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


