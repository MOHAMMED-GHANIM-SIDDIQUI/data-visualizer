import pandas as pd


def validate_dataframe(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("The selected CSV has no rows.")
    if len(df.columns) == 0:
        raise ValueError("The selected CSV has no columns.")


def build_column_profile(df: pd.DataFrame) -> pd.DataFrame:
    validate_dataframe(df)
    return pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "missing": df.isna().sum(),
            "missing_pct": (df.isna().mean() * 100).round(2),
            "unique_values": df.nunique(dropna=True),
        }
    )


def dataset_metrics(df: pd.DataFrame) -> dict[str, int]:
    validate_dataframe(df)
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
    }
