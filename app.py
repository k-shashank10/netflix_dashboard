import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("/netflix_titles.csv")
    return df

df = load_data()

# Dashboard Title
st.title("📺 Netflix Titles Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_type = st.sidebar.multiselect("Select Type", df['type'].unique())
selected_country = st.sidebar.multiselect("Select Country", df['country'].dropna().unique())

# Apply filters
filtered_df = df.copy()
if selected_type:
    filtered_df = filtered_df[filtered_df['type'].isin(selected_type)]
if selected_country:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

# Show dataset preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))

# Count of titles by type
st.subheader("Count of Titles by Type")
type_count = filtered_df['type'].value_counts()
st.bar_chart(type_count)

# Titles added per year
st.subheader("Titles Added per Year")
filtered_df['year_added'] = pd.to_datetime(filtered_df['date_added'], errors='coerce').dt.year
year_count = filtered_df['year_added'].value_counts().sort_index()
st.line_chart(year_count)

# Top 10 countries with most titles
st.subheader("Top 10 Countries with Most Titles")
country_count = filtered_df['country'].value_counts().head(10)
st.bar_chart(country_count)

# Genre distribution
st.subheader("Genre Distribution")
all_genres = filtered_df['listed_in'].dropna().str.split(',').explode().str.strip()
genre_count = all_genres.value_counts().head(15)
fig, ax = plt.subplots()
sns.barplot(x=genre_count.values, y=genre_count.index, ax=ax)
st.pyplot(fig)
