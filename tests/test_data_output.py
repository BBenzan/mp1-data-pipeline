#tests/test_data_output.py

import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"   
    s = save_data(sample_df, output_path)
    assert output_path.exists()
    df = pd.read_csv(output_path)
    assert len(df) == len(sample_df)
    assert list(df.columns) == list(sample_df.columns)
    