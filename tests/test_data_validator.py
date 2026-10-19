# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    columns = ["record_id", "name", "rating", "category", "status"]
    # TODO: Set the required and numeric column names
    numeric_columns = ["rating"]
    validated_df = validate_dataframe(sample_df, required_columns=columns, numeric_columns=numeric_columns)
    assert len(validated_df) == 98
   


def test_validate_dataframe_with_missing_column(sample_df):
    columns = ["user_id", "movie_id", "rating", "timestamp", "nonexistent_column"]
    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns=columns, numeric_columns=["rating"])
