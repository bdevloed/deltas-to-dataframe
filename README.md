# Deltas to DataFrame

This project provides functionality to process [delta files](https://github.com/lblod/delta-tutorial) and convert them into a pandas DataFrame. It includes features for extracting timestamps from filenames, collecting subject statistics based on specified filters, and generating heatmaps from the processed data.

## Overview

The main logic for processing deltas is implemented in `src/filtered_deltas_to_dataframe.py`. This script allows users to extract relevant information from delta files, including insert and delete operations. The `src/generate_heatmaps.py` script provides functionality to generate heatmaps from the processed DataFrame.

## Installation

To set up the project, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/deltas-to-dataframe.git
   cd deltas-to-dataframe
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the functionality provided by this project, you can run the main.py script with the appropriate arguments. Make sure to provide the path to the delta files and any filters you wish to apply.

#### Processing Delta Files

Example command to process delta files and create a DataFrame:

```
python src/main.py <directory> -f "key=value"
```

Generating Heatmaps
Example command to generate heatmaps from the processed DataFrame:

```
python src/main.py <directory> --heatmap
```

Example command to generate heatmaps from a specified CSV file:

```
python src/main.py <directory> --heatmap --csv=filename.csv
```

Docker
To run the application using Docker, you can use the following command:

```
docker run --rm -v "$(pwd):/shared" -w /shared bdevloed/deltas-to-dataframe --heatmap .
```

Make sure to replace <directory> with the actual path to your delta files and filename.csv with the path to your CSV file if applicable.

When running via docker, this has te be a relative path to the directory containing the delta files because of how the volume is mounted in the container.

License
This project is licensed under the MIT License. See the LICENSE file for details.

## Usage

To use the functionality provided by this project, you can run the `main.py` script with the appropriate arguments. Make sure to provide the path to the directory containing delta files and any filters you wish to apply.

Example command:

```
python src/main.py path/to/delta_directory --filters" '{"key": "value"}'"
```

## Docker

To build and run the Docker image, use the following commands:

1. Build the Docker image:

```
docker build -t bdevloed/deltas-to-dataframe .
```

2. Run the Docker container:

```
docker run bdevloed/deltas-to-dataframe
```

Mount the current directory to the container to access the delta files in the directory with the relative path `delta_directory`, e.g.:

```
docker run --rm -v "$(pwd):/shared" -w /shared bdevloed/deltas-to-dataframe delta_directory -f 's=http://example.org/subject/s1'
```

## Output

a csv, e.g.:
|timestamp |operation|subject |predicate |object |file_name |
|------------------------|---------|-----------------------------|-----------------------------------------|------------------------------------|------------------------------------------------------------------------|
|2025-01-28T16:57:44.657Z|INSERT |http://example.org/subject/s1|http://example.org/predicate/p1 |http://example.org/object/o1 |fe837410-dd98-11ef-86a2-979dcc8ba73e-delta-2025-01-28T16:57:44.657Z.json|
|2025-01-28T16:57:44.657Z|INSERT |http://example.org/subject/s1|http://mu.semte.ch/vocabularies/core/uuid|e94be4c0-aaaa-11ef-a972-0d005ce03818|fe837410-dd98-11ef-86a2-979dcc8ba73e-delta-2025-01-28T16:57:44.657Z.json|
|2025-01-29T10:00:00.000Z|DELETE |http://example.org/subject/s1|http://example.org/predicate/p1 |http://example.org/object/o1 |bbbbbbb-dd98-11ef-86a2-979dcc8ba73e-delta-2025-01-29T10:00:00.000Z.json |
|2025-01-29T10:00:00.000Z|INSERT |http://example.org/subject/s1|http://example.org/predicate/p1 |http://anotherexample.org/object/o5 |bbbbbbb-dd98-11ef-86a2-979dcc8ba73e-delta-2025-01-29T10:00:00.000Z.json |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
