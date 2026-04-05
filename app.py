import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Load and Clean Data
# -----------------------------
df = pd.read_csv("netflix_titles.csv")

# Handle missing values
for col in df.columns:
    if df[col].dtype == 'object':
        df[col].fillna('Unknown', inplace=True)
    else:
        df[col].fillna(0, inplace=True)

# Convert release_year to numeric
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

# Convert date_added to datetime
if 'date_added' in df.columns:
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# -----------------------------
# 2. Analyze Data
# -----------------------------
print("Dataset shape:", df.shape)
print("\nColumn data types:\n", df.dtypes)

print("\nMovies vs TV Shows:\n", df['type'].value_counts())
print("\nTop 10 countries:\n", df['country'].value_counts().head(10))
print("\nRatings distribution:\n", df['rating'].value_counts())
print("\nTitles released per year:\n", df['release_year'].value_counts().sort_index())

# -----------------------------
# 3. Visualizations
# -----------------------------

# 1. Movies and TV Shows vs Year
plt.figure(figsize=(12,6))
sns.countplot(data=df, x='release_year', hue='type', palette='Set2')
plt.title("Movies vs TV Shows by Release Year")
plt.xticks(rotation=90)
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.legend(title="Type")
plt.tight_layout()
plt.show()

# 2. Top countries with content count
top_countries = df['country'].value_counts().head(10)
plt.figure(figsize=(8,6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='Blues_r')
plt.title("Top 10 Countries by Content Count")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# 3. Ratings distribution
plt.figure(figsize=(8,6))
sns.countplot(data=df, y='rating', order=df['rating'].value_counts().index, palette='coolwarm')
plt.title("Distribution of Ratings")
plt.xlabel("Count")
plt.ylabel("Rating")
plt.tight_layout()
plt.show()

# 4. Release year with type and rating
plt.figure(figsize=(12,6))
sns.countplot(data=df, x='release_year', hue='rating', palette='tab10')
plt.title("Release Year vs Rating")
plt.xticks(rotation=90)
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.legend(title="Rating", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12,6))
release_type = df.groupby(['release_year', 'type']).size().unstack(fill_value=0)
release_type.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title("Release Year vs Content Type")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.legend(title="Type")
plt.tight_layout()
plt.show()
