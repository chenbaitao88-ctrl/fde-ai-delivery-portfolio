"""Original synthetic example. Python 3.10+, standard library, no network."""
import csv
import json
import math
from pathlib import Path


def summarize(rows):
    required = {"case_id", "group", "eligible", "status", "minutes"}
    groups = {}
    seen = set()
    for row in rows:
        if not required.issubset(row):
            raise ValueError("missing required field")
        if row["case_id"] in seen or not row["case_id"]:
            raise ValueError("case_id must be unique and nonempty")
        seen.add(row["case_id"])
        if not row["group"] or row["eligible"] not in ("yes", "no"):
            raise ValueError("invalid group or eligibility")
        if row["status"] not in ("complete", "pending"):
            raise ValueError("invalid status")
        minutes = float(row["minutes"])
        if not math.isfinite(minutes) or minutes < 0:
            raise ValueError("minutes must be finite and nonnegative")
        if row["eligible"] == "no":
            continue
        item = groups.setdefault(row["group"], {"eligible": 0, "complete": 0})
        item["eligible"] += 1
        item["complete"] += row["status"] == "complete"
    total = sum(g["eligible"] for g in groups.values())
    if total == 0:
        raise ValueError("no eligible records; denominator is zero")
    complete = sum(g["complete"] for g in groups.values())
    for group in groups.values():
        group["rate_percent"] = round(group["complete"] / group["eligible"] * 100, 1)
    return {"input_count": len(rows), "excluded_count": len(rows)-total,
            "eligible": total, "complete": complete,
            "rate_percent": round(complete / total * 100, 1), "groups": groups}


def run():
    with Path(__file__).with_name("input.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    result = {"kind": "executed synthetic calculation", "summary": summarize(rows)}
    broken = dict(rows[0]); del broken["status"]
    try:
        summarize([broken])
    except ValueError as exc:
        result["missing_field_demo"] = {"status": "BLOCKED", "reason": str(exc)}
    else:
        raise AssertionError("missing-field example was accepted")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
