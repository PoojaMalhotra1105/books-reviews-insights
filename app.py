import streamlit as st
import pandas as pd
import json
import os
import random
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="☀️ Summer Reading List Builder",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for summer reading theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FFB347 0%, #FFD700 50%, #FFA500 100%);
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #FF7043 0%, #FFB347 100%);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 15px rgba(255, 112, 67, 0.3);
    }
    
    .sidebar-brand {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar-subtitle {
        font-size: 0.85rem;
        color: #ffffff;
        font-weight: 400;
        opacity: 0.95;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .navigation-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(5px);
        padding: 0.6rem;
        border-radius: 10px;
        margin-bottom: 0.4rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .nav-title {
        color: #FF7043;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .summer-book-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(255, 112, 67, 0.2);
        border-left: 4px solid #FFB347;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .summer-book-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 112, 67, 0.3);
    }
    
    .compact-summer-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 12px rgba(255, 112, 67, 0.2);
        border: 1px solid rgba(255, 180, 71, 0.3);
        border-left: 4px solid #FF7043;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .compact-summer-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(255, 112, 67, 0.3);
    }
    
    .ultra-compact-summer-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(255, 112, 67, 0.15);
        border: 1px solid rgba(255, 180, 71, 0.2);
        border-left: 3px solid #FFB347;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    
    .ultra-compact-summer-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 112, 67, 0.25);
    }
    
    .summer-empty-state {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 248, 220, 0.95) 100%);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px rgba(255, 140, 0, 0.2);
        border: 2px solid rgba(255, 165, 0, 0.3);
        border-top: 4px solid #FFB347;
    }
    
    .summer-empty-state h3 {
        color: #FF7043;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .summer-empty-state p {
        color: #5D4037;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .summer-stat {
        background: linear-gradient(135deg, rgba(255, 248, 220, 0.9) 0%, rgba(255, 235, 205, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 165, 0, 0.3);
        box-shadow: 0 3px 10px rgba(255, 140, 0, 0.2);
    }
    
    .stat-number {
        color: #FF7043;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .stat-label {
        color: #8D6E63;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .recent-summer-book {
        color: #5D4037;
        font-size: 0.75rem;
        margin-bottom: 0.4rem;
        padding: 0.4rem;
        background: linear-gradient(135deg, rgba(255, 248, 220, 0.8) 0%, rgba(255, 235, 205, 0.8) 100%);
        backdrop-filter: blur(10px);
        border-radius: 6px;
        border-left: 3px solid #FFB347;
        box-shadow: 0 2px 8px rgba(255, 140, 0, 0.15);
    }
    
    .summer-recommendation {
        background: linear-gradient(135deg, rgba(255, 239, 213, 0.9) 0%, rgba(255, 224, 178, 0.9) 100%);
        border: 2px solid rgba(255, 152, 0, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
    }
    
    .summer-genre-tag {
        background: linear-gradient(135deg, #FFB347 0%, #FFA500 100%);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        margin: 0.1rem;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(255, 165, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'books_df' not in st.session_state:
    st.session_state.books_df = pd.DataFrame()
if 'summer_reading_list' not in st.session_state:
    st.session_state.summer_reading_list = []
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = False

# File to store summer reading list
SUMMER_LIST_FILE = 'summer_reading_list.json'

# Summer genre recommendations and emoji mapping
summer_genre_icons = {
    "Romance": "💕", "Adventure": "🏖️", "Mystery": "🕵️", "Fantasy": "🧚", 
    "Science Fiction": "🚀", "Historical Fiction": "🏛️", "Contemporary": "🌻", 
    "Thriller": "⚡", "Young Adult": "🌅", "Comedy": "😎", "Travel": "✈️",
    "Memoir": "📖", "Self-Help": "🌱", "Biography": "👤", "Literary Fiction": "📚",
    "Beach Read": "🏖️", "Light Fiction": "☀️", "Escapist": "🌴", "Feel-Good": "🌈"
}

def load_sample_summer_data():
    """Load sample summer reading data"""
    summer_books = {
        'title': [
            'Beach Read', 'The Seven Husbands of Evelyn Hugo', 'Where the Crawdads Sing', 
            'The Summer I Turned Pretty', 'It Ends with Us', 'The Midnight Library',
            'Project Hail Mary', 'Klara and the Sun', 'The Invisible Life of Addie LaRue',
            'The Guest List', 'Malibu Rising', 'The Sanatoriums', 'The Thursday Murder Club',
            'Educated', 'Atomic Habits', 'Becoming', 'The Alchemist', 'Big Little Lies',
            'Gone Girl', 'The Girl on the Train'
        ],
        'author': [
            'Emily Henry', 'Taylor Jenkins Reid', 'Delia Owens', 'Jenny Han', 
            'Colleen Hoover', 'Matt Haig', 'Andy Weir', 'Kazuo Ishiguro',
            'V.E. Schwab', 'Lucy Foley', 'Taylor Jenkins Reid', 'Sarah Pearse',
            'Richard Osman', 'Tara Westover', 'James Clear', 'Michelle Obama',
            'Paulo Coelho', 'Liane Moriarty', 'Gillian Flynn', 'Paula Hawkins'
        ],
        'year': [
            2020, 2017, 2018, 2009, 2016, 2020, 2021, 2021, 2020, 2020,
            2021, 2021, 2020, 2018, 2018, 2018, 1988, 2014, 2012, 2015
        ],
        'average_rating': [
            4.05, 4.25, 4.41, 4.20, 4.30, 4.15, 4.52, 4.01, 4.28, 4.01,
            3.95, 3.91, 4.26, 4.47, 4.34, 4.44, 3.88, 4.05, 4.08, 3.88
        ],
        'genre': [
            'Romance', 'Contemporary', 'Literary Fiction', 'Young Adult',
            'Romance', 'Literary Fiction', 'Science Fiction', 'Literary Fiction',
            'Fantasy', 'Mystery', 'Contemporary', 'Thriller', 'Mystery',
            'Memoir', 'Self-Help', 'Biography', 'Philosophy', 'Contemporary',
            'Thriller', 'Mystery'
        ],
        'summer_appeal': [
            'Perfect beach read with romance and humor',
            'Glamorous Hollywood story, great for poolside',
            'Beautiful nature writing, atmospheric',
            'Coming-of-age summer romance classic',
            'Emotional contemporary romance',
            'Thought-provoking yet accessible',
            'Fun space adventure with humor',
            'Gentle literary fiction',
            'Magical historical fantasy',
            'Gripping thriller set on an island',
            'Family drama set in Malibu',
            'Atmospheric thriller in the Alps',
            'Cozy British mystery series',
            'Inspiring memoir about education',
            'Practical self-improvement',
            'Inspiring political memoir',
            'Philosophical journey story',
            'Domestic drama with dark secrets',
            'Psychological thriller page-turner',
            'Suspenseful domestic thriller'
        ]
    }
    return pd.DataFrame(summer_books)

def load_data():
    """Load book data from CSV or create sample summer data"""
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
        
        st.info("📝 No CSV file found. Using curated summer reading recommendations.")
        return load_sample_summer_data()
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Using sample summer reading data instead.")
        return load_sample_summer_data()

def load_summer_list():
    """Load summer reading list from JSON file"""
    if os.path.exists(SUMMER_LIST_FILE):
        try:
            with open(SUMMER_LIST_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_summer_list():
    """Save summer reading list to JSON file"""
    with open(SUMMER_LIST_FILE, 'w') as f:
        json.dump(st.session_state.summer_reading_list, f, indent=2)

def parse_genres(genre_data):
    """Parse genre data into a list of individual genres"""
    if pd.isna(genre_data) or genre_data == '' or genre_data is None:
        return ['Contemporary']
    
    genre_str = str(genre_data).strip()
    
    if not genre_str or genre_str.lower() in ['unknown', 'n/a', 'none', 'nan']:
        return ['Contemporary']
    
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
    
    return clean_genres if clean_genres else ['Contemporary']

def get_summer_appeal_score(book):
    """Calculate summer appeal score based on genre and rating"""
    genre_data = book.get('genre', 'Contemporary')
    parsed_genres = parse_genres(genre_data)
    rating = book.get('average_rating', 3.5)
    
    # Summer-friendly genres get bonus points
    summer_friendly_genres = [
        'Romance', 'Contemporary', 'Adventure', 'Mystery', 'Young Adult',
        'Comedy', 'Travel', 'Self-Help', 'Biography', 'Light Fiction'
    ]
    
    genre_bonus = 0
    for genre in parsed_genres:
        if any(summer_genre in genre for summer_genre in summer_friendly_genres):
            genre_bonus += 0.5
    
    base_score = float(rating) if pd.notna(rating) else 3.5
    return min(5.0, base_score + genre_bonus)

def display_summer_book_card(book, show_add_button=True, compact=False, show_remove_button=False):
    """Display a summer-themed book card"""
    genre_data = book.get('genre', 'Contemporary')
    parsed_genres = parse_genres(genre_data)
    
    # Get summer appeal description
    summer_appeal = book.get('summer_appeal', 'Great for summer reading')
    
    if parsed_genres and parsed_genres != ['Contemporary']:
        genre_display = " ".join([summer_genre_icons.get(g, "📚") + " " + g for g in parsed_genres[:2]])
    else:
        genre_display = "📚 Contemporary"
    
    card_class = "ultra-compact-summer-card" if compact else "summer-book-card"
    
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
            st.markdown(f'<div class="book-title" style="font-size: 1rem; margin-bottom: 0.2rem; color: #FF7043;">{display_title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="book-author" style="font-size: 0.8rem; margin-bottom: 0.2rem; color: #8D6E63;">by {author}</div>', unsafe_allow_html=True)
            
            rating = book.get('average_rating', 0)
            year = book.get('year', 'Unknown')
            
            if pd.notna(rating) and rating > 0:
                rating_display = f"⭐ {float(rating):.1f}"
                summer_score = get_summer_appeal_score(book)
                if summer_score >= 4.0:
                    rating_display += " ☀️"
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
            
            st.markdown(f'<div class="book-details" style="font-size: 0.75rem; margin-bottom: 0.3rem; color: #5D4037;">{rating_display} • {year_display} • {genre_display}</div>', unsafe_allow_html=True)
            
            if summer_appeal and not compact:
                st.markdown(f'<div style="font-size: 0.7rem; color: #FF8C00; font-style: italic; margin-top: 0.3rem;">☀️ {summer_appeal}</div>', unsafe_allow_html=True)
        
        if col_action:
            with col_action:
                if show_add_button:
                    book_id = book.get('work_id', f"{title}_{author}")
                    book_exists = any(book.get('work_id') == book_id or 
                                    (book['title'] == title and book['author'] == author) 
                                    for book in st.session_state.summer_reading_list)
                    
                    if not book_exists:
                        if st.button("➕", key=f"add_{book_id}", type="secondary", help="Add to Summer List"):
                            new_book = {
                                'id': len(st.session_state.summer_reading_list) + 1,
                                'work_id': book_id,
                                'title': title,
                                'author': author,
                                'genre': book.get('genre', 'Contemporary'),
                                'rating': int(float(rating)) if pd.notna(rating) and rating > 0 else 4,
                                'average_rating': float(rating) if pd.notna(rating) else None,
                                'year': year,
                                'summer_appeal': summer_appeal,
                                'date_added': datetime.now().strftime("%Y-%m-%d"),
                                'source': 'recommendations'
                            }
                            st.session_state.summer_reading_list.append(new_book)
                            save_summer_list()
                            st.success(f"Added '{title}' to your summer reading list! ☀️")
                            st.rerun()
                    else:
                        st.markdown("✅")
                
                elif show_remove_button:
                    book_id = book.get('work_id', f"{title}_{author}")
                    if st.button("🗑️", key=f"remove_{book_id}", type="secondary", help="Remove from Summer List"):
                        st.session_state.summer_reading_list = [
                            b for b in st.session_state.summer_reading_list
                            if not (b.get('work_id', f"{b['title']}_{b['author']}") == book_id)
                        ]
                        save_summer_list()
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def discover_summer_books():
    """Discover summer reading recommendations"""
    st.markdown("### ☀️ Discover Summer Books")
    
    if st.session_state.books_df.empty:
        st.warning("📚 No book collection available. Please ensure your dataset file is in the project directory.")
        return
    
    df = st.session_state.books_df.copy()
    df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
    
    # Main search bar
    search_term = st.text_input("🔍 Search books, authors, or genres", placeholder="Try 'beach read', 'thriller', or author name...")
    
    # Filters in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Author filter
        if 'author' in df.columns:
            authors_list = ['All Authors'] + sorted(df['author'].dropna().unique().tolist())
            selected_author = st.selectbox("👤 Author", authors_list)
        else:
            selected_author = 'All Authors'
    
    with col2:
        # Genre filter
        all_genres = set()
        for genre_data in df['genre'].dropna():
            parsed_genres = parse_genres(genre_data)
            all_genres.update(parsed_genres)
        
        genres_list = ['All Genres'] + sorted(list(all_genres))
        selected_genre = st.selectbox("📚 Genre", genres_list)
    
    with col3:
        # Rating filter
        if 'average_rating' in df.columns:
            min_rating = st.slider("⭐ Min Rating", 1.0, 5.0, 3.5, step=0.1)
        else:
            min_rating = 1.0
    
    with col4:
        # Summer appeal filter
        min_summer_score = st.slider("☀️ Summer Appeal", 1.0, 5.0, 3.5, step=0.1)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter
    if search_term and search_term.strip():
        search_mask = (
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['author'].str.contains(search_term, case=False, na=False) |
            filtered_df['genre'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
    
    # Author filter
    if selected_author != 'All Authors':
        filtered_df = filtered_df[filtered_df['author'] == selected_author]
    
    # Genre filter
    if selected_genre != 'All Genres':
        genre_mask = filtered_df['genre'].apply(lambda x: selected_genre in parse_genres(x))
        filtered_df = filtered_df[genre_mask]
    
    # Rating filter
    if 'average_rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['average_rating'] >= min_rating]
    
    # Summer appeal filter
    filtered_df = filtered_df[filtered_df['summer_score'] >= min_summer_score]
    
    # Sort by summer score
    recommended_df = filtered_df.sort_values('summer_score', ascending=False)
    
    # Show default recommendations if no filters applied
    if not search_term and selected_author == 'All Authors' and selected_genre == 'All Genres' and min_rating <= 3.5 and min_summer_score <= 3.5:
        st.markdown("#### ⭐ Staff Picks - Highly Recommended Summer Reads")
        recommended_df = df.nlargest(25, 'summer_score')
    
    # Limit results
    max_results = 50
    total_results = len(recommended_df)
    
    if total_results > max_results:
        recommended_df = recommended_df.head(max_results)
        show_limit_message = True
    else:
        show_limit_message = False
    
    # Display results
    displayed_count = len(recommended_df)
    
    if total_results == 0:
        st.warning("🔍 No books match your current filters. Try adjusting your search criteria.")
        return
    
    # Result count message
    if show_limit_message:
        st.markdown(f"### 📖 Showing Top {displayed_count} of {total_results} Books Found")
        st.info(f"💡 Use filters to narrow your search for more specific recommendations.")
    else:
        st.markdown(f"### 📖 {displayed_count} Books Found")
    
    # Display recommendations
    for _, book in recommended_df.iterrows():
        display_summer_book_card(book, show_add_button=True, compact=True)

def display_summer_reading_list():
    """Display and manage the summer reading list"""
    st.markdown("### 🏖️ My Summer Reading List")
    
    if not st.session_state.summer_reading_list:
        st.markdown("""
        <div class="summer-empty-state">
            <h3>☀️ Your summer reading adventure awaits!</h3>
            <p>Start building your perfect summer reading list by discovering books that match your mood and interests.</p>
            <p>🌅 Head over to 'Discover Summer Books' to find your next great read!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    summer_books_df = pd.DataFrame(st.session_state.summer_reading_list)

    # Summer reading stats
    total_books = len(summer_books_df)
    avg_rating = summer_books_df['rating'].mean() if not summer_books_df.empty else 0
    unique_authors = summer_books_df['author'].nunique() if 'author' in summer_books_df.columns else 0
    
    # Calculate reading goal progress
    summer_goal = st.sidebar.number_input("📚 Summer Reading Goal", min_value=1, max_value=50, value=10)
    progress = min(100, (total_books / summer_goal) * 100)
    
    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="summer-stat">
            <div class="stat-number">{total_books}</div>
            <div class="stat-label">Books Added</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="summer-stat">
            <div class="stat-number">{avg_rating:.1f}⭐</div>
            <div class="stat-label">Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="summer-stat">
            <div class="stat-number">{unique_authors}</div>
            <div class="stat-label">Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="summer-stat">
            <div class="stat-number">{progress:.0f}%</div>
            <div class="stat-label">Goal Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress / 100)
    st.caption(f"🎯 {total_books} of {summer_goal} books added to your summer list")
    
    st.markdown("---")

    # Filters for the list
    col1, col2 = st.columns(2)
    with col1:
        search_summer_books = st.text_input("Search your summer list", placeholder="Title or author...")
    with col2:
        min_rating = st.slider("Minimum Rating", 1, 5, 1)

    # Apply filters to summer list
    filtered_books = summer_books_df.copy()
    if search_summer_books:
        mask = (
            filtered_books['title'].str.contains(search_summer_books, case=False, na=False) |
            filtered_books['author'].str.contains(search_summer_books, case=False, na=False)
        )
        filtered_books = filtered_books[mask]
    
    filtered_books = filtered_books[filtered_books['rating'] >= min_rating]

    # Display summer reading list
    st.markdown("### 📚 Your Curated Summer Collection")
    
    if len(filtered_books) == 0:
        st.info("🔍 No books match your filters. Try adjusting your search.")
        return
    
    # Group by genre for better organization
    genre_groups = {}
    for idx, book in filtered_books.iterrows():
        genre_data = book.get('genre', 'Contemporary')
        parsed_genres = parse_genres(genre_data)
        main_genre = parsed_genres[0] if parsed_genres else 'Contemporary'
        
        if main_genre not in genre_groups:
            genre_groups[main_genre] = []
        genre_groups[main_genre].append(book)
    
    # Display by genre sections
    for genre, books in genre_groups.items():
        genre_icon = summer_genre_icons.get(genre, "📚")
        st.markdown(f"#### {genre_icon} {genre} ({len(books)} book{'s' if len(books) != 1 else ''})")
        
        for book in books:
            display_summer_book_card(book, show_add_button=False, show_remove_button=True, compact=True)

def show_summer_insights():
    """Show summer reading insights and recommendations"""
    st.markdown("### 📊 Summer Reading Insights")
    
    # Dataset analytics for summer reading
    if not st.session_state.books_df.empty:
        st.markdown("#### 🌞 Summer Reading Trends")
        df = st.session_state.books_df.copy()
        
        # Calculate summer appeal scores for all books
        df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Most summer-friendly genres
            genre_summer_scores = {}
            for _, row in df.iterrows():
                genre_data = row['genre']
                parsed_genres = parse_genres(genre_data)
                summer_score = row['summer_score']
                
                for genre in parsed_genres:
                    if genre not in genre_summer_scores:
                        genre_summer_scores[genre] = []
                    genre_summer_scores[genre].append(summer_score)
            
            # Calculate average summer scores by genre
            avg_genre_scores = {
                genre: sum(scores) / len(scores) 
                for genre, scores in genre_summer_scores.items() 
                if len(scores) >= 3  # Only include genres with at least 3 books
            }
            
            if avg_genre_scores:
                st.markdown("##### 🏖️ Best Summer Genres")
                sorted_genres = sorted(avg_genre_scores.items(), key=lambda x: x[1], reverse=True)[:8]
                genre_chart_data = pd.DataFrame(sorted_genres, columns=['Genre', 'Summer Appeal Score'])
                st.bar_chart(genre_chart_data.set_index('Genre')['Summer Appeal Score'])
        
        with col2:
            # Summer reading recommendations by rating
            st.markdown("##### ⭐ Highly Rated Summer Books")
            top_summer_books = df[df['summer_score'] >= 4.2].nlargest(10, 'average_rating')
            
            if not top_summer_books.empty:
                for _, book in top_summer_books.head(5).iterrows():
                    genre_data = book.get('genre', 'Contemporary')
                    parsed_genres = parse_genres(genre_data)
                    genre_display = parsed_genres[0] if parsed_genres else 'Contemporary'
                    
                    st.markdown(f"""
                    <div class="summer-recommendation">
                        <strong>{book['title']}</strong><br>
                        <em>by {book['author']}</em><br>
                        <span class="summer-genre-tag">{genre_display}</span>
                        <span style="color: #FF7043;">⭐ {book['average_rating']:.1f}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Personal summer reading analytics
    if st.session_state.summer_reading_list:
        st.markdown("---")
        st.markdown("#### 🏖️ Your Summer Reading Profile")
        summer_books_df = pd.DataFrame(st.session_state.summer_reading_list)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution in summer list
            summer_genres = {}
            for book in st.session_state.summer_reading_list:
                genre_data = book.get('genre', 'Contemporary')
                parsed_genres = parse_genres(genre_data)
                for genre in parsed_genres:
                    summer_genres[genre] = summer_genres.get(genre, 0) + 1
            
            if summer_genres:
                st.markdown("##### 📚 Your Summer Genre Mix")
                summer_genre_df = pd.DataFrame(list(summer_genres.items()), columns=['Genre', 'Count'])
                st.bar_chart(summer_genre_df.set_index('Genre')['Count'])
        
        with col2:
            # Rating distribution
            rating_counts = summer_books_df['rating'].value_counts().sort_index()
            st.markdown("##### ⭐ Your Summer Ratings")
            rating_labels = {1: '1⭐', 2: '2⭐', 3: '3⭐', 4: '4⭐', 5: '5⭐'}
            rating_counts.index = rating_counts.index.map(rating_labels)
            st.bar_chart(rating_counts)
        
        # Summer reading timeline
        summer_books_df['date_added'] = pd.to_datetime(summer_books_df['date_added'])
        books_per_day = summer_books_df.groupby(summer_books_df['date_added'].dt.date).size()
        
        if len(books_per_day) > 1:
            st.markdown("##### 📈 List Building Progress")
            st.line_chart(books_per_day)
        
        # Summer reading recommendations based on preferences
        st.markdown("##### 🌅 Personalized Summer Recommendations")
        
        # Analyze user's genre preferences
        user_favorite_genres = list(summer_genres.keys())[:3] if summer_genres else ['Romance', 'Contemporary']
        
        # Find books that match user preferences but aren't in their list
        if not st.session_state.books_df.empty:
            df = st.session_state.books_df.copy()
            df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
            
            # Get existing book IDs in summer list
            existing_ids = {book.get('work_id', f"{book['title']}_{book['author']}") for book in st.session_state.summer_reading_list}
            
            # Filter recommendations
            recommendations = []
            for _, book in df.iterrows():
                book_id = book.get('work_id', f"{book['title']}_{book['author']}")
                if book_id not in existing_ids:
                    genre_data = book.get('genre', 'Contemporary')
                    parsed_genres = parse_genres(genre_data)
                    
                    # Check if book matches user's preferred genres
                    genre_match = any(user_genre in genre for user_genre in user_favorite_genres for genre in parsed_genres)
                    
                    if genre_match and book['summer_score'] >= 4.0:
                        recommendations.append(book)
            
            # Sort by summer score and display top 3
            recommendations.sort(key=lambda x: x['summer_score'], reverse=True)
            
            if recommendations:
                st.markdown("Based on your current list, you might enjoy:")
                for book in recommendations[:3]:
                    display_summer_book_card(book, show_add_button=True, compact=True)
            else:
                st.info("🎉 Great selection! You've already found some excellent summer reads.")
        
        # Summer reading tips
        st.markdown("##### 💡 Summer Reading Tips")
        tips = [
            "🏖️ Pack lighter paperbacks for beach reading",
            "📱 Download audiobooks for road trips and walks", 
            "🌙 Keep a shorter book for bedtime reading",
            "☀️ Mix genres to match different summer moods",
            "👥 Join online book clubs for summer discussions"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
    
    else:
        st.markdown("""
        <div class="summer-empty-state">
            <h3>📊 Start tracking your summer reading!</h3>
            <p>Add books to your summer reading list to see personalized insights and recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application"""
    # Load summer reading list on startup
    if not st.session_state.summer_reading_list:
        st.session_state.summer_reading_list = load_summer_list()
    
    # Auto-load dataset
    if not st.session_state.loaded_data:
        with st.spinner("Loading summer reading recommendations..."):
            st.session_state.books_df = load_data()
            st.session_state.loaded_data = True
    
    # Sidebar with summer-themed styling
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-brand">☀️ Summer Reading List Builder</div>
        <div class="sidebar-subtitle">Curate Your Perfect Summer Books</div>
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
        "Discover Summer Books", 
        "My Summer Reading List", 
        "Summer Reading Insights"
    ])
    
    # Show recent additions to summer list
    if st.session_state.summer_reading_list and len(st.session_state.summer_reading_list) > 0:
        st.sidebar.markdown("""
        <div class="navigation-section">
            <div class="nav-title">Recently Added</div>
        </div>
        """, unsafe_allow_html=True)
        recent_books = sorted(st.session_state.summer_reading_list, key=lambda x: x['date_added'], reverse=True)[:3]
        for book in recent_books:
            st.sidebar.markdown(f"""
            <div class="recent-summer-book">
                ☀️ {book['title'][:25]}{'...' if len(book['title']) > 25 else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="navigation-section">
            <div class="nav-title">Summer Reading Goals</div>
            <p style='color: #5D4037; font-size: 0.75rem; margin: 0.4rem 0; line-height: 1.3;'>
                🌞 Build your perfect summer reading list! Discover books that match your mood and create your ideal seasonal collection.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Summer reading tip of the day
    summer_tips = [
        "🏖️ Beach reads should be engaging but not too complex!",
        "📚 Mix different genres to match your summer moods",
        "⏰ Set a realistic summer reading goal",
        "🎧 Audiobooks are perfect for summer walks",
        "👥 Join a summer book club for motivation!"
    ]
    
    daily_tip = random.choice(summer_tips)
    st.sidebar.markdown(f"""
    <div class="navigation-section">
        <div class="nav-title">💡 Summer Reading Tip</div>
        <p style='color: #5D4037; font-size: 0.75rem; margin: 0.4rem 0; line-height: 1.3; font-style: italic;'>
            {daily_tip}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    if page == "Discover Summer Books":
        discover_summer_books()
    elif page == "My Summer Reading List":
        display_summer_reading_list()
    elif page == "Summer Reading Insights":
        show_summer_insights()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #5D4037; font-size: 0.7rem; background: linear-gradient(135deg, rgba(255, 248, 220, 0.9) 0%, rgba(255, 235, 205, 0.9) 100%); backdrop-filter: blur(10px); padding: 8px; border-radius: 6px; border: 1px solid rgba(255, 165, 0, 0.3); box-shadow: 0 2px 8px rgba(255, 140, 0, 0.15);'>
        <p style='margin: 0;'>☀️ Summer Reading List Builder</p>
        <p style='margin: 0; opacity: 0.8;'>Make this summer unforgettable with great books!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
