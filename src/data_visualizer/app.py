import matplotlib.pyplot as plt
import streamlit as st

from .data_io import get_default_files, load_default_csv, read_uploaded_csv
from .plots import build_plot
from .profiling import build_column_profile, dataset_metrics, validate_dataframe


@st.cache_data(show_spinner=False)
def cached_default_csv(file_name: str):
    return load_default_csv(file_name)


def render_overview(df) -> None:
    st.subheader("Dataset overview")
    metrics = dataset_metrics(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{metrics['rows']:,}")
    c2.metric("Columns", f"{metrics['columns']:,}")
    c3.metric("Missing cells", f"{metrics['missing_cells']:,}")

    with st.expander("Preview", expanded=True):
        st.dataframe(df.head(50), use_container_width=True)
    with st.expander("Column profile"):
        st.dataframe(build_column_profile(df), use_container_width=True)
    with st.expander("Descriptive statistics"):
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)


def render_plot(df) -> None:
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
        fig = None
        try:
            fig = build_plot(df, plot_type, x_axis, None if y_axis == "None" else y_axis)
            st.pyplot(fig)
        except Exception as exc:
            st.error(f"Could not render chart: {exc}")
        finally:
            if fig is not None:
                plt.close(fig)


def main() -> None:
    st.set_page_config(page_title="Data Visualizer", layout="wide", page_icon="chart_with_upwards_trend")
    st.title("Data Visualizer")
    st.caption("Explore built-in sample datasets or upload a CSV for quick profiling and charts.")

    default_files = get_default_files()
    data_option = st.radio("Choose data source", ("Use default data", "Upload a CSV file"), horizontal=True)

    try:
        df = None
        if data_option == "Upload a CSV file":
            uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
            if uploaded_file is not None:
                df = read_uploaded_csv(uploaded_file)
        elif default_files:
            selected_file = st.selectbox("Select a sample dataset", default_files)
            df = cached_default_csv(selected_file)
        else:
            st.warning("No sample CSV files were found in the data directory.")

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
