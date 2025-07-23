import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("goodreads_works 1.csv")

# Preprocess
df['genres'] = df['genres'].fillna('')
df['original_publication_year'] = pd.to_numeric(df['original_publication_year'], errors='coerce')
df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce')

# Sidebar filters
st.sidebar.header("📚 Filter Your Reading List")
all_genres = sorted(set(g.strip() for sublist in df['genres'].dropna().str.split(',') for g in sublist))
selected_genre = st.sidebar.selectbox("Select Genre", all_genres)
min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.5, 0.1)
year_range = st.sidebar.slider("Publication Year Range", int(df['original_publication_year'].min()), int(df['original_publication_year'].max()), (2000, 2020))

# Filtered data
filtered_df = df[
    df['genres'].str.contains(selected_genre, case=False) &
    (df['avg_rating'] >= min_rating) &
    (df['original_publication_year'] >= year_range[0]) &
    (df['original_publication_year'] <= year_range[1])
]

# App title
st.title("📖 Books, Reviews & Insights")
st.markdown("Explore Goodreads data and build your perfect summer reading list!")

# Book selection
st.subheader("🎯 Recommended Books")
selected_books = st.multiselect("Select books to add to your reading list", filtered_df['original_title'].dropna().unique())
reading_list = filtered_df[filtered_df['original_title'].isin(selected_books)]

st.write(reading_list[['original_title', 'author', 'avg_rating', 'original_publication_year', 'genres']])

# Export reading list
if not reading_list.empty:
    st.download_button("📥 Export Reading List as CSV", reading_list.to_csv(index=False), "reading_list.csv", "text/csv")

# Charts
st.subheader("📊 Top Genres")
genre_counts = pd.Series([g.strip() for sublist in df['genres'].dropna().str.split(',') for g in sublist]).value_counts().head(15)
fig1, ax1 = plt.subplots()
genre_counts.plot(kind='barh', ax=ax1)
ax1.set_xlabel("Number of Books")
ax1.set_ylabel("Genre")
ax1.set_title("Top 15 Genres by Book Count")
st.pyplot(fig1)

st.subheader("💬 Most Reviewed Books")
most_reviewed = df[['original_title', 'text_reviews_count']].dropna().sort_values(by='text_reviews_count', ascending=False).head(10)
fig2, ax2 = plt.subplots()
ax2.barh(most_reviewed['original_title'], most_reviewed['text_reviews_count'])
ax2.set_xlabel("Text Reviews Count")
ax2.set_title("Top 10 Most Reviewed Books")
st.pyplot(fig2)
