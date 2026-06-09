import pandas as pd
import pytest

from data_visualizer.data_io import validate_uploaded_size
from data_visualizer.profiling import build_column_profile, dataset_metrics, validate_dataframe


def test_dataset_metrics_counts_rows_columns_and_missing_values():
    df = pd.DataFrame({"a": [1, None], "b": ["x", "y"]})

    assert dataset_metrics(df) == {"rows": 2, "columns": 2, "missing_cells": 1}


def test_column_profile_reports_missing_percentages():
    df = pd.DataFrame({"a": [1, None], "b": ["x", "y"]})

    profile = build_column_profile(df)

    assert profile.loc["a", "missing"] == 1
    assert profile.loc["a", "missing_pct"] == 50.0


def test_validate_dataframe_rejects_empty_dataframes():
    with pytest.raises(ValueError, match="no rows"):
        validate_dataframe(pd.DataFrame(columns=["a"]))


def test_validate_uploaded_size_rejects_large_files():
    with pytest.raises(ValueError, match="Limit"):
        validate_uploaded_size(26 * 1024 * 1024, max_mb=25)
