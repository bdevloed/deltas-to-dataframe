import json
import os
import sys
import re
import pandas as pd
import argparse

# Regular expression to match any ISO8601 datetime pattern
DATETIME_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)"
)

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
        else:
            print(f"Warning: No inserts found in {filename}")

    return subject_stats


def process_directory(directory, filters):
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return

    total_subject_stats = []
    json_files_processed = 0

    print("Processing delta files...\n" + "-" * 50)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                subject_stats = collect_subject_stats(file_path, filters)
                total_subject_stats.extend(subject_stats)
                json_files_processed += 1

    if json_files_processed == 0:
        print(f"No delta files found in directory: {directory}")
        return

    df = pd.DataFrame(total_subject_stats)
    # sort by timestamp, subject, predicate, object
    df = df.sort_values(by=["timestamp", "subject", "predicate", "object"])

    print("\nDataFrame\n" + "-" * 50)
    print(f"Total rows: {len(df)}")

    # Save the DataFrame to a CSV file in the specified directory
    output_file = os.path.join(directory, "delta_dataframe.csv")
    df.to_csv(output_file, index=False)
    print(f"DataFrame saved to {output_file}")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process delta files and create a DataFrame."
    )
    parser.add_argument("directory", help="Directory containing delta files")
    parser.add_argument(
        "-f",
        "--filter",
        action="append",
        help=(
            "Filter in the format 'key=value' where key can be subject, "
            "predicate, object or their shorthand 's', 'p', 'o'."
        ),
    )

    args = parser.parse_args()

    filters = {}
    key_mapping = {"s": "subject", "p": "predicate", "o": "object"}
    if args.filter:
        for f in args.filter:
            try:
                key, value = f.split("=")
                key = key_mapping.get(
                    key, key
                )  # Map 's', 'p', 'o' to 'subject', 'predicate', 'object'
                if key not in ["subject", "predicate", "object"]:
                    raise ValueError("Invalid filter key")
                filters[key] = value
            except ValueError:
                print(
                    "Invalid filter format. Use 'key=value' "
                    "where key can be subject, predicate, or object."
                )
                sys.exit(1)

    process_directory(args.directory, filters)
