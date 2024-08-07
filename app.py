import base64
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from ydata_profiling import ProfileReport

st.set_page_config(layout="wide", page_title="The DATA EXPLORER App", page_icon=":rocket:")

# Web App Title
st.markdown('''
# **The DATA EXPLORER App**

"Unlock the Power of Data: Your All-in-One EDA and Data Preprocessing Companion!"

"DataExplore: Discover Insights, Cleanse Data, Excel in Analysis!"
 
---
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Helper function to remove duplicate values
def remove_duplicates(dataframe):
    return dataframe.drop_duplicates()

# Helper function to identify primary key candidates
def identify_primary_key(dataframe):
    primary_key_candidates = []
    for col in dataframe.columns:
        if dataframe[col].nunique() == len(dataframe):
            primary_key_candidates.append(col)
    return primary_key_candidates

# Helper function to replace missing values based on strategy
def replace_missing_values(dataframe, strategy):
    if strategy == "Replace with 0":
        return dataframe.fillna(0)
    elif strategy == "Replace with mean":
        numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
        dataframe[numeric_columns] = dataframe[numeric_columns].fillna(dataframe[numeric_columns].mean())
        return dataframe
    elif strategy == "Replace with median":
        numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
        dataframe[numeric_columns] = dataframe[numeric_columns].fillna(dataframe[numeric_columns].median())
        return dataframe
    else:
        return dataframe

# Helper function to convert categorical data to numerical
def convert_categorical_to_numerical(df):
    label_encoder = LabelEncoder()
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str)
        df[col] = label_encoder.fit_transform(df[col])
    return df

# Main Streamlit app
def main():
    global uploaded_file

    if uploaded_file is not None:
        
        def load_csv():
            csv = pd.read_csv(uploaded_file)
            return csv

        df = load_csv()
        info_str = str(df.info())
        
        st.header("Data Visualization Options")
        plot_types = st.multiselect("Select Plot Types:", ['Scatter', 'Line', 'Bar', 'Count', 'Histogram', 'Box', 'Heatmap', 'Pair'])
        
        # Plotting selected plots
        if 'Scatter' in plot_types:
            st.subheader("Scatter Plot")
            selected_x_column = st.selectbox("Select the X-axis column:", df.columns, key='scatter_x')
            selected_y_column = st.selectbox("Select the Y-axis column:", df.columns, key='scatter_y')

            height = st.slider("Select the height of the scatter plot:", min_value=1, max_value=20, value=10, key='scatter_height')
            fig, ax = plt.subplots(figsize=(10, height))
            sns.scatterplot(x=selected_x_column, y=selected_y_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Line' in plot_types:
            st.subheader("Line Plot")
            selected_x_column = st.selectbox("Select the X-axis column:", df.columns, key='line_x')
            selected_y_column = st.selectbox("Select the Y-axis column:", df.columns, key='line_y')

            height = st.slider("Select the height of the line plot:", min_value=1, max_value=20, value=10, key='line_height')
            fig, ax = plt.subplots(figsize=(10, height))
            sns.lineplot(x=selected_x_column, y=selected_y_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Bar' in plot_types:
            st.subheader("Bar Plot")
            selected_x_column = st.selectbox("Select the X-axis column:", df.columns, key='bar_x')
            selected_y_column = st.selectbox("Select the Y-axis column:", df.columns, key='bar_y')

            height = st.slider("Select the height of the bar plot:", min_value=1, max_value=20, value=10, key='bar_height')
            fig, ax = plt.subplots(figsize=(10, height))
            sns.barplot(x=selected_x_column, y=selected_y_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Count' in plot_types:
            st.subheader("Count Plot")
            selected_column = st.selectbox("Select a column:", df.columns, key='count_column')

            height = st.slider("Select the height of the count plot:", min_value=1, max_value=20, value=10, key='count_height')
            fig, ax = plt.subplots(figsize=(10, height))
            sns.countplot(x=selected_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Histogram' in plot_types:
            st.subheader("Histogram")
            selected_column = st.selectbox("Select a column:", df.columns, key='hist_column')

            height = st.slider("Select the height of the histogram plot:", min_value=1, max_value=20, value=10, key='hist_height')
            fig, ax = plt.subplots(figsize=(10, height))
            sns.histplot(df[selected_column], kde=True, ax=ax)
            st.pyplot(fig)

        if 'Box' in plot_types:
            st.subheader("Box Plot")
            target_column = st.selectbox("Select a column:", df.columns, key='box_target')
            selected_column = st.selectbox("Select a column:", df.columns, key='box_column')

            box_height = st.slider("Select the height of the Box Plot:", min_value=1, max_value=20, value=10, key='box_height')
            fig_box, ax_box = plt.subplots(figsize=(10, box_height))
            sns.boxplot(x=selected_column, y=target_column, data=df, ax=ax_box)
            st.pyplot(fig_box)

        if 'Heatmap' in plot_types:
            st.subheader("Heatmap")
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            correlation_matrix = df[numeric_columns].corr()

            height = st.slider("Select the height of the heatmap:", min_value=1, max_value=20, value=10, key='heatmap_height')
            fig, ax = plt.subplots(figsize=(10, height))
            sns.heatmap(correlation_matrix, annot=True, ax=ax)
            st.pyplot(fig)

        if 'Pair' in plot_types:
            st.subheader("Pair Plot")
            sns.pairplot(df, height=4)
            st.pyplot()

        st.header("EDA Report")
        if st.checkbox("Show Report"):
            st.header("Data Transformation Options")
            pr = ProfileReport(df, explorative=True)
            report_html = pr.to_html()

            if st.button("Download Missing Values Report (.doc)"):
                report_docx = io.StringIO()
                report_docx.write(report_html)
                report_docx.seek(0)

                b64 = base64.b64encode(report_docx.read().encode()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="missing_values_report.doc">Download Missing Values Report (.doc)</a>'
                st.markdown(href, unsafe_allow_html=True)

            st.components.v1.html(report_html, height=800, scrolling=True)

        st.header("Data Transformation Options")

        if st.checkbox("Remove Duplicate Values"):
            df = remove_duplicates(df)

        if st.checkbox("Replace Missing Values"):
            missing_value_strategy = st.selectbox(
                "Choose missing value replacement strategy:",
                ["Leave as NaN", "Replace with 0", "Replace with mean", "Replace with median"]
            )
            df = replace_missing_values(df, missing_value_strategy)

        if st.checkbox("Convert Categorical Data to Numerical"):
            df = convert_categorical_to_numerical(df)

        st.header("Processed DataFrame")
        st.dataframe(df)

        if st.button("Download Processed DataFrame as CSV"):
            processed_csv = df.to_csv(index=False)
            b64 = base64.b64encode(processed_csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="processed_dataframe.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info('Awaiting for CSV file to be uploaded.')

if __name__ == "__main__":
    main()
