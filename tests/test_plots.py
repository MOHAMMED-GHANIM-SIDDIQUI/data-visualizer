import pandas as pd
import pytest

from data_visualizer.plots import validate_plot_selection


def test_distribution_plot_requires_numeric_x_axis():
    df = pd.DataFrame({"category": ["a", "b"], "value": [1, 2]})

    with pytest.raises(ValueError, match="numeric"):
        validate_plot_selection(df, "Distribution Plot", "category")


def test_scatter_plot_requires_numeric_y_axis():
    df = pd.DataFrame({"x": [1, 2], "label": ["a", "b"]})

    with pytest.raises(ValueError, match="numeric"):
        validate_plot_selection(df, "Scatter Plot", "x", "label")
