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

# Custom CSS for summer reading theme
st.markdown("""
<style>
    /* Main app styling with summer gradient background */
    .stApp {
        background: linear-gradient(135deg, #FFB347 0%, #FFD700 50%, #FFA500 100%);
    }
    
    /* Sidebar styling with summer theme */
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
    
    /* Summer-themed metrics styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.95);
        padding: 0.4rem 0.6rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 180, 71, 0.3);
        margin-bottom: 0.3rem;
        box-shadow: 0 2px 8px rgba(255, 112, 67, 0.2);
    }
    
    .stMetric [data-testid="metric-container"] {
        padding: 0.2rem 0;
    }
    
    .stMetric [data-testid="metric-container"] > div:first-child {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #FF7043 !important;
    }
    
    /* Summer book card styling */
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
    
    /* Summer reading list styling */
    .summer-list-card {
        background: linear-gradient(135deg, rgba(255, 248, 220, 0.95) 0%, rgba(255, 235, 205, 0.95) 100%);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(255, 140, 0, 0.2);
        border: 2px solid rgba(255, 165, 0, 0.3);
        border-top: 4px solid #FF8C00;
    }
    
    /* Summer-themed buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF7043 0%, #FFB347 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        box-shadow: 0 3px 10px rgba(255, 112, 67, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%);
        color: white;
        box-shadow: 0 6px 15px rgba(255, 112, 67, 0.4);
        transform: translateY(-2px);
    }
    
    /* Empty state styling for summer theme */
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
    
    /* Summer reading stats */
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
    
    /* Recent additions for summer theme */
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
    
    /* Form styling for summer theme */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 180, 71, 0.3);
        border-radius: 8px;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: #FFB347;
        box-shadow: 0 0 10px rgba(255, 180, 71, 0.3);
    }
    
    /* Summer reading recommendations */
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

# Summer reading preferences
summer_moods = {
    "Beach Vibes": ["Romance", "Contemporary", "Light Fiction", "Comedy"],
    "Adventure Seeker": ["Adventure", "Thriller", "Fantasy", "Science Fiction"],  
    "Cozy Reader": ["Mystery", "Historical Fiction", "Literary Fiction", "Biography"],
    "Escape Reality": ["Fantasy", "Science Fiction", "Young Adult", "Escapist"],
    "Learn & Grow": ["Self-Help", "Biography", "Memoir", "Philosophy"]
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
    
    # Summer reading mood selector
    st.markdown("#### 🌅 What's your summer reading mood?")
    selected_mood = st.selectbox(
        "Choose your vibe:",
        list(summer_moods.keys()),
        help="Select the mood that matches your summer reading goals"
    )
    
    # Display mood description
    mood_descriptions = {
        "Beach Vibes": "Light, fun reads perfect for lounging by the water 🏖️",
        "Adventure Seeker": "Thrilling page-turners for your active summer 🗺️", 
        "Cozy Reader": "Thoughtful stories for quiet summer evenings 🌙",
        "Escape Reality": "Immersive worlds to lose yourself in ✨",
        "Learn & Grow": "Inspiring reads for summer self-improvement 🌱"
    }
    
    st.info(f"💭 {mood_descriptions[selected_mood]}")
    
    # Filter books based on mood
    preferred_genres = summer_moods[selected_mood]
    
    # Calculate summer appeal scores and filter
    df['summer_score'] = df.apply(get_summer_appeal_score, axis=1)
    
    # Filter by preferred genres and high summer scores
    genre_matches = df['genre'].apply(lambda x: any(genre in str(x) for genre in preferred_genres))
    high_ratings = df['summer_score'] >= 3.8
    
    recommended_df = df[genre_matches & high_ratings].sort_values('summer_score', ascending=False)
    
    if len(recommended_df) == 0:
        # Fallback to all books with good summer scores
        recommended_df = df[df['summer_score'] >= 4.0].sort_values('summer_score', ascending=False)
    
    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Refine Your Search")
        
        # Search filter
        search_term = st.text_input("Search books or authors", placeholder="Enter search term...")
        
        # Rating filter
        if 'average_rating' in df.columns:
            min_rating = st.slider("Minimum Rating", 3.0, 5.0, 3.8, step=0.1)
            recommended_df = recommended_df[recommended_df['average_rating'] >= min_rating]
    
    # Apply search filter
    if search_term and search_term.strip():
        search_mask = (
            recommended_df['title'].str.contains(search_term, case=False, na=False) |
            recommended_df['author'].str.contains(search_term, case=False, na=False)
        )
        recommended_df = recommended_df[search_mask]
    
   # Display results
st.markdown(f"### 📖 {len(recommended_df)} Perfect Matches for '{selected_mood}'")

if len(recommended_df) > 0:
    for _, book in recommended_df.iterrows():
        display_summer_book_card(book, show_add_button=True)
else:
    st.markdown("""
    <div class="summer-empty-state">
        <h3>No books found for your current filters</h3>
        <p>Try adjusting your search criteria or rating threshold to discover more summer reads!</p>
    </div>
    """, unsafe_allow_html=True)
