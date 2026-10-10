"""Created by JXP and Claude.

Refresh the "Our footprint" page: download the development repository's
``Logs/log_summary.csv`` from its ``main`` branch and regenerate the Bokeh
HTML into ``docs/_static/footprint/``. Runs before ``sphinx-build`` locally and
in CI (``.github/workflows/deploy.yml``).

Design rule: this script must never fail the site build. If the download
fails, the committed CSV snapshot is used; if plotting fails, the committed
HTML is left untouched. The exit code is 0 unless no HTML exists at all.

Usage::

    python scripts/build_footprint.py [--offline]
"""

import argparse
import csv
import io
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE_ROOT = HERE.parent
OUT_DIR = SITE_ROOT / "docs" / "_static" / "footprint"
CSV_PATH = OUT_DIR / "log_summary.csv"
HTML_PATH = OUT_DIR / "token_usage_and_co2_emissions.html"

CSV_URL = ("https://raw.githubusercontent.com/Sea-Meets-the-Stars/"
           "ClimateIntelligence/main/Logs/log_summary.csv")
EXPECTED_HEADER = ["ut_time", "tokens_used", "model", "co2_grams_estimate"]
TIMEOUT_S = 30


def fetch_csv(url=CSV_URL, dest=CSV_PATH):
    """Created by JXP and Claude.

    Download the summary CSV and replace ``dest`` only if the download looks
    like the real table (expected header, at least one row).

    Inputs: url (str), dest (Path). Output: True if dest was updated.
    """
    with urllib.request.urlopen(url, timeout=TIMEOUT_S) as resp:
        text = resp.read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or rows[0] != EXPECTED_HEADER or len(rows) < 2:
        raise ValueError(f"unexpected CSV content from {url}: header={rows[:1]}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Write atomically so a half-written file never replaces the snapshot.
    with tempfile.NamedTemporaryFile("w", dir=dest.parent, delete=False,
                                     suffix=".tmp", encoding="utf-8") as tmp:
        tmp.write(text)
    shutil.move(tmp.name, dest)
    dest.chmod(0o644)  # NamedTemporaryFile creates 0600; keep the snapshot world-readable
    return True


def build_html(csv_path=CSV_PATH, html_path=HTML_PATH):
    """Created by JXP and Claude.

    Run the copied Bokeh script's ``build_dashboard`` on ``csv_path`` and
    write ``html_path``. Inputs: paths. Output: the written Path.
    """
    sys.path.insert(0, str(HERE))
    from token_usage_and_co2_emissions import build_dashboard  # noqa: E402
    return build_dashboard(csv_path, html_path)


def main():
    """Created by JXP and Claude. Fetch, then plot; degrade gracefully."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    parser.add_argument("--offline", action="store_true",
                        help="skip the download and plot the committed CSV")
    args = parser.parse_args()

    if not args.offline:
        try:
            fetch_csv()
            print(f"[footprint] downloaded {CSV_URL}")
        except Exception as exc:  # network, 404, bad content: keep the snapshot
            print(f"[footprint] WARNING: download failed ({exc}); using committed CSV",
                  file=sys.stderr)

    try:
        written = build_html()
        print(f"[footprint] wrote {written}")
    except Exception as exc:
        print(f"[footprint] WARNING: plot failed ({exc}); keeping committed HTML",
              file=sys.stderr)

    if not HTML_PATH.exists():
        print("[footprint] ERROR: no footprint HTML available", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
