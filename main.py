import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊 Data Visualizer')

working_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the folder where your CSV files are located
folder_path = f"{working_dir}/data"  # Update this to your folder path

# List all files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Option for user to select between default or custom CSV file
data_option = st.radio("Choose data source", ("Upload a CSV file", "Use default data"))

# Initialize df to avoid referencing an undefined variable
df = None

if data_option == "Upload a CSV file":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("**Data Preview**:")
        st.write(df.head())
else:
    # Let user select a file from default folder
    selected_file = st.selectbox('Select a default file', files, index=None)

    if selected_file:
        # Construct the full path to the file
        file_path = os.path.join(folder_path, selected_file)

        # Read the selected CSV file
        df = pd.read_csv(file_path)

        st.write("**Data Preview**:")
        st.write(df.head())  # Display the first few rows of the dataframe

# Ensure df is not None before proceeding
if df is not None:
    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("**Data Overview:**")
        st.write(df.describe())

    with col2:
        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

    # Generate the plot based on user selection
    if st.button('Generate Plot'):

        # Avoid using "None" as a valid axis for plotting
        if x_axis != "None" and y_axis != "None":
            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'  # Set y-axis label only for Distribution Plot
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'  # Set y-axis label for count plot

            # Adjust label sizes
            ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
            ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

            # Adjust title and axis labels with a smaller font size
            plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
            plt.xlabel(x_axis, fontsize=10)
            plt.ylabel(y_axis, fontsize=10)

            # Show the results
            st.pyplot(fig)
        else:
            st.error("Please select valid columns for both X and Y axes.")

else:
    st.error("Please upload a CSV file or select a default file to visualize the data.")

st.markdown("**Created by MOHAMMED GHANIM SIDIQUI**")
