import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Netflix Dashboard", page_icon="🎬", layout="wide")

# Function to load and cache the data
@st.cache_data
def load_data():
    # Ensure the csv file is in the same directory as this script
    df = pd.read_csv('/netflix_titles.csv')
    
    # Minor data cleaning: fill missing values for visual clarity
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unknown')
    return df

df = load_data()

# --- HEADER ---
st.title("🎬 Netflix Data Explorer")
st.markdown("Explore the massive catalog of Movies and TV Shows available on Netflix.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Content")

# Filter by Type (Movie / TV Show)
type_options = df['type'].unique().tolist()
selected_types = st.sidebar.multiselect("Select Content Type", options=type_options, default=type_options)

# Filter by Release Year
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
selected_years = st.sidebar.slider("Select Release Year Range", min_year, max_year, (2000, max_year))

# Apply Filters
filtered_df = df[
    (df['type'].isin(selected_types)) & 
    (df['release_year'] >= selected_years[0]) & 
    (df['release_year'] <= selected_years[1])
]

# --- TOP METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Titles", value=len(filtered_df))
col2.metric(label="Total Movies", value=len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric(label="Total TV Shows", value=len(filtered_df[filtered_df['type'] == 'TV Show']))

st.markdown("---")

# --- VISUALIZATIONS ---
col_left, col_right = st.columns(2)

with col_left:
    # 1. Content Distribution (Pie Chart)
    st.subheader("Movie vs TV Show Distribution")
    fig_type = px.pie(filtered_df, names='type', hole=0.4, color_discrete_sequence=['#E50914', '#221F1F'])
    st.plotly_chart(fig_type, use_container_width=True)

with col_right:
    # 2. Content Released Over Time (Line Chart)
    st.subheader("Content Releases Over Time")
    trend_df = filtered_df['release_year'].value_counts().reset_index()
    trend_df.columns = ['Release Year', 'Count']
    trend_df = trend_df.sort_values('Release Year')
    
    fig_trend = px.line(trend_df, x='Release Year', y='Count', markers=True, color_discrete_sequence=['#E50914'])
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# 3. Top 10 Countries with the Most Content (Bar Chart)
st.subheader("Top 10 Producing Countries")
# Some entries have multiple countries separated by commas. For simplicity, we just count the direct string.
country_df = filtered_df['country'].value_counts().head(10).reset_index()
country_df.columns = ['Country', 'Number of Titles']

fig_country = px.bar(country_df, x='Country', y='Number of Titles', color='Number of Titles', color_continuous_scale='Reds')
st.plotly_chart(fig_country, use_container_width=True)

# --- RAW DATA VIEW ---
st.markdown("---")
st.subheader("Raw Data View")
if st.checkbox("Show raw data table"):
    st.dataframe(filtered_df)
