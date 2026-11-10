"""Validate a two-wave survey CSV and write a group-level Markdown report."""
import argparse
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ("wave", "site", "question", "response_id", "score")
WAVES = ("Baseline", "Follow-up")


def summarize(source, minimum=5):
    if minimum < 2:
        raise ValueError("The minimum group size must be at least two.")
    with sqlite3.connect(":memory:") as db, Path(source).open(newline="", encoding="utf-8") as handle:
        db.execute("""CREATE TABLE response (
            wave TEXT, site TEXT, question TEXT, response_id TEXT,
            score INTEGER CHECK(score BETWEEN 1 AND 5),
            PRIMARY KEY (wave, site, question, response_id)
        )""")
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("The input header does not match the five documented fields.")
        for line, record in enumerate(reader, 2):
            if None in record or any(not (record[key] or "").strip() for key in FIELDS):
                raise ValueError(f"Missing or extra field on input line {line}.")
            wave, site, question, response_id, score = (record[key].strip() for key in FIELDS)
            if wave not in WAVES or score not in ("1", "2", "3", "4", "5"):
                raise ValueError(f"Invalid wave or score on input line {line}.")
            try:
                db.execute("INSERT INTO response VALUES (?, ?, ?, ?, ?)", (wave, site, question, response_id, int(score)))
            except sqlite3.IntegrityError as exc:
                raise ValueError(f"Duplicate response on input line {line}.") from exc
        query = (ROOT / "sql/summary.sql").read_text(encoding="utf-8")
        return db.execute(query, {"minimum": minimum, "prior": WAVES[0], "current": WAVES[1]}).fetchall()


def render(rows, minimum):
    def cell(value):
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", " ").replace("\r", " ")
    lines = [
        "# Follow-up survey results", "",
        f"A favorable response is a score of 4 or 5 on a five-point scale. Rows require at least {minimum} responses. Change is measured in percentage points against the baseline wave. A dash means the baseline group did not meet the reporting threshold or had no responses.", "",
        "| Site | Question | Responses | Favorable | Change |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for site, question, responses, favorable, delta in rows:
        change = "—" if delta is None else f"{delta:+.1f} pp"
        lines.append(f"| {cell(site)} | {cell(question)} | {responses} | {favorable:.1f}% | {change} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--minimum", type=int, default=5)
    args = parser.parse_args()
    print(render(summarize(args.source, args.minimum), args.minimum), end="")
