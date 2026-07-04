from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


TEXT_FIELDS = ("text", "full_text", "tweet", "content", "body")
LIST_FIELDS = ("data", "tweets", "results", "items")


def _iter_json_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in LIST_FIELDS:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    raise ValueError("Xquik export must contain a list of result objects.")


def _extract_text(item: dict[str, Any]) -> str:
    for field in TEXT_FIELDS:
        value = item.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _normalize_row(item: dict[str, Any]) -> dict[str, Any]:
    text = _extract_text(item)
    if not text:
        return {}

    row: dict[str, Any] = {"text": text}
    for source, target in (
        ("user", "user"),
        ("username", "user"),
        ("author_username", "user"),
        ("favorite_count", "favorite_count"),
        ("like_count", "favorite_count"),
        ("retweet_count", "retweet_count"),
        ("created_at", "created_at"),
    ):
        value = item.get(source)
        if value not in (None, "") and target not in row:
            row[target] = value

    return row


def load_xquik_rows(path: str | Path) -> list[dict[str, Any]]:
    export_path = Path(path)
    if not export_path.exists():
        raise FileNotFoundError(f"Xquik export not found: {export_path}")

    if export_path.suffix.lower() == ".jsonl":
        items = [json.loads(line) for line in export_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    elif export_path.suffix.lower() == ".json":
        items = _iter_json_rows(json.loads(export_path.read_text(encoding="utf-8")))
    elif export_path.suffix.lower() == ".csv":
        with export_path.open(encoding="utf-8", newline="") as file:
            items = list(csv.DictReader(file))
    else:
        raise ValueError("Xquik export must be a JSON, JSONL, or CSV file.")

    rows = [row for item in items if isinstance(item, dict) for row in [_normalize_row(item)] if row]
    if not rows:
        raise ValueError("Xquik export does not contain any rows with text.")

    return rows
