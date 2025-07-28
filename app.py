# main.py - Your main Streamlit app file
import streamlit as st
from pages import landing, collection_overview, recommendations

def main():
    st.set_page_config(
        page_title="Books, Reviews & Insights",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'
    
    # Hide Streamlit's default menu and footer for landing page
    if st.session_state.current_page == 'landing':
        hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 0rem;}
        </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == 'landing':
        landing.show()
    elif st.session_state.current_page == 'collection_overview':
        collection_overview.show()
    elif st.session_state.current_page == 'recommendations':
        recommendations.show()

if __name__ == "__main__":
    main()

# ===== pages/landing.py =====
import streamlit as st
import streamlit.components.v1 as components

def show():
    # Your landing page HTML (same as above)
    landing_html = """
    <!-- Your complete landing page HTML here -->
    """
    
    # Display landing page
    components.html(landing_html, height=1200, scrolling=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Explore Your Collection", key="to_collection", type="primary"):
            st.session_state.current_page = 'collection_overview'
            st.rerun()

# ===== pages/collection_overview.py =====
import streamlit as st

def show():
    # Navigation
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
    with col3:
        if st.button("💡 Recommendations"):
            st.session_state.current_page = 'recommendations'
            st.rerun()
    
    st.title("📊 Collection Overview")
    
    # Your existing collection overview content
    # This is where your current localhost:8501/#collection-overview content goes
    
    # Example content
    st.subheader("Your Reading Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Books", "142", "12")
    with col2:
        st.metric("Books Read", "89", "8")
    with col3:
        st.metric("Average Rating", "4.2", "0.1")
    with col4:
        st.metric("Reading Goal", "75%", "5%")

# ===== pages/recommendations.py =====
import streamlit as st

def show():
    # Navigation
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
    with col2:
        if st.button("📊 Collection"):
            st.session_state.current_page = 'collection_overview'
            st.rerun()
    
    st.title("💡 Book Recommendations")
    st.write("Based on your reading history and preferences...")
    
    # Your recommendation logic here
