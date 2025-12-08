import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration variables
GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScPZoL1rmqr3nJvRqixLlvBphF4Tbj3MrLd9U6WyQjTLzs5hg/viewform?usp=dialog"
KOBOTOOLBOX_LINK = "https://ee.kobotoolbox.org/x/LNbLn5W1"

# Page Configuration
st.set_page_config(
    page_title="Coinafrique Scraper Pro",
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS with Fashion Theme (BACKGROUND FIX APPLIED HERE)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* WELCOME PAGE - Shopping Background (INCHANGÉ) */
    .welcome-container {
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)),
                    url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1920&q=90');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        border-radius: 25px;
        padding: 4rem 2rem;
        margin: -1rem -2rem;
        min-height: 85vh;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    /* ALL ACTION PAGES - NOUVEAU STYLE AVEC FOND ET OVERLAY */
    .scraping-page, .download-page, .dashboard-page, .evaluation-page {
        /* Copie de la structure du Welcome Container */
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)),
                    url('https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=1920&q=90'); /* Image Ventes/Sacs */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        border-radius: 20px; /* Légèrement plus petit pour l'action */
        padding: 2rem;
        margin: -1rem -2rem;
        min-height: 100vh;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(21, 101, 192, 0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .welcome-title {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(21, 101, 192, 0.2);
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    .welcome-subtitle {
        text-align: center;
        color: #546e7a;
        font-size: 1.4rem;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(21, 101, 192, 0.1);
        position: relative;
        z-index: 1;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(21, 101, 192, 0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1565c0;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #546e7a;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* MAIN APP BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* SIDEBAR - Elegant Navy Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #0d47a1 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* MAIN CONTENT CARD - Rendre la carte plus transparente pour voir le fond */
    .main .block-container {
        /* Opacité à 0.85 pour laisser l'image de fond transparaître */
        background: rgba(255, 255, 255, 0.85); 
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
    }
    
    /* TITLES */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 50%, #42a5f5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #546e7a;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.7;
    }
    
    /* BUTTONS - Primary (Scrape) */
    .stButton>button {
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
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(21, 101, 192, 0.6);
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    
    /* START BUTTON (Welcome Page) */
    .start-button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%) !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.5);
    }
    
    .start-button:hover {
        background: linear-gradient(135deg, #388e3c 0%, #4caf50 100%) !important;
        box-shadow: 0 15px 40px rgba(76, 175, 80, 0.7);
    }
    
    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ff9800 0%, #ffa726 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 15px 30px;
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
        border: none;
        text-transform: uppercase;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 152, 0, 0.6);
    }
    
    /* METRICS */
    [data-testid="stMetricValue"] {
        color: #1565c0;
        font-weight: 800;
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #546e7a;
        font-weight: 600;
    }
    
    /* ALERTS */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #1976d2;
        background: rgba(25, 118, 210, 0.05);
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1565c0 0%, #42a5f5 100%);
        border-radius: 10px;
    }
    
    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* IMAGES */
    img {
        border-radius: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    img:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 35px rgba(21, 101, 192, 0.3);
    }
    
    /* SEPARATOR */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #1976d2 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* LINK BUTTONS (Evaluation) */
    .stLinkButton > a {
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
    }
    
    .stLinkButton > a:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 137, 123, 0.6);
    }
    
    /* ANIMATIONS */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: fadeInUp 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ... (Le reste du code Python est inchangé) ...
# Functions
def scrape_category(url, num_pages, column_name):
    data = []
    for i in range(num_pages):
        try:
            time.sleep(0.5)
            page_url = f'{url}?page={i}'
            res = get(page_url)
            soup = bs(res.content, 'html.parser')
            containers = soup.find_all('div', class_='col s6 m4 l3')
            for container in containers:
                try:
                    item_type = container.find('p', 'ad__card-description').text.strip()
                    price = container.find('p', class_='ad__card-price').text.replace('CFA', '').strip()
                    adress = container.find('p', class_='ad__card-location').text.strip()
                    img_tag = container.find('img', class_='ad__card-img')
                    img = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "No Image"
                    dic = {
                        column_name: item_type,
                        'price': price,
                        'adress': adress,
                        'img': img
                    }
                    data.append(dic)
                except:
                    pass
        except:
            pass
    return pd.DataFrame(data)

def clean_price(price_str):
    try:
        cleaned = str(price_str).replace(' ', '').replace(',', '').replace('.', '')
        return float(cleaned) if cleaned.isdigit() else 0
    except:
        return 0

def create_charts_for_category(df, cat_name, cat_color):
    df['price_numeric'] = df['price'].apply(clean_price)
    df_clean = df[df['price_numeric'] > 0]
    if len(df_clean) < 10:
        return None
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Data Analysis - {cat_name}', fontsize=20, fontweight='bold', y=1.0)
    
    # 1. KDE Plot
    prices = df_clean['price_numeric'].values
    if len(np.unique(prices)) > 1 and len(prices) > 1:
        axes[0, 0].hist(prices, bins=50, alpha=0.3, color=cat_color, edgecolor='black', density=True)
        kde = stats.gaussian_kde(prices)
        x_range = np.linspace(prices.min(), prices.max(), 200)
        axes[0, 0].plot(x_range, kde(x_range), color=cat_color, linewidth=3, label='KDE')
        axes[0, 0].set_ylabel('Density', fontsize=12)
    else:
        axes[0, 0].hist(prices, bins=1, color=cat_color, edgecolor='black')
        axes[0, 0].set_ylabel('Frequency', fontsize=12)
    axes[0, 0].set_title('Price Distribution (Histogram & KDE)', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Price (CFA)', fontsize=12)
    axes[0, 0].legend()
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
    
    # 3. Box Plot
    bp = axes[1, 0].boxplot(df_clean['price_numeric'], vert=True, patch_artist=True,
                            showmeans=True, meanline=True, labels=['Price'])
    for patch in bp['boxes']:
        patch.set_facecolor(cat_color)
        patch.set_alpha(0.7)
    axes[1, 0].set_title('Price Box Plot', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Price (CFA)', fontsize=12)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 4. Quartile Distribution
    if len(df_clean['price_numeric'].unique()) >= 4:
        try:
            quartiles = pd.qcut(df_clean['price_numeric'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'], duplicates='drop')
            quartile_counts = quartiles.value_counts().sort_index()
            axes[1, 1].bar(range(len(quartile_counts)), quartile_counts.values, color=cat_color, alpha=0.7)
            axes[1, 1].set_xticks(range(len(quartile_counts)))
            axes[1, 1].set_xticklabels(quartile_counts.index, fontsize=10)
            axes[1, 1].set_title('Price Distribution by Quartile', fontsize=14, fontweight='bold')
            axes[1, 1].set_xlabel('Quartile', fontsize=12)
            axes[1, 1].set_ylabel('Count', fontsize=12)
            axes[1, 1].grid(True, alpha=0.3, axis='y')
        except Exception as e:
            axes[1, 1].text(0.5, 0.5, f'Quartile error: {e}', ha='center', va='center')
    else:
        axes[1, 1].text(0.5, 0.5, 'Not enough unique data points for quartiles', ha='center', va='center')
    
    plt.tight_layout()
    return fig

# SIDEBAR
st.sidebar.markdown("## 🧭 Navigation")
page_selection = st.sidebar.radio(
    "Go to",
    ["🏠 Welcome", "📊 Scrape & Analyze"],
    index=0
)

# Initialize default values
selected_category = list(CATEGORIES.keys())[0]
num_pages = 5
option_choice = "Scrape data using BeautifulSoup"

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
            "Download scraped data",
            "Data Dashboard",
            "Evaluate the App"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Category:** {selected_category}\n\n**Pages:** {int(num_pages)}")
    
    # Update page_selection based on st.session_state if button was clicked on welcome page
    if 'page' in st.session_state and st.session_state.page == "📊 Scrape & Analyze":
        page_selection = "📊 Scrape & Analyze"

# MAIN CONTENT
if page_selection == "🏠 Welcome":
    st.markdown('<div class="welcome-container animated">', unsafe_allow_html=True)
    
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
        
        # Use session state to handle page transition if button is clicked
        if st.button("🎬 START SCRAPING NOW", key="start", help="Click to begin"):
            st.session_state['page'] = "📊 Scrape & Analyze"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    cat_info = CATEGORIES[selected_category]
    
    # Determine which CSS class to use based on action
    if option_choice == "Scrape data using BeautifulSoup":
        page_class = "scraping-page"
    elif option_choice == "Download scraped data":
        page_class = "download-page"
    elif option_choice == "Data Dashboard":
        page_class = "dashboard-page"
    elif option_choice == "Evaluate the App":
        page_class = "evaluation-page"
    else:
        page_class = "scraping-page"
    
    st.markdown(f'<div class="{page_class}">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title animated">📈 Market Data Scraper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Extract and analyze fashion market data from Coinafrique Senegal</p>', unsafe_allow_html=True)
    
    st.markdown(f"**Category:** {selected_category} | **Source:** [View on Coinafrique]({cat_info['url']})")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if option_choice == "Scrape data using BeautifulSoup":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"{cat_info['icon']} SCRAPE {selected_category.upper()}", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                start_time = time.time()
                status_text.markdown(f"**⏳ Scraping {selected_category}...**")
                
                df = scrape_category(cat_info['url'], int(num_pages), cat_info['column'])
                
                elapsed_time = time.time() - start_time
                progress_bar.progress(1.0)
                status_text.markdown(f"**✅ Completed in {elapsed_time:.2f}s | {len(df)} items found**")
                
                if not df.empty:
                    st.session_state[f'scraped_data_{selected_category}'] = df
                    st.session_state['current_category'] = selected_category
                    st.success(f"🎉 Successfully scraped **{len(df)} products**!")
                else:
                    st.error("❌ No data found. Try increasing the number of pages.")
        
        if 'current_category' in st.session_state and st.session_state['current_category'] == selected_category:
            df = st.session_state[f'scraped_data_{selected_category}']
            
            st.markdown("---")
            st.markdown(f"## 📦 Results: {selected_category}")
            st.markdown(f"**{len(df)} rows** × **{len(df.columns)} columns**")
            
            st.dataframe(df, use_container_width=True, height=400)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 DOWNLOAD CSV",
                    csv,
                    f"coinafrique_{selected_category.lower().replace(' ', '_')}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            st.markdown("### 🖼️ Product Preview")
            cols = st.columns(5)
            for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
                with col:
                    img_url = row.img if row.img != "No Image" else "https://via.placeholder.com/300x400.png?text=No+Image"
                    st.image(img_url, use_container_width=True)
                    st.caption(f"💰 {row.price} CFA")
                    st.caption(f"📍 {row.adress[:15]}...")
    
    elif option_choice == "Download scraped data":
        available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
        
        if available_data:
            st.success(f"✅ {len(available_data)} dataset(s) available")
            
            for cat_name in available_data:
                df = st.session_state[f'scraped_data_{cat_name}']
                csv = df.to_csv(index=False).encode('utf-8')
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        f"📥 {cat_name} ({len(df)} rows)",
                        csv,
                        f"coinafrique_{cat_name.lower().replace(' ', '_')}.csv",
                        "text/csv",
                        use_container_width=True,
                        key=f"dl_{cat_name}"
                    )
        else:
            st.warning("⚠️ No data available. Please scrape first.")
    
    elif option_choice == "Data Dashboard":
        available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
        
        if available_data:
            st.markdown("## 📊 Analytics Dashboard")
            
            for cat_name in available_data:
                df = st.session_state[f'scraped_data_{cat_name}']
                
                st.markdown(f"### {CATEGORIES[cat_name]['icon']} {cat_name}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📦 Total Ads", len(df))
                with col2:
                    st.metric("📍 Locations", df['adress'].nunique())
                with col3:
                    df['price_numeric'] = df['price'].apply(clean_price)
                    avg = df[df['price_numeric'] > 0]['price_numeric'].mean()
                    st.metric("💰 Avg Price", f"{avg:,.0f} CFA" if avg > 0 else "N/A")
                with col4:
                    med = df[df['price_numeric'] > 0]['price_numeric'].median()
                    st.metric("📊 Median", f"{med:,.0f} CFA" if med > 0 else "N/A")
                
                fig = create_charts_for_category(df, cat_name, CATEGORIES[cat_name]['color'])
                if fig:
                    st.pyplot(fig)
                else:
                    st.warning("⚠️ Need at least 10 items for charts")
                
                st.markdown("---")
        else:
            st.warning("⚠️ No data available. Please scrape first.")
    
    elif option_choice == "Evaluate the App":
        st.markdown("## ⭐ Help Us Improve")
        st.markdown("Your feedback matters! Choose your preferred platform:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📝 Google Forms", GOOGLE_FORMS_LINK, use_container_width=True)
        with col2:
            st.link_button("📋 KoboToolbox", KOBOTOOLBOX_LINK, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
