import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path
import os
import io

# Configuration variables
GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScPZoL1rmqr3nJvRqixQlvBphF4Tbj3MrLd9U6WyQjTLzs5hg/viewform?usp=dialog"
KOBOTOOLBOX_LINK = "https://ee.kobotoolbox.org/x/LNbLn5W1"
WARDROBE_BACKGROUND_URL = "https://www.journaldutextile.com/wp-content/uploads/2024/03/garde-robe-masculine.jpg"

# Database Configuration
DB_PATH = "coinafrique_data.db"
CSV_FOLDER = "data"

# Ensure data folder exists for CSV loading/saving
Path(CSV_FOLDER).mkdir(exist_ok=True)

# CSV Files Configuration (Assumes these files exist in the 'data' folder for the CSV Viewer)
CSV_FILES = {
    "👔 Vêtements Homme": "vetement_homme.csv",
    "👶 Vêtements Enfant": "vetements_enfant.csv",
    "👞 Chaussures Homme": "chaussures_hommes.csv",
    "👟 Chaussures Enfant": "chaussure_enfant.csv"
}

# Page Configuration
st.set_page_config(
    page_title="Coinafrique Scraper Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS (KEEP AS IS)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
    }}
    
    /* Background global */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.70), rgba(250, 250, 250, 0.70)),
                    url('{WARDROBE_BACKGROUND_URL}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    /* SIDEBAR - Bleu élégant */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1a237e 0%, #0d47a1 100%) !important;
        box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    }}
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown {{
        color: #ffffff !important;
        font-weight: 600;
    }}
    
    /* Main content container */
    .main .block-container {{
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
    }}
    
    /* TITLES */
    .main-title {{
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 50%, #42a5f5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }}
    
    .subtitle {{
        text-align: center;
        color: #546e7a;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.7;
    }}
    
    /* Welcome specific */
    .welcome-title {{
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: 3px;
    }}
    
    .welcome-subtitle {{
        text-align: center;
        color: #546e7a;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }}
    
    /* Feature cards */
    .feature-card {{
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(21, 101, 192, 0.1);
    }}
    
    .feature-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(21, 101, 192, 0.2);
    }}
    
    .feature-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }}
    
    .feature-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #1565c0;
        margin-bottom: 0.5rem;
    }}
    
    .feature-text {{
        color: #546e7a;
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    /* BUTTONS */
    .stButton>button {{
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%) !important;
        color: white !important;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 18px 40px;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        width: 100%;
        box-shadow: 0 8px 25px rgba(21, 101, 192, 0.4);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(21, 101, 192, 0.6);
    }}
    
    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #ff9800 0%, #ffa726 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 15px 30px;
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
        text-transform: uppercase;
    }}
    
    .stDownloadButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 152, 0, 0.6);
    }}
    
    /* METRICS */
    [data-testid="stMetricValue"] {{
        color: #1565c0;
        font-weight: 800;
        font-size: 2rem;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #546e7a;
        font-weight: 600;
    }}
    
    /* ALERTS */
    .stAlert {{
        border-radius: 12px;
        border-left: 5px solid #1976d2;
        background: rgba(25, 118, 210, 0.05);
    }}
    
    /* PROGRESS BAR */
    .stProgress > div > div {{
        background: linear-gradient(90deg, #1565c0 0%, #42a5f5 100%);
        border-radius: 10px;
    }}
    
    /* DATAFRAME */
    [data-testid="stDataFrame"] {{
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }}
    
    /* IMAGES */
    img {{
        border-radius: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }}
    
    img:hover {{
        transform: scale(1.05);
        box-shadow: 0 10px 35px rgba(21, 101, 192, 0.3);
    }}
    
    /* SEPARATOR */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #1976d2 50%, transparent 100%);
        margin: 2rem 0;
    }}
    
    /* LINK BUTTONS */
    .stLinkButton > a {{
        background: linear-gradient(135deg, #00897b 0%, #26a69a 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 15px 30px;
        text-decoration: none;
        display: inline-block;
        width: 100%;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 137, 123, 0.4);
        transition: all 0.3s ease;
    }}
    
    .stLinkButton > a:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 137, 123, 0.6);
    }}
</style>
""", unsafe_allow_html=True)

# Category Configuration
CATEGORIES = {
    "Men's Clothing": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "icon": "👔",
        "column": "type_habits",
        "color": "#1565c0",
        "table": "mens_clothing"
    },
    "Men's Shoes": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "icon": "👞",
        "column": "type_shoes",
        "color": "#1976d2",
        "table": "mens_shoes"
    },
    "Children's Clothing": {
        "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "icon": "👶",
        "column": "type_clothes",
        "color": "#42a5f5",
        "table": "children_clothing"
    },
    "Children's Shoes": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "icon": "👟",
        "column": "type_shoes",
        "color": "#64b5f6",
        "table": "children_shoes"
    }
}

# ========================== DATABASE FUNCTIONS ==========================

def init_database():
    """Initialize SQLite database and create tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables for each category
    for cat_name, cat_info in CATEGORIES.items():
        table_name = cat_info['table']
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {cat_info['column']} TEXT,
                price TEXT,
                adress TEXT,
                img TEXT,
                scrape_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    conn.commit()
    conn.close()

def save_to_database(df, table_name, column_name):
    """Save DataFrame to SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Add scrape_date column if not exists
        if 'scrape_date' not in df.columns:
            df['scrape_date'] = pd.Timestamp.now()
        
        # Rename the category-specific column in the DataFrame to match the DB schema
        # Assuming the DataFrame has one column that matches the category's 'column' name
        # We ensure the DF only contains the columns expected by the DB table.
        df_to_save = df[[column_name, 'price', 'adress', 'img']].copy()
        df_to_save['scrape_date'] = pd.Timestamp.now()
        
        # Append to table
        df_to_save.to_sql(table_name, conn, if_exists='append', index=False)
        
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Database error during save: {str(e)}")
        return False

def get_from_database(table_name):
    """Retrieve data from SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Database error during retrieval: {str(e)}")
        return pd.DataFrame()

def get_database_stats():
    """Get statistics from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        stats = {}
        
        for cat_name, cat_info in CATEGORIES.items():
            table_name = cat_info['table']
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            stats[cat_name] = count
        
        conn.close()
        return stats
    except:
        return {}

# ========================== SCRAPING FUNCTIONS ==========================

def scrape_category(url, num_pages, column_name):
    data = []
    
    # Check if a progress bar is available in session state
    if 'progress_bar' in st.session_state:
        progress_bar = st.session_state['progress_bar']
    else:
        # Fallback for testing/direct use, though Streamlit UI handles it better
        progress_bar = st.empty()

    for i in range(1, num_pages + 1): # Start from page 1 up to num_pages
        try:
            time.sleep(1) # Be polite! Increased delay
            page_url = f'{url}?page={i}'
            
            # Use a short timeout to prevent hanging forever
            res = get(page_url, timeout=10) 
            
            if res.status_code != 200:
                 st.warning(f"⚠️ Page {i} returned status code {res.status_code}. Stopping.")
                 break

            soup = bs(res.content, 'html.parser')
            # Check for empty results page - Coinafrique uses a simple layout 
            if "no-results" in res.text or not soup.find('div', class_='col s6 m4 l3'):
                st.info(f"ℹ️ No more results found on page {i}. Stopping scraping.")
                break
                
            containers = soup.find_all('div', class_='col s6 m4 l3')
            
            if not containers:
                st.info(f"ℹ️ No containers found on page {i}. Stopping scraping.")
                break
                
            for container in containers:
                try:
                    # Extraction des champs
                    item_type_tag = container.find('p', 'ad__card-description')
                    price_tag = container.find('p', class_='ad__card-price')
                    adress_tag = container.find('p', class_='ad__card-location')
                    img_tag = container.find('img', class_='ad__card-img')
                    
                    item_type = item_type_tag.text.strip() if item_type_tag else "N/A"
                    price = price_tag.text.replace('CFA', '').strip() if price_tag else "N/A"
                    adress = adress_tag.text.strip() if adress_tag else "N/A"
                    img = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "No Image"
                    
                    dic = {
                        column_name: item_type,
                        'price': price,
                        'adress': adress,
                        'img': img
                    }
                    data.append(dic)
                except Exception as e_item:
                    # Ignore items that fail to parse
                    # st.warning(f"Item parsing error: {e_item}") 
                    pass
            
            # Update progress bar
            progress = int((i / num_pages) * 100)
            if progress_bar:
                progress_bar.progress(progress)
                
        except Exception as e:
            st.error(f"❌ Error scraping page {i}: {e}")
            break
            
    # Finalize progress bar
    if progress_bar:
        progress_bar.progress(100)
    
    return pd.DataFrame(data)

def clean_price(price_str):
    """Converts price string to float, handling formatting and non-numeric values."""
    try:
        # Remove spaces, commas, periods (common French/African formatting) and keep only digits/known characters
        cleaned = str(price_str).strip().upper()
        if 'FCFA' in cleaned: cleaned = cleaned.replace('FCFA', '')
        if 'CFA' in cleaned: cleaned = cleaned.replace('CFA', '')
        
        # Remove non-digit characters except for space (to handle thousands separation before removal)
        cleaned = ''.join(c for c in cleaned if c.isdigit() or c in ' ')
        cleaned = cleaned.replace(' ', '')
        
        return float(cleaned) if cleaned.isdigit() and cleaned else 0.0
    except:
        return 0.0

def create_charts_for_category(df, cat_name, cat_color):
    """Generates a 4-panel analysis plot."""
    df['price_numeric'] = df['price'].apply(clean_price)
    df_clean = df[df['price_numeric'] > 0]
    
    if len(df_clean) < 10:
        return None
    
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Data Analysis - {cat_name}', fontsize=20, fontweight='bold', y=1.0)
    
    # 1. Price Distribution (Histogram + KDE)
    prices = df_clean['price_numeric'].values
    if len(np.unique(prices)) > 1 and len(prices) > 1:
        # Use log scale for x-axis if max price is much larger than the 75th percentile
        is_skewed = np.percentile(prices, 75) * 5 < prices.max()
        
        axes[0, 0].hist(prices, bins=50, alpha=0.3, color=cat_color, edgecolor='black', density=True, log=False)
        
        if is_skewed:
            # Better visualization for highly skewed price data
            axes[0, 0].set_xscale('log')
            axes[0, 0].set_xlabel('Price (CFA) - Log Scale', fontsize=12)
        else:
            axes[0, 0].set_xlabel('Price (CFA)', fontsize=12)
            
        try:
            kde = stats.gaussian_kde(prices)
            x_range = np.linspace(prices.min(), prices.max(), 200)
            axes[0, 0].plot(x_range, kde(x_range), color='darkred', linewidth=3, label='KDE')
            axes[0, 0].legend()
        except:
             # Fails if prices are too clustered
             pass

        axes[0, 0].set_ylabel('Density', fontsize=12)
    else:
        axes[0, 0].text(0.5, 0.5, 'Not enough variation for distribution plot', ha='center', va='center')
        axes[0, 0].set_title('Price Distribution', fontsize=14, fontweight='bold')
    
    axes[0, 0].set_title('Price Distribution', fontsize=14, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Top 10 Locations
    top_locations = df['adress'].value_counts().head(10)
    if not top_locations.empty:
        axes[0, 1].barh(range(len(top_locations)), top_locations.values, color=cat_color)
        axes[0, 1].set_yticks(range(len(top_locations)))
        axes[0, 1].set_yticklabels(top_locations.index, fontsize=10)
        axes[0, 1].invert_yaxis()
        axes[0, 1].set_title('Top 10 Locations', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Number of Ads', fontsize=12)
        axes[0, 1].grid(True, alpha=0.3, axis='x')
    else:
        axes[0, 1].text(0.5, 0.5, 'No location data', ha='center', va='center')
        axes[0, 1].set_title('Top 10 Locations', fontsize=14, fontweight='bold')
        
    # 3. Price Box Plot
    bp = axes[1, 0].boxplot(df_clean['price_numeric'], vert=True, patch_artist=True,
                             showmeans=True, meanline=True, labels=['Price'])
    for patch in bp['boxes']:
        patch.set_facecolor(cat_color)
        patch.set_alpha(0.7)
    axes[1, 0].set_title('Price Box Plot (Outliers Included)', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Price (CFA)', fontsize=12)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 4. Price by Quartile
    if len(df_clean['price_numeric'].unique()) >= 4:
        try:
            quartiles = pd.qcut(df_clean['price_numeric'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'], duplicates='drop')
            quartile_counts = quartiles.value_counts().sort_index()
            axes[1, 1].bar(range(len(quartile_counts)), quartile_counts.values, color=cat_color, alpha=0.7)
            axes[1, 1].set_xticks(range(len(quartile_counts)))
            axes[1, 1].set_xticklabels(quartile_counts.index, fontsize=10)
            axes[1, 1].set_title('Price by Quartile Count', fontsize=14, fontweight='bold')
            axes[1, 1].set_xlabel('Quartile', fontsize=12)
            axes[1, 1].set_ylabel('Count', fontsize=12)
            axes[1, 1].grid(True, alpha=0.3, axis='y')
        except:
            axes[1, 1].text(0.5, 0.5, 'Not enough unique prices for 4 quartiles', ha='center', va='center')
            axes[1, 1].set_title('Price by Quartile Count', fontsize=14, fontweight='bold')
    else:
        axes[1, 1].text(0.5, 0.5, 'Not enough data (need at least 4 unique prices)', ha='center', va='center')
        axes[1, 1].set_title('Price by Quartile Count', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

# ========================== CSV VIEWER FUNCTIONS ==========================

def load_csv_file(filename):
    """Load CSV file from data folder"""
    try:
        filepath = os.path.join(CSV_FOLDER, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            return df
        else:
            # Handle case where file might not exist locally
            st.error(f"❌ Fichier non trouvé: {filepath}. Veuillez vous assurer qu'il est dans le dossier 'data'.")
            return None
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
        return None

# ========================== INITIALIZE DATABASE ==========================
init_database()

# ========================== SESSION STATE INITIALIZATION ==========================
if 'page' not in st.session_state:
    st.session_state['page'] = "🏠 Welcome"
if 'last_scraped_df' not in st.session_state:
    st.session_state['last_scraped_df'] = pd.DataFrame()
if 'last_scraped_category' not in st.session_state:
    st.session_state['last_scraped_category'] = ""

# ========================== SIDEBAR ==========================
st.sidebar.markdown("## 🧭 Navigation")
page_selection = st.sidebar.radio(
    "Go to",
    ["🏠 Welcome", "📊 Scrape & Analyze", "📁 View CSV Files", "💾 Database Manager"],
    index=["🏠 Welcome", "📊 Scrape & Analyze", "📁 View CSV Files", "💾 Database Manager"].index(st.session_state['page'])
)
st.session_state['page'] = page_selection


# Default sidebar selections for 'Scrape & Analyze' page
selected_category = list(CATEGORIES.keys())[0]
num_pages = 5
option_choice = "Scrape data using BeautifulSoup"


# Dynamic sidebar settings for 'Scrape & Analyze'
if page_selection == "📊 Scrape & Analyze":
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ⚙️ Settings")
    
    selected_category = st.sidebar.selectbox(
        "📂 Category",
        list(CATEGORIES.keys()),
        key="category_select"
    )
    
    num_pages = st.sidebar.number_input(
        "📄 Pages to scrape",
        min_value=1,
        max_value=120,
        value=5,
        step=1
    )
    
    st.sidebar.markdown("---")
    option_choice = st.sidebar.selectbox(
        "🎯 Action",
        [
            "Scrape data using BeautifulSoup",
            "Data Dashboard",
            "Download scraped data",
            "Evaluate the App"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Category:** {selected_category}\n\n**Pages:** {int(num_pages)}")

# Database stats in sidebar for 'Database Manager'
if page_selection == "💾 Database Manager":
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📊 Database Stats")
    db_stats = get_database_stats()
    for cat, count in db_stats.items():
        st.sidebar.metric(CATEGORIES[cat]['icon'] + " " + cat, f"{count} records")

# ========================== MAIN CONTENT ==========================

if page_selection == "🏠 Welcome":
    st.markdown('<h1 class="welcome-title">🛍️ Coinafrique Scraper Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subtitle">Your Professional Tool for Fashion & Footwear Market Analysis in Senegal</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h3 class="feature-title">Smart Scraping</h3>
            <p class="feature-text">Extract data from thousands of fashion listings with advanced web scraping technology.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <h3 class="feature-title">Deep Analytics</h3>
            <p class="feature-text">Visualize price distributions, top locations, and market trends with interactive charts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💾</span>
            <h3 class="feature-title">Easy Export</h3>
            <p class="feature-text">Download your data in CSV format for further analysis in Excel or other tools.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3 class="feature-title">🚀 Ready to Start?</h3>
            <p class="feature-text">Analyze 4 categories: Men's Clothing, Men's Shoes, Children's Clothing, and Children's Shoes</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Change page without rerunning the entire script using Streamlit's internal mechanism
        if st.button("🎬 START SCRAPING NOW", key="start"):
            st.session_state['page'] = "📊 Scrape & Analyze"
            st.rerun()

# --- CSV VIEWER PAGE ---
elif page_selection == "📁 View CSV Files":
    st.markdown('<h1 class="main-title">📁 CSV Files Viewer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">View and download pre-collected data from CSV files</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # File selector
    selected_file = st.selectbox(
        "🗂️ Select a CSV file to view:",
        list(CSV_FILES.keys()),
        key="csv_selector"
    )
    
    filename = CSV_FILES[selected_file]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"📂 LOAD {selected_file}", use_container_width=True):
            with st.spinner(f"Loading CSV file **{filename}**..."):
                df = load_csv_file(filename)
                
                if df is not None:
                    st.session_state[f'csv_data_{selected_file}'] = df
                    st.success(f"✅ Successfully loaded **{len(df):,} rows** from {filename}")
    
    # Display loaded data
    if f'csv_data_{selected_file}' in st.session_state:
        df = st.session_state[f'csv_data_{selected_file}']
        
        st.markdown("---")
        st.markdown(f"## 📊 Data: {selected_file}")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Total Rows", f"{len(df):,}")
        with col2:
            st.metric("📋 Columns", len(df.columns))
        with col3:
            if 'price' in df.columns:
                df['price_numeric'] = df['price'].apply(clean_price)
                avg = df[df['price_numeric'] > 0]['price_numeric'].mean()
                st.metric("💰 Avg Price", f"{avg:,.0f} CFA" if avg > 0 else "N/A")
            else:
                st.metric("💰 Avg Price", "N/A")
        with col4:
            if 'adress' in df.columns:
                st.metric("📍 Locations", df['adress'].nunique())
            else:
                st.metric("📍 Locations", "N/A")
        
        st.markdown("### 📋 Data Preview")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Use io.StringIO for CSV export
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            
            st.download_button(
                f"📥 DOWNLOAD {selected_file}",
                csv_data,
                filename,
                "text/csv",
                use_container_width=True,
                key=f"download_{selected_file}"
            )
            
        # Product preview with images (if img column exists)
        if 'img' in df.columns and not df.empty:
            st.markdown("### 🖼️ Product Preview")
            cols = st.columns(5)
            for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
                with col:
                    img_url = row.img if hasattr(row, 'img') and row.img != "No Image" and row.img and str(row.img).startswith('http') else "https://via.placeholder.com/300x400.png?text=No+Image"
                    st.image(img_url, use_container_width=True)
                    if hasattr(row, 'price'):
                        st.caption(f"💰 {row.price}")
                    if hasattr(row, 'adress'):
                        st.caption(f"📍 {str(row.adress)[:15]}...")

# --- DATABASE MANAGER PAGE ---
elif page_selection == "💾 Database Manager":
    st.markdown('<h1 class="main-title">💾 Database Manager</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Manage scraped data stored in SQLite database</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Database overview
    st.markdown("## 📊 Database Overview")
    db_stats = get_database_stats()
    
    cols = st.columns(4)
    for idx, (cat_name, count) in enumerate(db_stats.items()):
        with cols[idx % 4]:
            st.metric(
                CATEGORIES[cat_name]['icon'] + " " + cat_name,
                f"{count:,} records"
            )
    
    st.markdown("---")
    
    # View data from database
    st.markdown("## 🔍 View Database Records")
    
    selected_db_cat = st.selectbox(
        "Select category to view:",
        list(CATEGORIES.keys()),
        key="db_category_select"
    )
    
    if st.button(f"📊 VIEW {selected_db_cat} DATA", use_container_width=True):
        table_name = CATEGORIES[selected_db_cat]['table']
        df_db = get_from_database(table_name)
        
        if not df_db.empty:
            st.session_state[f'db_data_{selected_db_cat}'] = df_db
            st.success(f"✅ Loaded {len(df_db):,} records from database")
        else:
            st.warning("⚠️ No data found in database for this category")
    
    # Display database data
    if f'db_data_{selected_db_cat}' in st.session_state:
        df_db = st.session_state[f'db_data_{selected_db_cat}']
        
        st.markdown(f"### 📋 Records: {selected_db_cat}")
        st.dataframe(df_db, use_container_width=True, height=400)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            csv_buffer = io.StringIO()
            df_db.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            
            st.download_button(
                "📥 DOWNLOAD FROM DATABASE",
                csv_data,
                f"database_{selected_db_cat.lower().replace(' ', '_')}.csv",
                "text/csv",
                use_container_width=True,
                key=f"download_db_{selected_db_cat}"
            )

# --- SCRAPE & ANALYZE PAGE ---
elif page_selection == "📊 Scrape & Analyze":
    cat_info = CATEGORIES[selected_category]
    
    st.markdown('<h1 class="main-title">📈 Market Data Scraper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Extract and analyze fashion market data from Coinafrique Senegal</p>', unsafe_allow_html=True)
    
    st.markdown(f"**Category:** {selected_category} | **Pages to Scrape:** {num_pages} | **Source:** [View on Coinafrique]({cat_info['url']})")
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # --- ACTION: SCRAPE DATA ---
    if option_choice == "Scrape data using BeautifulSoup":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"{cat_info['icon']} SCRAPE {selected_category.upper()}", use_container_width=True):
                
                status_container = st.empty()
                status_container.info(f"⏳ Starting scraping for **{num_pages} pages** of {selected_category}...")
                
                # Use a progress bar
                progress_container = st.empty()
                st.session_state['progress_bar'] = progress_container.progress(0)
                
                try:
                    df_scraped = scrape_category(cat_info['url'], int(num_pages), cat_info['column'])
                    
                    if not df_scraped.empty:
                        # 1. Store the scraped DF for immediate use (Download)
                        st.session_state['last_scraped_df'] = df_scraped
                        st.session_state['last_scraped_category'] = selected_category
                        
                        # 2. Save to database
                        save_success = save_to_database(df_scraped, cat_info['table'], cat_info['column'])
                        
                        status_container.success(f"✅ Scraping completed! **{len(df_scraped):,} records** found.")
                        
                        if save_success:
                            st.success(f"💾 Data saved to database table: **{cat_info['table']}**")
                        
                        st.markdown("### 📋 Scraped Data Preview (First 50 rows)")
                        st.dataframe(df_scraped.head(50), use_container_width=True, height=300)
                        
                    else:
                        status_container.error("❌ Scraping failed or no data found.")
                        
                except Exception as e:
                    status_container.error(f"❌ An unexpected error occurred during scraping: {e}")
                finally:
                    # Clear the progress bar and status message after completion
                    st.session_state['progress_bar'].empty()
                    del st.session_state['progress_bar']

    # --- ACTION: DATA DASHBOARD ---
    elif option_choice == "Data Dashboard":
        st.markdown(f"## 📊 Data Dashboard: {selected_category}")
        
        # Retrieve all data for analysis
        table_name = cat_info['table']
        df_analysis = get_from_database(table_name)
        
        if not df_analysis.empty:
            st.info(f"Loading analysis for **{len(df_analysis):,} records** from the database.")
            
            # Display Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📦 Total Records", f"{len(df_analysis):,}")
            with col2:
                latest_date = pd.to_datetime(df_analysis['scrape_date']).max().strftime('%Y-%m-%d %H:%M')
                st.metric("⏱️ Last Scrape Date", latest_date)
            
            df_analysis['price_numeric'] = df_analysis['price'].apply(clean_price)
            df_clean = df_analysis[df_analysis['price_numeric'] > 0]
            
            with col3:
                avg = df_clean['price_numeric'].mean()
                st.metric("💰 Avg Price", f"{avg:,.0f} CFA" if avg > 0 else "N/A")
            with col4:
                st.metric("📍 Unique Locations", df_analysis['adress'].nunique())

            st.markdown("---")
            
            # Create and display the charts
            fig = create_charts_for_category(df_analysis, selected_category, cat_info['color'])
            
            if fig:
                st.pyplot(fig) 
            else:
                st.warning("⚠️ Not enough cleaned data (less than 10 records with valid price) to generate charts. Try scraping more pages.")
                
        else:
            st.warning("⚠️ No data found in the database for this category. Please run the **Scrape** action first.")


    # --- ACTION: DOWNLOAD SCRAPED DATA ---
    elif option_choice == "Download scraped data":
        st.markdown("## 📥 Download Data")
        
        # Try to use the last scraped data first
        if not st.session_state['last_scraped_df'].empty and st.session_state['last_scraped_category'] == selected_category:
            df_to_download = st.session_state['last_scraped_df']
            cat_name = st.session_state['last_scraped_category']
            st.info(f"Data available for download (Last Scrape: **{len(df_to_download):,} records** of {cat_name}).")
        else:
            # Fallback: load from database
            table_name = cat_info['table']
            df_to_download = get_from_database(table_name)
            cat_name = selected_category
            st.info(f"Data loaded from Database for download: **{len(df_to_download):,} records** of {cat_name}.")


        if not df_to_download.empty:
            st.dataframe(df_to_download.head(10))
            
            csv_buffer = io.StringIO()
            df_to_download.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode('utf-8')
            
            st.download_button(
                f"📥 DOWNLOAD {cat_name.upper()} CSV",
                csv_data,
                f"scraped_data_{cat_name.lower().replace(' ', '_')}.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.warning("⚠️ No data available to download. Please run the **Scrape** action first.")

    # --- ACTION: EVALUATE THE APP ---
    elif option_choice == "Evaluate the App":
        st.markdown("## ⭐ Evaluate the App")
        st.info("Your feedback is important! Please take a moment to evaluate the tool.")
        
        col_form, col_kobo = st.columns(2)
        with col_form:
            st.markdown(f'<div class="stLinkButton"><a href="{GOOGLE_FORMS_LINK}" target="_blank">📝 GOOGLE FORMS</a></div>', unsafe_allow_html=True)
        with col_kobo:
            st.markdown(f'<div class="stLinkButton" style="background: linear-gradient(135deg, #00897b 0%, #26a69a 100%) !important;"><a href="{KOBOTOOLBOX_LINK}" target="_blank">🗄️ KOBOTOOLBOX</a></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("The links above open external forms to submit your evaluation.")
