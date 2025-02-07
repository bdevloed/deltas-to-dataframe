import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns


def generate_heatmaps(df):
    # Convert the timestamp column to datetime and extract the date
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # ---------------------------
    # 1. Heatmap: Number of Inserts and Deletes Grouped by Property (predicate) per Day
    # ---------------------------
    # Group the data by date, predicate, and operation, and count occurrences.
    ops_by_property = (
        df.groupby(["date", "predicate", "operation"]).size().reset_index(name="count")
    )

    # Define a mapping from operation to output file name for property-level plots.
    output_files_property = {
        "INSERT": "inserts_per_property.png",
        "DELETE": "deletes_per_property.png",
    }

    # Generate and save a heatmap for each operation (INSERT, DELETE)
    for op in ops_by_property["operation"].unique():
        df_op = ops_by_property[ops_by_property["operation"] == op]
        # Pivot the data: rows = predicate, columns = date, values = count
        pivot_table = df_op.pivot(
            index="predicate", columns="date", values="count"
        ).fillna(0)

        # Determine the maximum value to set the logarithmic normalization
        max_val = pivot_table.max().max()

        plt.figure(figsize=(16, 10))  # Increase the figure size
        sns.heatmap(
            pivot_table,
            annot=True,
            fmt="g",
            norm=LogNorm(vmin=1, vmax=max_val),
            cmap="YlGnBu",
            cbar_kws={"label": "Count"},
        )
        plt.title(f"Heatmap: Number of {op} Operations per Day by Property")
        plt.xlabel("Date")
        plt.ylabel("Property (predicate)")
        plt.xticks(
            rotation=45, ha="right"
        )  # Rotate x-axis labels for better readability
        plt.yticks(rotation=0)  # Ensure y-axis labels are horizontal
        plt.tight_layout()

        # Save the figure using the appropriate filename
        output_filename = output_files_property.get(
            op.upper(), f"{op.lower()}_per_property.png"
        )
        plt.savefig(output_filename)
        print(f"Saved property-level heatmap for {op} as {output_filename}")
        plt.close()

    # ---------------------------
    # 2. Heatmap: For Predicate http://www.w3.org/1999/02/22-rdf-syntax-ns#type,
    #    Number of Inserts and Deletes per Object Value per Day
    # ---------------------------
    # Define the specific predicate
    type_predicate = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    subset = df[df["predicate"] == type_predicate]

    # Group by date, object, and operation
    subset_grouped = (
        subset.groupby(["date", "object", "operation"]).size().reset_index(name="count")
    )

    # Define a mapping from operation to output file name for type-level plots.
    output_files_type = {
        "INSERT": "inserts_type_triples_class.png",
        "DELETE": "deletes_type_triples_class.png",
    }

    # Generate and save a heatmap for each operation
    for op in subset_grouped["operation"].unique():
        df_op = subset_grouped[subset_grouped["operation"] == op]
        # Pivot the data: rows = object, columns = date, values = count
        pivot_table = df_op.pivot(
            index="object", columns="date", values="count"
        ).fillna(0)

        max_val = pivot_table.max().max()

        plt.figure(figsize=(16, 10))  # Increase the figure size
        sns.heatmap(
            pivot_table,
            annot=True,
            fmt="g",
            norm=LogNorm(vmin=1, vmax=max_val),
            cmap="YlGnBu",
            cbar_kws={"label": "Count"},
        )
        plt.title(
            f"Heatmap: Number of {op} Operations per Day for predicate '{type_predicate}' by Object."
        )
        plt.xlabel("Date")
        plt.ylabel("Object")
        plt.xticks(
            rotation=45, ha="right"
        )  # Rotate x-axis labels for better readability
        plt.yticks(rotation=0)  # Ensure y-axis labels are horizontal
        plt.tight_layout()

        # Save the figure using the appropriate filename
        output_filename = output_files_type.get(
            op.upper(), f"{op.lower()}_type_triples_class.png"
        )
        plt.savefig(output_filename)
        print(f"Saved type-level heatmap for {op} as {output_filename}")
        plt.close()
