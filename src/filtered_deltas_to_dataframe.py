import json
import os
import sys
import re
import pandas as pd
import argparse

# Regular expression to extract the datetime from filenames
DATETIME_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)")


def extract_datetime(filename):
    """Extract datetime from filename using regex"""
    match = DATETIME_PATTERN.search(filename)
    return match.group(1) if match else None


def collect_subject_stats(file_path, filters):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    subject_stats = []

    filename = os.path.basename(file_path)
    timestamp = extract_datetime(filename)

    for entry in data:
        # Process deletes
        if "deletes" in entry and isinstance(entry["deletes"], list):
            for d in entry["deletes"]:
                if not all(
                    d.get(key, {}).get("value") == value
                    for key, value in filters.items()
                ):
                    continue
                subject_stats.append(
                    {
                        "operation": "DELETE",
                        "timestamp": timestamp,
                        "subject": d["subject"]["value"],
                        "predicate": d["predicate"]["value"],
                        "object": d["object"]["value"],
                        "file_name": filename,
                    }
                )
        else:
            print(f"Warning: No deletes found in {filename}")

        # Process inserts
        if "inserts" in entry and isinstance(entry["inserts"], list):
            for i in entry["inserts"]:
                if not all(
                    i.get(key, {}).get("value") == value
                    for key, value in filters.items()
                ):
                    continue
                subject_stats.append(
                    {
                        "timestamp": timestamp,
                        "operation": "INSERT",
                        "subject": i["subject"]["value"],
                        "predicate": i["predicate"]["value"],
                        "object": i["object"]["value"],
                        "file_name": filename,
                    }
                )