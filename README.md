# MP1 Data Pipeline

This pipeline is a command-line tool that loads a CSV dataset, validates it, cleans it based on a YAML configuration file, and saves the cleaned result as a new CSV. Data moves through five stages: the input and config paths are checked, both files are loaded, the DataFrame is validated, the data is cleaned, and the output is written to disk. `pipeline.py` sits at the repository root and coordinates the workflow, while the reusable logic lives in the `src/` package. `src/utils.py` configures logging and checks that input files exist, and `src/data_loaders.py` loads CSV, JSON, or YAML files based on their extension. `src/data_validator.py` confirms required columns exist and removes rows with non-numeric values in numeric columns. `src/data_processor.py` removes duplicates, missing values, and outliers according to the settings in `config/config.yaml`, then builds a cleaning report. `src/data_output.py` creates the output directory if needed and saves the cleaned DataFrame without the index. Because column names and cleaning options live in the config file, the same code can clean a different dataset by changing only the config.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
13:50:32 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
13:50:32 INFO     src.utils — Input file validated: fixtures/sample_data.csv
13:50:32 INFO     src.utils — Input file validated: config/config.yaml
13:50:32 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
13:50:32 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
13:50:32 WARNING  src.data_validator — Invalid numeric value in rating at row 14: 'excellent'
13:50:32 WARNING  src.data_validator — Invalid numeric value in rating at row 89: 'bad'
13:50:32 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
13:50:32 DEBUG    src.data_validator — Validation: 100 -> 98 rows (valid=98, removed=2)
13:50:32 INFO     __main__ — Validation complete: 100 -> 98 rows
13:50:32 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows (removed 2)
13:50:32 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows (removed 2)
13:50:32 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
13:50:32 INFO     __main__ — Processing complete: 98 -> 92 rows
13:50:32 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
13:50:32 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{
    'rows_before': 98,
    'rows_after': 92,
    'rows_removed': 6,
    'columns_before': 5,
    'columns_after': 5,
    'columns_removed': 0
}
```
