from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
MAX_UPLOAD_SIZE_MB = 25


st.set_page_config(
    page_title="Data Visualizer",
    layout="wide",
    page_icon="chart_with_upwards_trend",
)


@st.cache_data(show_spinner=False)
def load_default_csv(file_name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / file_name)


def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_UPLOAD_SIZE_MB:
        raise ValueError(f"Uploaded file is {size_mb:.1f} MB. Limit is {MAX_UPLOAD_SIZE_MB} MB.")
    return pd.read_csv(uploaded_file)


def get_default_files() -> list[str]:
    if not DATA_DIR.exists():
        return []
    return sorted(path.name for path in DATA_DIR.glob("*.csv"))


def validate_dataframe(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("The selected CSV has no rows.")
    if df.columns.empty:
        raise ValueError("The selected CSV has no columns.")


def render_overview(df: pd.DataFrame) -> None:
    st.subheader("Dataset overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{len(df.columns):,}")
    c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

    with st.expander("Preview", expanded=True):
        st.dataframe(df.head(50), use_container_width=True)

    with st.expander("Column profile"):
        profile = pd.DataFrame(
            {
                "dtype": df.dtypes.astype(str),
                "missing": df.isna().sum(),
                "missing_pct": (df.isna().mean() * 100).round(2),
                "unique_values": df.nunique(dropna=True),
            }
        )
        st.dataframe(profile, use_container_width=True)

    with st.expander("Descriptive statistics"):
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)


def render_plot(df: pd.DataFrame) -> None:
    st.subheader("Visualization")
    columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    plot_type = st.selectbox(
        "Chart type",
        ["Scatter Plot", "Line Plot", "Bar Chart", "Distribution Plot", "Count Plot", "Box Plot"],
    )

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X-axis", columns)
    with col2:
        y_options = numeric_columns if plot_type not in {"Count Plot", "Distribution Plot"} else ["None"]
        y_axis = st.selectbox("Y-axis", y_options)

    if st.button("Generate plot", type="primary"):
        fig, ax = plt.subplots(figsize=(9, 5))
        try:
            if plot_type == "Scatter Plot":
                sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
            elif plot_type == "Line Plot":
                sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
            elif plot_type == "Bar Chart":
                sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
            elif plot_type == "Distribution Plot":
                if x_axis not in numeric_columns:
                    raise ValueError("Distribution plots require a numeric X-axis.")
                sns.histplot(data=df, x=x_axis, kde=True, ax=ax)
            elif plot_type == "Count Plot":
                sns.countplot(data=df, x=x_axis, ax=ax)
            elif plot_type == "Box Plot":
                sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)

            ax.set_title(f"{plot_type}: {x_axis}" + (f" vs {y_axis}" if y_axis != "None" else ""))
            ax.tick_params(axis="x", labelrotation=30)
            fig.tight_layout()
            st.pyplot(fig)
        except Exception as exc:
            st.error(f"Could not render chart: {exc}")
        finally:
            plt.close(fig)


def main() -> None:
    st.title("Data Visualizer")
    st.caption("Explore built-in sample datasets or upload a CSV for quick profiling and charts.")

    default_files = get_default_files()
    data_option = st.radio("Choose data source", ("Use default data", "Upload a CSV file"), horizontal=True)

    df = None
    try:
        if data_option == "Upload a CSV file":
            uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
            if uploaded_file is not None:
                df = read_uploaded_csv(uploaded_file)
        else:
            if not default_files:
                st.warning("No sample CSV files were found in the data directory.")
            else:
                selected_file = st.selectbox("Select a sample dataset", default_files)
                df = load_default_csv(selected_file)

        if df is None:
            st.info("Choose a dataset to begin.")
            return

        validate_dataframe(df)
        render_overview(df)
        render_plot(df)
    except Exception as exc:
        st.error(str(exc))

    st.markdown("---")
    st.caption("Created by Mohammed Ghanim Siddiqui")


if __name__ == "__main__":
    main()
