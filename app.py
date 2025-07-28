import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="☀️ Summer Reading List Builder",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for library theme
st.markdown("""
<style>
    /* Main app styling with neutral background */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Sidebar styling with library theme */
    .stSidebar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-header {
        background: rgba(139, 69, 19, 0.9);
        backdrop-filter: blur(10px);
        padding: 0.6rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 0.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-brand {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8f9fa;
        margin-bottom: 0.2rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    .sidebar-subtitle {
        font-size: 0.9rem;
        color: #f8f9fa;
        font-weight: 400;
        opacity: 0.9;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .navigation-section {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        padding: 0.4rem;
        border-radius: 8px;
        margin-bottom: 0.3rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .nav-title {
        color: #2c3e50;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Special spacing for Recently Added section */
    .navigation-section:has(.nav-title:contains("Recently Added")) .nav-title,
    .recently-added-title {
        margin-bottom: 0.6rem !important;
    }
    
    /* Hide any remaining header blocks */
    .main-header {
        display: none !important;
    }
    
    /* Compact metrics styling */
    /* Ultra-compact metrics styling */
    .stMetric {
        background: rgba(248, 249, 250, 0.9);
        padding: 0.25rem 0.4rem;
        border-radius: 4px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        margin-bottom: 0.2rem;
    }
    
    .stMetric [data-testid="metric-container"] {
        padding: 0.1rem 0;
    }
    
    .stMetric [data-testid="metric-container"] > div {
        gap: 0.1rem;
    }
    
    .stMetric [data-testid="metric-container"] > div:first-child {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        line-height: 1.1 !important;
    }
    
    .stMetric [data-testid="metric-container"] > div:last-child {
        font-size: 0.7rem !important;
        opacity: 0.8 !important;
        margin-top: -2px !important;
    }
    
    /* Book card styling */
    .book-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        border-left: 4px solid #6c757d;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .book-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    
    .compact-book-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-left: 4px solid #8B4513;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .compact-book-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    }
    
    .ultra-compact-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        padding: 0.4rem;
        border-radius: 6px;
        margin-bottom: 0.4rem;
        box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-left: 3px solid #8B4513;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    
    .ultra-compact-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    .book-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .book-author {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 0.5rem;
    }
    
    .book-rating {
        color: #f39c12;
        font-weight: bold;
    }
    
    .book-year {
        color: #95a5a6;
        font-size: 0.9rem;
    }
    
    .book-details {
        font-size: 0.8rem;
        color: #6c757d;
        margin-bottom: 0.2rem;
    }
    
    /* Compact controls section */
    .compact-controls {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(5px);
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Reduce spacing in form containers */
    .compact-controls .stSelectbox,
    .compact-controls .stRadio {
        margin-bottom: 0.3rem !important;
    }
    
    .compact-controls .stSelectbox > div,
    .compact-controls .stRadio > div {
        margin-bottom: 0.2rem !important;
        padding-bottom: 0 !important;
    }
    
    /* Compact form labels */
    .compact-controls .stSelectbox label,
    .compact-controls .stRadio label {
        margin-bottom: 0.3rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #2c3e50 !important;
    }
    
    /* Remove extra spacing */
    .compact-controls .element-container {
        margin-bottom: 0.4rem !important;
    }
    
    .compact-controls .row-widget {
        margin-bottom: 0.3rem !important;
    }
    
    /* Tighter radio button spacing in navigation */
    .navigation-section .stRadio > div {
        gap: 0rem !important;
        margin-top: -0.6rem !important;
    }
    
    .navigation-section .stRadio label {
        margin-bottom: 0rem !important;
    }
    
    .navigation-section .stRadio {
        margin-top: -0.3rem !important;
    }
    
    .navigation-section .stRadio > div > div {
        margin-top: -0.2rem !important;
        padding-top: 0rem !important;
    }
    
    /* Tighter column spacing */
    .compact-controls [data-testid="column"] {
        padding: 0 0.3rem !important;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 2rem 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-top: 4px solid #8B4513;
    }
    
    .empty-state h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .empty-state p {
        color: #495057;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Sidebar stats styling */
    .sidebar-stat {
        background: rgba(248, 249, 250, 0.9);
        backdrop-filter: blur(5px);
        padding: 0.6rem;
        border-radius: 6px;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .stat-label {
        color: #495057;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .recent-book {
        color: #2c3e50;
        font-size: 0.75rem;
        margin-bottom: 0.3rem;
        padding: 0.3rem;
        background: rgba(248, 249, 250, 0.8);
        backdrop-filter: blur(5px);
        border-radius: 4px;
        border-left: 2px solid #8B4513;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: #8B4513;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        padding: 0.4rem 0.8rem;
        font-size: 0.85rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: #654321;
        color: white;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Form styling */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 0, 0, 0.2);
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'books_df' not in st.session_state:
    st.session_state.books_df = pd.DataFrame()
if 'my_books' not in st.session_state:
    st.session_state.my_books = []
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = False

# File to store personal books data
MY_BOOKS_FILE = 'my_books.json'

# Genre emoji mapping
genre_icons = {
    "Fantasy": "🧙", "Romance": "❤️", "Science Fiction": "🚀", "Mystery": "🕵️",
    "Nonfiction": "📘", "Historical": "🏛️", "Horror": "👻", "Thriller": "🔪", 
    "Classic": "🎩", "Adventure": "⚔️", "Biography": "👤", "Comedy": "😄",
    "Drama": "🎭", "Fiction": "📖", "Poetry": "📝", "Philosophy": "🤔",
    "Classic Fiction": "📚", "Dystopian Fiction": "🔮", "Coming of Age": "🌱",
    "Gothic Horror": "🏰", "Historical Fiction": "🏛️", "Science": "🔬"
}

def load_sample_data():
    """Load sample book data if no CSV is found"""
    sample_books = {
        'title': [
            'The Great Gatsby', 'To Kill a Mockingbird', '1984', 'Pride and Prejudice',
            'The Catcher in the Rye', 'Lord of the Flies', 'The Lord of the Rings',
            'Harry Potter and the Sorcerer\'s Stone', 'The Hobbit', 'Fahrenheit 451',
            'Jane Eyre', 'Wuthering Heights', 'Great Expectations', 'The Adventures of Huckleberry Finn',
            'The Picture of Dorian Gray', 'Dracula', 'Frankenstein', 'The Time Machine',
            'War and Peace', 'Crime and Punishment'
        ],
        'author': [
            'F. Scott Fitzgerald', 'Harper Lee', 'George Orwell', 'Jane Austen',
            'J.D. Salinger', 'William Golding', 'J.R.R. Tolkien',
            'J.K. Rowling', 'J.R.R. Tolkien', 'Ray Bradbury',
            'Charlotte Bronte', 'Emily Bronte', 'Charles Dickens', 'Mark Twain',
            'Oscar Wilde', 'Bram Stoker', 'Mary Shelley', 'H.G. Wells',
            'Leo Tolstoy', 'Fyodor Dostoevsky'
        ],
        'year': [
            1925, 1960, 1949, 1813, 1951, 1954, 1954, 1997, 1937, 1953,
            1847, 1847, 1861, 1884, 1890, 1897, 1818, 1895, 1869, 1866
        ],
        'average_rating': [
            3.93, 4.28, 4.19, 4.28, 3.80, 3.69, 4.50, 4.47, 4.28, 3.97,
            4.14, 3.86, 3.78, 3.82, 4.11, 4.01, 3.83, 3.89, 4.12, 4.20
        ],
        'genre': [
            'Classic Fiction', 'Classic Fiction', 'Dystopian Fiction', 'Romance',
            'Coming of Age', 'Classic Fiction', 'Fantasy', 'Fantasy', 'Fantasy', 'Dystopian Fiction',
            'Classic Fiction', 'Classic Fiction', 'Classic Fiction', 'Adventure',
            'Classic Fiction', 'Gothic Horror', 'Gothic Horror', 'Science Fiction',
            'Historical Fiction', 'Classic Fiction'
        ]
    }
    return pd.DataFrame(sample_books)

def load_data():
    """Load book data from CSV or create sample data"""
    try:
        possible_files = [
            'books.csv', 'book_data.csv', 'library.csv', 'goodbooks.csv',
            'goodreads_works.csv', 'maven_books_dataset.csv', 'bookshelf.csv', 'maven_bookshelf.csv'
        ]
        
        for filename in possible_files:
            if Path(filename).exists():
                df = pd.read_csv(filename)
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
                
                column_mapping = {
                    'original_title': 'title',
                    'avg_rating': 'average_rating',
                    'original_publication_year': 'year',
                    'genres': 'genre'
                }
                
                for old_name, new_name in column_mapping.items():
                    if old_name in df.columns:
                        df.rename(columns={old_name: new_name}, inplace=True)
                
                df.dropna(subset=['title'], inplace=True)
                if 'author' in df.columns:
                    df.dropna(subset=['author'], inplace=True)
                
                return df
        
        st.info("📝 No CSV file found. Using sample book data.")
        return load_sample_data()
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Using sample data instead.")
        return load_sample_data()

def load_my_books():
    """Load personal books from JSON file"""
    if os.path.exists(MY_BOOKS_FILE):
        try:
            with open(MY_BOOKS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_my_books():
    """Save personal books to JSON file"""
    with open(MY_BOOKS_FILE, 'w') as f:
        json.dump(st.session_state.my_books, f, indent=2)

def parse_genres(genre_data):
    """Parse genre data into a list of individual genres"""
    if pd.isna(genre_data) or genre_data == '' or genre_data is None:
        return ['Unknown']
    
    genre_str = str(genre_data).strip()
    
    if not genre_str or genre_str.lower() in ['unknown', 'n/a', 'none', 'nan']:
        return ['Unknown']
    
    # Handle different separators
    separators = [',', ';', '|', '\n', '/', '&', ' and ', ' & ', ' - ']
    current_genres = [genre_str]
    
    for sep in separators:
        new_genres = []
        for item in current_genres:
            if sep in item:
                parts = item.split(sep)
                for part in parts:
                    cleaned_part = part.strip()
                    if cleaned_part:
                        new_genres.append(cleaned_part)
            else:
                new_genres.append(item)
        current_genres = new_genres
    
    # Clean up genres
    clean_genres = []
    for genre in current_genres:
        clean_genre = genre.strip().strip('"').strip("'").strip('[]').strip('()').strip()
        clean_genre = clean_genre.replace('_', ' ').title()
        
        if (clean_genre and 
            len(clean_genre) > 1 and
            clean_genre.lower() not in ['unknown', 'n/a', 'none', 'nan', 'null', '', ' '] and
            not clean_genre.isdigit()):
            clean_genres.append(clean_genre)
    
    return clean_genres if clean_genres else ['Unknown']

def extract_all_genres_from_dataframe(df):
    """Extract all unique genres from the dataframe"""
    all_genres = set()
    
    if 'genre' not in df.columns:
        return []
    
    for _, row in df.iterrows():
        genre_value = row['genre']
        parsed_genres = parse_genres(genre_value)
        all_genres.update(parsed_genres)
    
    return sorted(list(all_genres))

def display_book_card(book, show_add_button=True, compact=False, show_remove_button=False):
    """Display a book card with optional add button"""
    genre_data = book.get('genre', 'Unknown')
    parsed_genres = parse_genres(genre_data)
    
    if parsed_genres and parsed_genres != ['Unknown']:
        genre_display = " ".join([genre_icons.get(g, "📗") + " " + g for g in parsed_genres[:2]])
    else:
        genre_display = "📗 Unknown"
    
    card_class = "ultra-compact-card"
    
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        
        if show_add_button or show_remove_button:
            col_info, col_action = st.columns([5, 1])
        else:
            col_info = st.container()
            col_action = None
        
        with col_info:
            title = str(book.get('title', 'Unknown Title'))
            author = str(book.get('author', 'Unknown Author'))
            
            display_title = title if len(title) <= 60 else title[:57] + "..."
            st.markdown(f'<div class="book-title" style="font-size: 0.9rem; margin-bottom: 0.1rem;">{display_title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="book-author" style="font-size: 0.75rem; margin-bottom: 0.1rem;">by {author}</div>', unsafe_allow_html=True)
            
            rating = book.get('average_rating', 0)
            year = book.get('year', 'Unknown')
            
            if pd.notna(rating) and rating > 0:
                rating_display = f"⭐ {float(rating):.1f}"
            else:
                rating_display = "⭐ N/A"
            
            if pd.notna(year) and year != 'Unknown':
                try:
                    year_val = int(float(year))
                    year_display = str(year_val)
                except:
                    year_display = "Unknown"
            else:
                year_display = "Unknown"
            
            st.markdown(f'<div class="book-details" style="font-size: 0.7rem; margin-bottom: 0.1rem;">{rating_display} • {year_display} • {genre_display}</div>', unsafe_allow_html=True)
        
        if col_action:
            with col_action:
                if show_add_button:
                    book_id = book.get('work_id', f"{title}_{author}")
                    book_exists = any(book.get('work_id') == book_id or 
                                    (book['title'] == title and book['author'] == author) 
                                    for book in st.session_state.my_books)
                    
                    if not book_exists:
                        if st.button("Add", key=f"add_{book_id}", type="secondary"):
                            new_book = {
                                'id': len(st.session_state.my_books) + 1,
                                'work_id': book_id,
                                'title': title,
                                'author': author,
                                'genre': book.get('genre', 'Unknown'),
                                'rating': int(float(rating)) if pd.notna(rating) and rating > 0 else 3,
                                'average_rating': float(rating) if pd.notna(rating) else None,
                                'year': year,
                                'date_added': datetime.now().strftime("%Y-%m-%d"),
                                'source': 'dataset'
                            }
                            st.session_state.my_books.append(new_book)
                            save_my_books()
                            st.success(f"Added '{title}' to your library!")
                            st.rerun()
                    else:
                        st.markdown("✅")
                
                elif show_remove_button:
                    book_id = book.get('work_id', f"{title}_{author}")
                    if st.button("Remove", key=f"remove_{book_id}", type="secondary"):
                        st.session_state.my_books = [
                            b for b in st.session_state.my_books
                            if not (b.get('work_id', f"{b['title']}_{b['author']}") == book_id)
                        ]
                        save_my_books()
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def discover_books():
    """Discover and browse books from the collection - WITHOUT GENRE FILTER"""
    st.markdown("### Discover Books")
    if st.session_state.books_df.empty:
        st.warning("📚 No book collection available. Please ensure your dataset file is in the project directory.")
        return
    
    df = st.session_state.books_df.copy()
    
    # Initialize filter session state if not exists
    if 'clear_filters_counter' not in st.session_state:
        st.session_state.clear_filters_counter = 0
    
    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")
        
        # Clear filters button
        if st.button("🔄 Clear All Filters", key=f"clear_filters_{st.session_state.clear_filters_counter}"):
            st.session_state.clear_filters_counter += 1
            st.rerun()
        
        # Search filter
        search_key = f"search_term_{st.session_state.clear_filters_counter}"
        search_term = st.text_input("Search books or authors", placeholder="Enter search term...", key=search_key)
        
        # Author filter
        if 'author' in df.columns:
            all_authors = ['All'] + sorted(df['author'].dropna().unique().tolist())
            
            author_key = f"selected_author_{st.session_state.clear_filters_counter}"
            selected_author = st.selectbox("Author", all_authors, key=author_key)
        else:
            selected_author = 'All'
        
        # Rating filter
        if 'average_rating' in df.columns:
            min_rating_default = float(df['average_rating'].min())
            max_rating = float(df['average_rating'].max())
            
            rating_key = f"min_rating_{st.session_state.clear_filters_counter}"
            min_rating = st.slider("Minimum Rating", min_value=min_rating_default, max_value=max_rating, value=min_rating_default, step=0.1, key=rating_key)
        else:
            min_rating = 0
    
    # Apply filters step by step
    filtered = df.copy()
    
    # Search filter
    if search_term and search_term.strip():
        search_mask = (
            filtered['title'].str.contains(search_term, case=False, na=False) |
            (filtered['author'].str.contains(search_term, case=False, na=False) if 'author' in filtered.columns else pd.Series([False] * len(filtered)))
        )
        filtered = filtered[search_mask]
    
    # Author filter
    if selected_author != 'All' and 'author' in filtered.columns:
        filtered = filtered[filtered['author'] == selected_author]
    
    # Rating filter
    if 'average_rating' in filtered.columns:
        rating_mask = filtered['average_rating'] >= min_rating
        filtered = filtered[rating_mask]
    
    # Display results
    st.caption(f"📖 Found {len(filtered):,} books")
    
    # Show active filters
    active_filters = []
    if search_term and search_term.strip():
        active_filters.append(f"Search: '{search_term}'")
    if selected_author != 'All':
        active_filters.append(f"Author: '{selected_author}'")
    if 'average_rating' in df.columns and min_rating > float(df['average_rating'].min()):
        active_filters.append(f"Min Rating: {min_rating:.1f}")
    
    if active_filters:
        st.caption(f"🔍 Active filters: {' | '.join(active_filters)}")
    
    if len(filtered) == 0:
        st.warning("🔍 No books match your current filters. Try adjusting your search criteria.")
        return
    
    # Controls section
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        sort_options = ["Title", "Rating"]
        if 'author' in filtered.columns:
            sort_options.append("Author")
        sort_by = st.selectbox("Sort", sort_options, index=1 if "Rating" in sort_options else 0, key="sort_select", label_visibility="collapsed")
    
    with col2:
        sort_order = st.radio("", ["↓", "↑"], horizontal=True, key="sort_order", label_visibility="collapsed")
    
    with col3:
        books_per_page = st.selectbox("", [25, 50, 100], key="books_per_page", label_visibility="collapsed")
    
    with col4:
        total_pages = len(filtered) // books_per_page + (1 if len(filtered) % books_per_page > 0 else 1)
        if total_pages > 1:
            page = st.selectbox("", range(1, total_pages + 1), 
                              format_func=lambda x: f"{x}/{total_pages}", 
                              key="page_select", label_visibility="collapsed")
        else:
            page = 1

    # Apply sorting
    ascending = (sort_order == "↑")
    if sort_by == "Title":
        filtered = filtered.sort_values('title', ascending=ascending)
    elif sort_by == "Author" and 'author' in filtered.columns:
        filtered = filtered.sort_values('author', ascending=ascending)
    elif sort_by == "Rating" and 'average_rating' in filtered.columns:
        filtered = filtered.sort_values('average_rating', ascending=ascending)
    
    # Pagination
    if total_pages > 1:
        start_idx = (page - 1) * books_per_page
        end_idx = start_idx + books_per_page
        page_df = filtered.iloc[start_idx:end_idx]
    else:
        page_df = filtered.head(books_per_page)
    
    # Display books
    for _, book in page_df.iterrows():
        display_book_card(book, show_add_button=True, compact=True)

def display_my_library():
    if not st.session_state.my_books:
        st.markdown("""
        <div class="empty-state">
            <h3>📖 Your library is waiting to be filled!</h3>
            <p>Head over to 'Discover Books' to start building your personal collection.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    my_books_df = pd.DataFrame(st.session_state.my_books)

    total_books = len(my_books_df)
    avg_rating = my_books_df['rating'].mean() if not my_books_df.empty else 0
    unique_authors = my_books_df['author'].nunique() if 'author' in my_books_df.columns else 0
    if not my_books_df.empty:
        latest_book = max(st.session_state.my_books, key=lambda x: x['date_added'])
        days_ago = (datetime.now() - datetime.strptime(latest_book['date_added'], '%Y-%m-%d')).days
    else:
        days_ago = 0
    st.caption(f"📚 {total_books} book{'s' if total_books != 1 else ''} • ⭐ {avg_rating:.1f} avg • ✍️ {unique_authors} author{'s' if unique_authors != 1 else ''} • 📅 {days_ago} days ago")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        search_my_books = st.text_input("Search your books", placeholder="Title or author...")
    with col2:
        min_rating = st.slider("Minimum Rating", 1, 5, 1)

    # Apply filters to library
    filtered_books = my_books_df.copy()
    if search_my_books:
        mask = (
            filtered_books['title'].str.contains(search_my_books, case=False, na=False) |
            filtered_books['author'].str.contains(search_my_books, case=False, na=False)
        )
        filtered_books = filtered_books[mask]
    
    filtered_books = filtered_books[filtered_books['rating'] >= min_rating]

    # Display books
    for idx, book in filtered_books.iterrows():
        display_book_card(book, show_add_button=False, show_remove_button=True, compact=True)

def show_reading_insights():
    """Show reading insights and statistics"""
    st.markdown("### 📊 Reading Insights")
    
    # Dataset analytics
    if not st.session_state.books_df.empty:
        st.subheader("📖 Collection Overview")
        df = st.session_state.books_df
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution
            if 'genre' in df.columns:
                all_genres = {}
                for _, row in df.iterrows():
                    genre_data = row['genre']
                    parsed_genres = parse_genres(genre_data)
                    for genre in parsed_genres:
                        all_genres[genre] = all_genres.get(genre, 0) + 1
                
                if all_genres:
                    genre_df = pd.DataFrame(list(all_genres.items()), columns=['Genre', 'Count'])
                    genre_df = genre_df.sort_values('Count', ascending=False).head(10)
                    st.subheader("📚 Popular Genres in Collection")
                    st.bar_chart(genre_df.set_index('Genre')['Count'])
        
        with col2:
            # Rating distribution
            if 'average_rating' in df.columns:
                st.subheader("⭐ Rating Distribution in Collection")
                rating_data = df['average_rating'].dropna()
                if not rating_data.empty:
                    rating_bins = pd.cut(rating_data, bins=[0, 1, 2, 3, 4, 5], labels=['1⭐', '2⭐', '3⭐', '4⭐', '5⭐'])
                    rating_counts = rating_bins.value_counts().sort_index()
                    st.bar_chart(rating_counts)
    
    # Personal library analytics
    if st.session_state.my_books:
        st.markdown("---")
        st.subheader("📚 Your Reading Profile")
        my_books_df = pd.DataFrame(st.session_state.my_books)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution in personal library
            all_personal_genres = {}
            for book in st.session_state.my_books:
                genre_data = book.get('genre', 'Unknown')
                parsed_genres = parse_genres(genre_data)
                for genre in parsed_genres:
                    all_personal_genres[genre] = all_personal_genres.get(genre, 0) + 1
            
            if all_personal_genres:
                st.subheader("📚 Your Favorite Genres")
                personal_genre_df = pd.DataFrame(list(all_personal_genres.items()), columns=['Genre', 'Count'])
                st.bar_chart(personal_genre_df.set_index('Genre')['Count'])
        
        with col2:
            rating_counts = my_books_df['rating'].value_counts().sort_index()
            st.subheader("⭐ Your Rating Patterns")
            rating_labels = {1: '1⭐', 2: '2⭐', 3: '3⭐', 4: '4⭐', 5: '5⭐'}
            rating_counts.index = rating_counts.index.map(rating_labels)
            st.bar_chart(rating_counts)
        
        # Reading timeline
        my_books_df['date_added'] = pd.to_datetime(my_books_df['date_added'])
        books_per_day = my_books_df.groupby(my_books_df['date_added'].dt.date).size()
        
        if len(books_per_day) > 1:
            st.subheader("📈 Library Growth Over Time")
            st.line_chart(books_per_day)
        
        # Summary stats
        st.subheader("📊 Reading Statistics Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Books", len(my_books_df))
        with col2:
            avg_rating = my_books_df['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}⭐")
        with col3:
            if all_personal_genres:
                favorite_genre = max(all_personal_genres, key=all_personal_genres.get)
                st.metric("Favorite Genre", favorite_genre)
            else:
                st.metric("Favorite Genre", "None")
        with col4:
            unique_authors = my_books_df['author'].nunique()
            st.metric("Unique Authors", unique_authors)
        
        # Recent additions
        st.subheader("📅 Recent Additions")
        recent_books = sorted(st.session_state.my_books, key=lambda x: x['date_added'], reverse=True)[:5]
        for book in recent_books:
            days_ago = (datetime.now() - datetime.strptime(book['date_added'], '%Y-%m-%d')).days
            st.write(f"📖 **{book['title']}** by {book['author']} - Added {days_ago} days ago")
    else:
        st.markdown("""
        <div class="empty-state">
            <h3>📊 No reading data yet!</h3>
            <p>Add some books to your library to see your reading insights and analytics.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application"""
    # Load personal books on startup
    if not st.session_state.my_books:
        st.session_state.my_books = load_my_books()
    
    # Auto-load dataset
    if not st.session_state.loaded_data:
        with st.spinner("Loading book collection..."):
            st.session_state.books_df = load_data()
            st.session_state.loaded_data = True
    
    # Sidebar with library-themed styling
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-brand">📚 BookHaven</div>
        <div class="sidebar-subtitle">Personal Library System</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation section
    st.sidebar.markdown("""
    <div class="navigation-section">
        <div class="nav-title">Navigation</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.sidebar.radio("", [
        "Discover Books", 
        "My Library", 
        "Reading Insights"
    ])
    
    # Show recent additions
    if st.session_state.my_books and len(st.session_state.my_books) > 0:
        st.sidebar.markdown("""
        <div class="navigation-section">
            <div class="nav-title recently-added-title">Recently Added</div>
        </div>
        """, unsafe_allow_html=True)
        recent_books = sorted(st.session_state.my_books, key=lambda x: x['date_added'], reverse=True)[:3]
        for book in recent_books:
            st.sidebar.markdown(f"""
            <div class="recent-book">
                📖 {book['title'][:25]}{'...' if len(book['title']) > 25 else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="navigation-section">
            <div class="nav-title">Getting Started</div>
            <p style='color: #2c3e50; font-size: 0.75rem; margin: 0.4rem 0; line-height: 1.3;'>
                Welcome to your personal library! Start by discovering books and adding them to your collection.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if page == "Discover Books":
        discover_books()
    elif page == "My Library":
        display_my_library()
    elif page == "Reading Insights":
        show_reading_insights()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #2c3e50; font-size: 0.7rem; background: rgba(248, 249, 250, 0.9); backdrop-filter: blur(5px); padding: 6px; border-radius: 4px; border: 1px solid rgba(0, 0, 0, 0.1); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);'>
        <p style='margin: 0;'>📚 BookHaven - Your Personal Library</p>
        <p style='margin: 0; opacity: 0.7;'>Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
