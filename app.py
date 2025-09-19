# app.py - Fixed Streamlit App with Better Error Handling
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import re
from collections import Counter
from pathlib import Path
import base64
import io
import os

# Page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1f77b4; margin-bottom: 0;}
    .sub-header {color: #ff7f0e; font-weight: bold;}
    .metric-card {background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center;}
    .error-box {background-color: #ffebee; padding: 15px; border-radius: 10px; border-left: 5px solid #f44336;}
</style>
""", unsafe_allow_html=True)

# Load data with better error handling
@st.cache_data
def load_data():
    try:
        # Try multiple possible locations for the data file
        possible_paths = [
            Path.home() / "Desktop" / "cleaned_cord19_data.csv",
            Path.cwd() / "cleaned_cord19_data.csv",
            Path.home() / "Documents" / "cleaned_cord19_data.csv"
        ]
        
        data_file = None
        for path in possible_paths:
            if path.exists():
                data_file = path
                break
        
        if data_file is None:
            st.error("❌ Data file not found. Please make sure 'cleaned_cord19_data.csv' exists.")
            return None
        
        st.info(f"📁 Loading data from: {data_file}")
        df = pd.read_csv(data_file)
        
        # Basic validation
        if len(df) == 0:
            st.error("❌ The data file is empty.")
            return None
        
        # Convert date columns if they exist
        if 'publish_time' in df.columns:
            df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
            df['publication_year'] = df['publish_time'].dt.year.fillna(2020).astype(int)
        
        # Ensure required columns exist
        required_columns = ['title', 'journal', 'abstract']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"❌ Required column '{col}' not found in data.")
                return None
        
        # Create word count columns if they don't exist
        if 'title_word_count' not in df.columns:
            df['title_word_count'] = df['title'].apply(lambda x: len(str(x).split()))
        
        if 'abstract_word_count' not in df.columns:
            df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Demo data for testing if real data fails
def create_demo_data():
    """Create sample data for demonstration"""
    return pd.DataFrame({
        'title': ['COVID-19 Vaccine Efficacy Study', 'Pandemic Response Analysis', 'Virus Transmission Patterns'],
        'authors': ['Smith et al.', 'Johnson et al.', 'Williams et al.'],
        'journal': ['Medical Journal', 'Health Review', 'Science Today'],
        'publication_year': [2020, 2021, 2022],
        'abstract': ['Study of vaccine effectiveness', 'Analysis of pandemic response', 'Patterns of virus transmission'],
        'title_word_count': [4, 3, 3],
        'abstract_word_count': [3, 4, 4]
    })

# Main app
def main():
    st.markdown('<h1 class="main-header">📊 CORD-19 COVID-19 Research Explorer</h1>', unsafe_allow_html=True)
    st.markdown("Explore metadata from COVID-19 research papers (2019-2023)")
    
    # Load data
    with st.spinner("Loading data... Please wait."):
        df = load_data()
    
    # If data loading failed, use demo data
    if df is None:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.warning("⚠️ Using demonstration data. To use your real data:")
        st.write("1. Run the data cleaning script first")
        st.write("2. Save the file as 'cleaned_cord19_data.csv'")
        st.write("3. Place it on your Desktop or in the same folder as this app")
        st.markdown('</div>', unsafe_allow_html=True)
        
        df = create_demo_data()
        st.info("📊 Demonstration mode activated with sample data")
    
    # Display success message only if we have real data
    if len(df) > 3:  # More than demo data
        st.success(f"✅ Data loaded successfully! {len(df):,} research papers")
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters & Controls")
    
    # Year filter
    min_year = int(df['publication_year'].min())
    max_year = int(df['publication_year'].max())
    year_range = st.sidebar.slider(
        "Select Publication Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Journal filter
    journals = ['All Journals'] + sorted([j for j in df['journal'].unique() if pd.notna(j)])
    selected_journal = st.sidebar.selectbox(
        "Filter by Journal",
        options=journals,
        index=0
    )
    
    # Apply filters
    filtered_df = df[df['publication_year'].between(year_range[0], year_range[1])]
    
    if selected_journal != 'All Journals':
        filtered_df = filtered_df[filtered_df['journal'] == selected_journal]
    
    # Main content
    st.sidebar.info(f"**Filter Results:**\n{len(filtered_df):,} papers\n{year_range[0]} - {year_range[1]}")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Papers", f"{len(filtered_df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Journals", filtered_df['journal'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_title = filtered_df['title_word_count'].mean()
        st.metric("Avg Title Words", f"{avg_title:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_abstract = filtered_df['abstract_word_count'].mean()
        st.metric("Avg Abstract Words", f"{avg_abstract:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualizations
    st.markdown("---")
    st.markdown('<h2 class="sub-header">📈 Visualizations</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Publication Trends", "Journal Analysis", "Content Analysis", "Data Explorer"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Publications by Year")
            yearly_counts = filtered_df['publication_year'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(yearly_counts.index.astype(str), yearly_counts.values, color='skyblue', alpha=0.7)
            ax.set_title('Number of Publications by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Top Journals")
        top_journals = filtered_df['journal'].value_counts().head(10)
        if len(top_journals) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            top_journals.plot(kind='barh', color='lightgreen', ax=ax)
            ax.set_title('Top Journals by Publication Count')
            ax.set_xlabel('Number of Publications')
            plt.gca().invert_yaxis()
            st.pyplot(fig)
        else:
            st.info("No journal data available for current filters")
    
    with tab3:
        st.subheader("Word Cloud - Titles")
        if len(filtered_df) > 0:
            try:
                all_titles = ' '.join(filtered_df['title'].dropna().astype(str).str.lower())
                wordcloud = WordCloud(width=600, height=400, background_color='white').generate(all_titles)
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                ax.set_title('Common Words in Paper Titles')
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"Could not generate word cloud: {e}")
        else:
            st.info("No data available for word cloud")
    
    with tab4:
        st.subheader("Data Preview")
        display_columns = [col for col in ['title', 'authors', 'journal', 'publication_year'] if col in filtered_df.columns]
        
        if len(display_columns) > 0:
            st.dataframe(
                filtered_df[display_columns].head(20),
                height=400,
                use_container_width=True
            )
            
            # Download button
            csv = filtered_df[display_columns].to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name="filtered_cord19_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No data available for preview")
    
    # Instructions for real data
    if len(df) <= 3:  # Demo data
        st.markdown("---")
        st.markdown("### 📋 How to Use Your Real Data")
        st.write("""
        1. **Run the data cleaning script** to process your CORD-19 metadata
        2. **Save the cleaned data** as `cleaned_cord19_data.csv`
        3. **Place the file** on your Desktop or in the same folder as this app
        4. **Restart this app** to load your real data
        """)

# Run the app
if __name__ == "__main__":
    main()