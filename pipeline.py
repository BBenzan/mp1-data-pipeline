"""
Data Processing Pipeline - CLI

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="DS 3500 MP1 data pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", "-c", required=True, help="Path to YAML config file")
    parser.add_argument("--output", "-o", required=True, help="Path to output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def print_report(report):
    """Print the cleaning report in a readable format."""
    lines = ",\n".join(f"    {key!r}: {value!r}" for key, value in report.items())
    print(f"\nCleaning report:\n{{\n{lines}\n}}")


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        f"Arguments parsed: input={args.input}, config={args.config}, output={args.output}"
    )

    # Validate files from src folder
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # Load data and configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        logger.ERROR("Failed to load data or configuration.")
        sys.exit(1)

    # Validate DataFrame
    validation = (config or {}).get("validation", {}) or {}
    required_columns = validation.get("required_columns", []) or []
    numeric_columns = validation.get("numeric_columns", []) or []

    rows_before_validation = len(data)
    try:
        df = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {rows_before_validation} -> {len(df)} rows")

    # Process data
    df_original = df.copy()
    try:
        df_clean = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df_clean)
    logger.info(
        f"Processing complete: {report['rows_before']} -> {report['rows_after']} rows"
    )

    # Save output
    output_path = save_data(df_clean, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    print_report(report)


if __name__ == "__main__":
    main()
