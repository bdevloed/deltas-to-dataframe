import argparse
import sys


class ArgumentHandler:
    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="Process delta files and create a DataFrame or generate heatmaps."
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
        parser.add_argument(
            "--heatmap",
            action="store_true",
            help="Generate heatmaps from the DataFrame.",
        )
        parser.add_argument("--csv", help="Path to the DataFrame CSV file")

        return parser.parse_args()

    def handle_filters(self, filters):
        filter_dict = {}
        key_mapping = {"s": "subject", "p": "predicate", "o": "object"}
        if filters:
            for f in filters:
                try:
                    key, value = f.split("=")
                    key = key_mapping.get(
                        key, key
                    )  # Map 's', 'p', 'o' to 'subject', 'predicate', 'object'
                    if key not in ["subject", "predicate", "object"]:
                        raise ValueError("Invalid filter key")
                    filter_dict[key] = value
                except ValueError:
                    print(
                        "Invalid filter format. Use 'key=value' where key can be subject, predicate, or object."
                    )
                    sys.exit(1)
        return filter_dict
