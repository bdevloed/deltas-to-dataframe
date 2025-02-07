import pandas as pd
from argument_handler import ArgumentHandler
from filtered_deltas_to_dataframe import process_directory
from generate_heatmaps import generate_heatmaps

if __name__ == "__main__":
    arg_handler = ArgumentHandler()
    args = arg_handler.parse_arguments()

    if args.heatmap:
        if args.csv:
            df = pd.read_csv(args.csv)
        else:
            filters = arg_handler.handle_filters(args.filter)
            df = process_directory(args.directory, filters)
        generate_heatmaps(df)
    else:
        filters = arg_handler.handle_filters(args.filter)
        process_directory(args.directory, filters)
