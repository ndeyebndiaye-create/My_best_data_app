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
GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScPZoL1rmqr3nJvRqixQlvBphF4Tbj3MrLd9U6WyQjTLzs5hg/viewform?usp=dialog"
KOBOTOOLBOX_LINK = "https://ee.kobotoolbox.org/x/LNbLn5W1"

# Page Configuration
st.set_page_config(
    page_title="Coinafrique Scraper - Multi-Categories",
    page_icon="📊", # Remplacé par un icône neutre
    layout="wide"
)

# Thème de couleur Vert d'Eau (Teal)
TEAL_DARK = "#008080"      # Vert d'Eau foncé / Teal
TEAL_LIGHT = "#00CCCC"     # Cyan / Vert d'Eau clair
BACKGROUND_COLOR = "#F0FFFF" # Azure très clair
CARD_COLOR = "#FFFFFF"     # Blanc pour les cartes

# Custom CSS with modern Teal/Aquamarine design (NO EMOJIS)
st.markdown(f"""
<style>
    /* Global background for the app - Using a clear, professional e-commerce image */
    .stApp {{
        background: linear-gradient(rgba(240, 255, 255, 0.95), rgba(240, 255, 255, 0.95)),
                    url('https://images.unsplash.com/photo-1576759795078-7d8b5c9b9804?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); /* Stockage/Logistique clair */
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #333333;
    }}

    /* Sidebar with solid light background */
    [data-testid="stSidebar"] {{
        background-color: {BACKGROUND_COLOR};
        box-shadow: 4px 0 15px rgba(0,0,0,0.05);
        color: {TEAL_DARK};
    }}
    
    /* Sidebar titles/text */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {{
        color: {TEAL_DARK} !important;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    
    /* Main area with clean card effect */
    .main .block-container {{
        background-color: {CARD_COLOR};
        border-radius: 15px;
        padding: 2.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 30px rgba(0, 128, 128, 0.1),
                    0 0 0 1px rgba(0, 128, 128, 0.1);
        border: 1px solid rgba(0, 128, 128, 0.1);
    }}
    
    /* Specific background for the Welcome Page container */
    #welcome-page-container {{
        background: {CARD_COLOR}; 
        border-radius: 15px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 10px 40px rgba(0, 128, 128, 0.2);
        border: 1px solid rgba(0, 128, 128, 0.2);
    }}

    /* Main title (Teal gradient) */
    .welcome-title, .main-title {{
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, {TEAL_DARK} 0%, {TEAL_LIGHT} 100%); 
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 6px rgba(0, 128, 128, 0.2);
        letter-spacing: 2px;
    }}

    .subtitle {{
        text-align: center;
        color: #555555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
        font-weight: 400;
    }}
    
    /* Primary Button (Scraping/Main Action) - Teal */
    .stButton>button {{
        background: linear-gradient(135deg, {TEAL_DARK} 0%, {TEAL_LIGHT} 100%) !important;
        color: white !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 15px 30px;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 128, 128, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 128, 128, 0.6);
        background: linear-gradient(135deg, #00A3A3 0%, #00B3B3 100%) !important;
    }}

    /* Evaluation button 1 (Accent Green) */
    #button-evaluate-google > button {{
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 8px;
        padding: 15px 30px;
        box-shadow: 0 4px 15px rgba(76, 175, 79, 0.4);
    }}
    #button-evaluate-google > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(76, 175, 79, 0.6);
    }}
    
    /* Evaluation button 2 (Accent Blue) */
    #button-evaluate-kobo > button {{
        background: linear-gradient(135deg, #2196F3 0%, #4DD0E1 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 8px;
        padding: 15px 30px;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
    }}
    #button-evaluate-kobo > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(33, 150, 243, 0.6);
    }}
    
    /* Download button (Teal Accent) */
    .stDownloadButton > button {{
        background: {TEAL_LIGHT} !important;
        color: white !important;
        border-radius: 8px;
        padding: 12px 25px;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(0, 204, 204, 0.4);
        border: none;
        text-transform: uppercase;
    }}
    
    .stDownloadButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 204, 204, 0.6);
        background: {TEAL_DARK} !important;
    }}

    /* Metrics with color */
    [data-testid="stMetricValue"] {{
        color: {TEAL_DARK};
        font-weight: 800;
    }}
    
    /* Progress bar */
    .stProgress > div > div {{
        background-color: {TEAL_LIGHT};
    }}
    
    /* Info boxes */
    .stAlert {{
        border-radius: 8px;
        border-left: 5px solid {TEAL_DARK};
        background-color: #F8FFFF; /* Lightest tone */
    }}
    
    /* Separator line */
    hr {{
        border: none;
        height: 1px;
        background-color: rgba(0, 128, 128, 0.2);
        margin: 1.5rem 0;
    }}
    
    /* Images */
    img {{
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    
    img:hover {{
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(0, 128, 128, 0.3);
    }}

</style>
""", unsafe_allow_html=True)

# Category Configuration (EMOJI REMOVED)
CATEGORIES = {
    "Men's Clothing": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "icon": "👔", # Maintenu dans l'objet pour les fonctions Python, mais inutilisé dans le frontend
        "column": "type_habits",
        "color": "#008080" # Teal Dark
    },
    "Men's Shoes": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "icon": "👞",
        "column": "type_shoes",
        "color": "#009999" # Teal Medium
    },
    "Children's Clothing": {
        "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "icon": "👶",
        "column": "type_clothes",
        "color": "#00B3B3" # Teal Light
    },
    "Children's Shoes": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "icon": "👟",
        "column": "type_shoes",
        "color": "#00CCCC" # Cyan
    }
}

# --- Scraping and Chart Functions (No Change) ---
# Maintained as in the original corrected code
def scrape_category(url, num_pages, column_name):
    """Scrape a specific category"""
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
    """Clean and convert prices to float"""
    try:
        cleaned = str(price_str).replace(' ', '').replace(',', '').replace('.', '')
        return float(cleaned) if cleaned.isdigit() else 0
    except:
        return 0

def create_charts_for_category(df, cat_name, cat_color):
    """Create charts for a category using matplotlib"""
    
    # Clean prices
    df['price_numeric'] = df['price'].apply(clean_price)
    df_clean = df[df['price_numeric'] > 0]
    
    if len(df_clean) < 10:
        return None
    
    # Set style
    sns.set_style("whitegrid")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Data Analysis - {cat_name}', fontsize=20, fontweight='bold', y=1.0) # Adjusted y-position
    
    # 1. KDE Plot
    prices = df_clean['price_numeric'].values
    if len(np.unique(prices)) > 1 and len(prices) > 1:
        axes[0, 0].hist(prices, bins=50, alpha=0.3, color=cat_color, edgecolor='black', density=True)
        kde = stats.gaussian_kde(prices)
        x_range = np.linspace(prices.min(), prices.max(), 200)
        axes[0, 0].plot(x_range, kde(x_range),
                        color=cat_color, linewidth=3, label='KDE')
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
    else:
        axes[0, 1].text(0.5, 0.5, 'No Location Data', ha='center', va='center')
    
    # 3. Box Plot
    bp = axes[1, 0].boxplot(df_clean['price_numeric'], vert=True, patch_artist=True,
                            showmeans=True, meanline=True, labels=['Price'])
    for patch in bp['boxes']:
        patch.set_facecolor(cat_color)
        patch.set_alpha(0.7)
    axes[1, 0].set_title('Price Box Plot (Outliers Included)', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Price (CFA)', fontsize=12)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 4. Quartile Distribution
    if len(df_clean['price_numeric'].unique()) >= 4 and len(df_clean) >= 4:
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
        except ValueError as e:
            axes[1, 1].text(0.5, 0.5, f'Quartile error: {e}', ha='center', va='center', fontsize=10)
    else:
        axes[1, 1].text(0.5, 0.5, 'Not enough unique prices for Quartile analysis', ha='center', va='center')
    
    plt.tight_layout()
    return fig

# --- SIDEBAR ---
# Main page selection (NO EMOJI)
st.sidebar.markdown("## Navigation")
page_selection = st.sidebar.radio(
    "Go to",
    ["1. Welcome & Guide", "2. Scrape & Analyze"],
    index=0
)

if page_selection == "2. Scrape & Analyze":
    st.sidebar.markdown("---")
    st.sidebar.markdown("## User Input Features")
    
    st.sidebar.markdown("### Category Selection")
    selected_category = st.sidebar.selectbox(
        "Choose a category",
        list(CATEGORIES.keys()),
        key="category_select"
    )
    
    st.sidebar.markdown("### Pages Indexes")
    
    num_pages = st.sidebar.number_input(
        "Number of pages to scrape (Max 120)",
        min_value=1,
        max_value=120, 
        value=5,
        step=1,
        key="pages_number_input"
    )
    
    num_pages = int(num_pages)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Options")
    
    option_choice = st.sidebar.selectbox(
        "Choose an option",
        [
            "Scrape data using BeautifulSoup",
            "Download scraped data",
            "Data Dashboard",
            "Evaluate the App"
        ],
        key="option_select"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Info")
    st.sidebar.info(f"**Category:** {selected_category}\n\n**Pages:** {num_pages}")
else:
    selected_category = list(CATEGORIES.keys())[0]
    num_pages = 5
    option_choice = "Scrape data using BeautifulSoup"
# --- END SIDEBAR ---

# --- MAIN CONTENT AREA ---

if page_selection == "1. Welcome & Guide":
    
    with st.container(border=False):
        st.markdown('<div id="welcome-page-container">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="welcome-title">Welcome to the Coinafrique Scraper</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Your dedicated tool for **online sales market analysis** on Coinafrique Senegal. Prepare your market studies with precision and clarity.</p>', unsafe_allow_html=True)

        # Updated image for sales / marketplace
        st.image(
            "https://images.unsplash.com/photo-1601004928014-998875a6c8e3?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            caption="Clear view of market and sales context.",
            use_column_width=True
        )
        
        st.markdown("---")
        
        st.markdown("## How to Use the App")
        st.markdown("""
        1.  **Change Page**: In the sidebar on the left, select **"2. Scrape & Analyze"**.
        2.  **Select Category**: Choose the product category (men's clothing/shoes, children's clothing/shoes) you want to analyze.
        3.  **Define Number of Pages**: Enter the number of pages to scrape. Higher numbers increase processing time (max. 120 pages).
        4.  **Start Scraping**: Click the main button to collect data.
        5.  **Analyze**: Use the **"Data Dashboard"** or **"Download scraped data"** options to visualize or export the results.
        """)
        st.markdown("---")
        st.info("**Ready to start?** Go to the **'2. Scrape & Analyze'** tab to launch your first market study.")
        
        st.markdown('</div>', unsafe_allow_html=True)

else: # Scraping and Analysis Page
    
    cat_info = CATEGORIES[selected_category]
    st.markdown('<h1 class="main-title">Coinafrique Multi-Category Scraper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Scrape data from 4 categories on coinafrique.com: men\'s clothing, men\'s shoes, children\'s clothing and children\'s shoes.</p>', unsafe_allow_html=True)
    st.markdown("**Python libraries:** pandas, streamlit, requests, bs4, scipy, matplotlib, seaborn")

    st.markdown(f"**Data source:** [{selected_category}]({cat_info['url']})") 

    st.markdown("<br>", unsafe_allow_html=True)

    if option_choice == "Scrape data using BeautifulSoup":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # NO EMOJI
            if st.button(f"Scrape Data for {selected_category}"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                start_time = time.time()
                status_text.markdown(f"**Scraping {selected_category} in progress...**")
                
                df = scrape_category(
                    cat_info['url'],
                    num_pages,
                    cat_info['column']
                )
                
                elapsed_time = time.time() - start_time
                progress_bar.progress(1.0)
                status_text.markdown(f"**Scraping completed in {elapsed_time:.2f} seconds.**")
                
                if not df.empty:
                    st.session_state[f'scraped_data_{selected_category}'] = df
                    st.session_state['current_category'] = selected_category
                    st.session_state['num_pages'] = num_pages
                    st.session_state['elapsed_time'] = elapsed_time
                    st.success(f"Successfully scraped **{len(df)}** rows of data.")
                else:
                    st.error("No data retrieved. The page structure may have changed or the number of pages is too low.")
        
        if 'current_category' in st.session_state and st.session_state['current_category'] == selected_category:
            cat_name = st.session_state['current_category']
            df = st.session_state[f'scraped_data_{cat_name}']
            num_pages_scraped = st.session_state.get('num_pages', 0)
            
            st.markdown("---")
            st.markdown(f"## Results: {cat_name}")
            st.markdown(f"**Data dimension:** {len(df)} rows and {len(df.columns)} columns.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.dataframe(df, use_container_width=True, height=400)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # NO EMOJI
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f"coinafrique_{cat_name.lower().replace(' ', '_')}_{num_pages_scraped}pages.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### Preview of Items")
            cols = st.columns(5)
            if 'img' in df.columns and not df.empty:
                for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
                    with col:
                        img_url = row.img if row.img != "No Image" else "https://via.placeholder.com/300x400.png?text=No+Image"
                        st.image(img_url, use_container_width=True)
                        st.caption(f"Price: {row.price} CFA")
                        st.caption(f"Location: {row.adress[:15]}...")
            else:
                st.info("No images to display or 'img' column missing.")
        

    elif option_choice == "Download scraped data":
        available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
        
        if available_data:
            st.success(f"{len(available_data)} category(ies) available for download.")
            
            for cat_name in available_data:
                df = st.session_state[f'scraped_data_{cat_name}']
                csv = df.to_csv(index=False).encode('utf-8')
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label=f"Download {cat_name} ({len(df)} rows)",
                        data=csv,
                        file_name=f"coinafrique_{cat_name.lower().replace(' ', '_')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key=f"download_{cat_name}"
                    )
        else:
            st.warning("No scraped data available. Please scrape data first.")
            
    elif option_choice == "Data Dashboard":
        available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
        
        if available_data:
            st.markdown("## Data Dashboard")
            
            for cat_name in available_data:
                df = st.session_state[f'scraped_data_{cat_name}']
                cat_info_dash = CATEGORIES[cat_name]
                
                st.markdown(f"### {cat_name}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Ads", len(df))
                with col2:
                    st.metric("Unique Locations", df['adress'].nunique())
                with col3:
                    try:
                        df['price_numeric'] = df['price'].apply(clean_price)
                        avg_price = df[df['price_numeric'] > 0]['price_numeric'].mean()
                        st.metric("Average Price", f"{avg_price:,.0f} CFA")
                    except:
                        st.metric("Average Price", "N/A")
                with col4:
                    try:
                        median_price = df[df['price_numeric'] > 0]['price_numeric'].median()
                        st.metric("Median Price", f"{median_price:,.0f} CFA")
                    except:
                        st.metric("Median Price", "N/A")
                
                fig = create_charts_for_category(df, cat_name, cat_info_dash['color'])
                if fig:
                    st.pyplot(fig)
                else:
                    st.warning("Not enough data points to generate meaningful charts for this category (needs at least 10 entries with unique prices).")
                
                st.markdown("---")
        else:
            st.warning("No data available. Please scrape data first.")
            
    elif option_choice == "Evaluate the App":
        st.markdown("## App Evaluation")
        st.markdown("Please take a moment to evaluate our application. Your feedback is valuable for its improvement.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div id="button-evaluate-google">', unsafe_allow_html=True)
            st.link_button(
                label="Evaluate on Google Forms",
                url=GOOGLE_FORMS_LINK,
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div id="button-evaluate-kobo">', unsafe_allow_html=True)
            st.link_button(
                label="Evaluate on KoboToolbox",
                url=KOBOTOOLBOX_LINK,
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
