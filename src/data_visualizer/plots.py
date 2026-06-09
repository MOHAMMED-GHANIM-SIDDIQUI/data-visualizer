import pandas as pd


NUMERIC_REQUIRED = {"Scatter Plot", "Line Plot", "Bar Chart", "Distribution Plot", "Box Plot"}


def validate_plot_selection(df: pd.DataFrame, plot_type: str, x_axis: str, y_axis: str | None = None) -> None:
    if x_axis not in df.columns:
        raise ValueError("Selected X-axis is not in the dataframe.")
    if plot_type in NUMERIC_REQUIRED and plot_type != "Distribution Plot":
        if not y_axis or y_axis not in df.columns:
            raise ValueError("Selected Y-axis is not in the dataframe.")
        if not pd.api.types.is_numeric_dtype(df[y_axis]):
            raise ValueError("Selected Y-axis must be numeric for this chart.")
    if plot_type == "Distribution Plot" and not pd.api.types.is_numeric_dtype(df[x_axis]):
        raise ValueError("Distribution plots require a numeric X-axis.")


def build_plot(df: pd.DataFrame, plot_type: str, x_axis: str, y_axis: str | None = None):
    import matplotlib.pyplot as plt
    import seaborn as sns

    validate_plot_selection(df, plot_type, x_axis, y_axis)
    fig, ax = plt.subplots(figsize=(9, 5))

    if plot_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif plot_type == "Line Plot":
        sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif plot_type == "Bar Chart":
        sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
    elif plot_type == "Distribution Plot":
        sns.histplot(data=df, x=x_axis, kde=True, ax=ax)
    elif plot_type == "Count Plot":
        sns.countplot(data=df, x=x_axis, ax=ax)
    elif plot_type == "Box Plot":
        sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
    else:
        raise ValueError(f"Unsupported chart type: {plot_type}")

    ax.set_title(f"{plot_type}: {x_axis}" + (f" vs {y_axis}" if y_axis else ""))
    ax.tick_params(axis="x", labelrotation=30)
    fig.tight_layout()
    return fig
