import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time
import numpy as np
from scipy import stats
# Configuration de la page
st.set_page_config(
    page_title="Coinafrique Scraper - Multi-Categories",
    page_icon="👔",
    layout="wide"
)
# CSS personnalisé avec design élégant rose/doré
st.markdown("""
<style>
    /* Fond principal avec image de boutique de luxe */
    .stApp {
        background: linear-gradient(rgba(255, 245, 250, 0.92), rgba(255, 240, 245, 0.92)),
                    url('https://images.unsplash.com/photo-1558769132-cb1aea1f19e0?w=1400&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
   
    /* Sidebar avec dégradé rose/doré élégant */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,
                    rgba(255, 182, 193, 0.95) 0%,
                    rgba(255, 218, 185, 0.95) 50%,
                    rgba(255, 228, 196, 0.95) 100%),
                    url('https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80');
        background-size: cover;
        background-position: center;
        box-shadow: 4px 0 15px rgba(0,0,0,0.1);
    }
   
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
   
    /* Titres sidebar avec effet doré */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #8B4513 !important;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(255, 215, 0, 0.3);
        letter-spacing: 1px;
    }
   
    /* Labels sidebar */
    [data-testid="stSidebar"] label {
        color: #8B4513 !important;
        font-weight: 700;
        font-size: 1rem;
    }
   
    /* Select boxes sidebar avec effet glassmorphism */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(255, 182, 193, 0.4);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
   
    /* Zone principale avec effet carte premium */
    .main .block-container {
        background: linear-gradient(135deg,
                    rgba(255, 255, 255, 0.98) 0%,
                    rgba(255, 250, 250, 0.98) 100%);
        border-radius: 25px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 15px 50px rgba(255, 105, 180, 0.2),
                    0 0 0 1px rgba(255, 182, 193, 0.3);
        border: 2px solid rgba(255, 182, 193, 0.2);
    }
   
    /* Titre principal avec dégradé rose-doré */
    .main-title {
        font-size: 3.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 30%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(255, 105, 180, 0.3);
        letter-spacing: 2px;
    }
   
    .subtitle {
        text-align: center;
        color: #696969;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        line-height: 1.7;
        font-weight: 500;
    }
   
    /* Boutons avec dégradé rose vif */
    .stButton>button {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 50%, #FFC0CB 100%) !important;
        color: white !important;
        font-weight: 800;
        border: none;
        border-radius: 15px;
        padding: 18px 35px;
        font-size: 1.15rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        box-shadow: 0 8px 25px rgba(255, 20, 147, 0.35),
                    inset 0 -2px 5px rgba(0,0,0,0.1);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
   
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(255, 20, 147, 0.5),
                    inset 0 -2px 5px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 50%, #C71585 100%) !important;
    }

    /* Bouton d'évaluation personnalisé */
    #button-evaluate > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%) !important;
        color: #8B4513 !important;
        font-weight: 800;
        border: none;
        border-radius: 15px;
        padding: 18px 35px;
        font-size: 1.15rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.35),
                    inset 0 -2px 5px rgba(0,0,0,0.1);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    #button-evaluate > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(255, 215, 0, 0.5),
                    inset 0 -2px 5px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 50%, #FFDF00 100%) !important;
    }

   
    /* Tableau avec effet premium */
    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(255, 105, 180, 0.2);
        border: 2px solid rgba(255, 182, 193, 0.3);
    }
   
    /* Info boxes avec glassmorphism */
    .stAlert {
        border-radius: 15px;
        background: linear-gradient(135deg,
                    rgba(255, 255, 255, 0.95),
                    rgba(255, 245, 250, 0.95));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 4px 20px rgba(255, 105, 180, 0.15);
    }
   
    /* Progress bar avec dégradé rose */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FF1493 0%, #FF69B4 50%, #FFB6C1 100%);
        box-shadow: 0 2px 10px rgba(255, 20, 147, 0.4);
    }
   
    /* Download button doré */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%) !important;
        color: #8B4513 !important;
        border-radius: 15px;
        padding: 14px 28px;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
        border: 2px solid rgba(255, 215, 0, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
   
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.6);
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 50%, #FFDF00 100%) !important;
    }
   
    /* Metrics avec effet carte */
    [data-testid="stMetricValue"] {
        color: #FF1493;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(255, 105, 180, 0.2);
    }
   
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(255, 105, 180, 0.5) 50%,
                    transparent 100%);
        margin: 2rem 0;
    }
   
    img {
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
   
    img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.3);
    }
   
    /* Style pour les iframes */
    iframe {
        border-radius: 15px;
        border: 2px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 8px 30px rgba(255, 105, 180, 0.2);
    }
</style>
""", unsafe_allow_html=True)
# Configuration des catégories
CATEGORIES = {
    "Men's Clothing 👔": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "icon": "👔",
        "column": "type_habits",
        "color": "#667eea"
    },
    "Men's Shoes 👞": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "icon": "👞",
        "column": "type_shoes",
        "color": "#764ba2"
    },
    "Children's Clothing 👶": {
        "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "icon": "👶",
        "column": "type_clothes",
        "color": "#f093fb"
    },
    "Children's Shoes 👟": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "icon": "👟",
        "column": "type_shoes",
        "color": "#4facfe"
    }
}

GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScPZoL1rmqr3nJvRqixQlvBphF4Tbj3MrLd9U6WyQjTLzs5hg/viewform?usp=sf_link"

# Fonction de scraping
def scrape_category(url, num_pages, column_name):
    """Scrape a specific category"""
    data = []
   
    for i in range(num_pages):
        try:
            # Ajout d'une pause pour éviter le blocage par le site
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
                    # Assurez-vous que l'élément img existe avant d'accéder à 'src'
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
        # Gère les cas où la conversion en float échouerait après le nettoyage initial
        return float(cleaned) if cleaned.isdigit() else 0
    except:
        return 0

def create_charts_for_category(df, cat_name, cat_color):
    """Create charts for a category using matplotlib"""
   
    # Clean prices
    df['price_numeric'] = df['price'].apply(clean_price)
    df_clean = df[df['price_numeric'] > 0]
   
    if len(df_clean) < 10: # Nécessite un minimum de données pour des graphiques pertinents
        st.warning(f"Not enough data points ({len(df_clean)}) for {cat_name} to generate meaningful charts.")
        return None
   
    import matplotlib.pyplot as plt
    import seaborn as sns
   
    # Set style
    sns.set_style("whitegrid")
   
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Data Analysis - {cat_name}', fontsize=20, fontweight='bold', y=0.995)
   
    # 1. KDE Plot
    prices = df_clean['price_numeric'].values
    # Ajout d'une vérification de la variance pour KDE
    if len(np.unique(prices)) > 1:
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
        # Inversement pour avoir le plus grand en haut
        axes[0, 1].barh(range(len(top_locations)), top_locations.values, color=cat_color)
        axes[0, 1].set_yticks(range(len(top_locations)))
        axes[0, 1].set_yticklabels(top_locations.index, fontsize=10)
        axes[0, 1].invert_yaxis() # Met le plus grand en haut
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
    # S'assurer que le nombre de bins est suffisant et que les quartiles peuvent être calculés
    if len(df_clean['price_numeric'].unique()) >= 4:
        quartiles = pd.qcut(df_clean['price_numeric'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'], duplicates='drop')
        quartile_counts = quartiles.value_counts().sort_index()
        axes[1, 1].bar(range(len(quartile_counts)), quartile_counts.values, color=cat_color, alpha=0.7)
        axes[1, 1].set_xticks(range(len(quartile_counts)))
        axes[1, 1].set_xticklabels(quartile_counts.index, fontsize=10)
        axes[1, 1].set_title('Price Distribution by Quartile', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Quartile', fontsize=12)
        axes[1, 1].set_ylabel('Count', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
    else:
        axes[1, 1].text(0.5, 0.5, 'Not enough unique prices for Quartile analysis', ha='center', va='center')
   
    plt.tight_layout()
    return fig

# Sidebar
with st.sidebar:
    st.markdown("## 🛍️ User Input Features")
    st.markdown("---")
   
    st.markdown("### Category")
    selected_category = st.selectbox(
        "Choose a category",
        list(CATEGORIES.keys()),
        key="category_select"
    )
   
    st.markdown("### Pages Indexes")
    num_pages = st.selectbox(
        "Number of pages",
        options=[5, 10, 15, 20, 25, 30, 50, 75, 100, 120],
        index=0,
        key="pages_select"
    )
   
    st.markdown("---")
    st.markdown("### Options")
   
    option_choice = st.selectbox(
        "Choose an option",
        [
            "Scrape data using BeautifulSoup",
            "Download scraped data",
            "Dashboard of the data",
            "Evaluate the App"
        ],
        key="option_select"
    )
   
    st.markdown("---")
    st.markdown("### 📊 Info")
    st.info(f"**Category:** {selected_category}\n\n**Pages:** {num_pages}")


# Zone principale
cat_info = CATEGORIES[selected_category] # Récupère les infos de la catégorie sélectionnée
st.markdown('<h1 class="main-title">🛍️ Coinafrique Multi-Category Scraper</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Scrape data from 4 categories: men\'s clothing, men\'s shoes, children\'s clothing and children\'s shoes from coinafrique.com</p>', unsafe_allow_html=True)
st.markdown("**Python libraries:** base64, pandas, streamlit, requests, bs4, scipy, matplotlib, seaborn")

# MODIFICATION 1 : Affichage du lien de la catégorie sélectionnée
st.markdown(f"**Data source:** [{selected_category}]({cat_info['url']})") 

st.markdown("<br>", unsafe_allow_html=True)

# Logique selon l'option choisie
if option_choice == "Scrape data using BeautifulSoup":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"{cat_info['icon']} Scrape {selected_category}"):
            progress_bar = st.progress(0)
            status_text = st.empty()
           
            start_time = time.time()
            status_text.markdown(f"**⏳ Scraping {selected_category} in progress...**")
           
            df = scrape_category(
                cat_info['url'],
                num_pages,
                cat_info['column']
            )
           
            elapsed_time = time.time() - start_time
            progress_bar.progress(1.0)
            status_text.markdown(f"**✅ Scraping completed in {elapsed_time:.2f} seconds!**")
           
            if not df.empty:
                st.session_state[f'scraped_data_{selected_category}'] = df
                st.session_state['current_category'] = selected_category
                st.session_state['num_pages'] = num_pages
                st.session_state['elapsed_time'] = elapsed_time
            else:
                st.error("❌ No data retrieved.")
elif option_choice == "Download scraped data":
    available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
   
    if available_data:
        st.success(f"✅ {len(available_data)} category(ies) available for download")
       
        for cat_name in available_data:
            df = st.session_state[f'scraped_data_{cat_name}']
            csv = df.to_csv(index=False).encode('utf-8')
           
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label=f"📥 Download {cat_name} ({len(df)} rows)",
                    data=csv,
                    file_name=f"coinafrique_{cat_name.lower().replace(' ', '_').replace(chr(39), '')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"download_{cat_name}"
                )
    else:
        st.warning("⚠️ No scraped data available. Please scrape data first.")
elif option_choice == "Dashboard of the data":
    available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
   
    if available_data:
        st.markdown("## 📊 Data Dashboard")
       
        for cat_name in available_data:
            df = st.session_state[f'scraped_data_{cat_name}']
            cat_info_dash = CATEGORIES[cat_name]
           
            st.markdown(f"### {cat_info_dash['icon']} {cat_name}")
           
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Ads", len(df), "📦")
            with col2:
                st.metric("Unique Locations", df['adress'].nunique(), "📍")
            with col3:
                try:
                    df['price_numeric'] = df['price'].apply(clean_price)
                    avg_price = df[df['price_numeric'] > 0]['price_numeric'].mean()
                    st.metric("Average Price", f"{avg_price:,.0f} CFA", "💰")
                except:
                    st.metric("Average Price", "N/A", "💰")
            with col4:
                try:
                    median_price = df[df['price_numeric'] > 0]['price_numeric'].median()
                    st.metric("Median Price", f"{median_price:,.0f} CFA", "📊")
                except:
                    st.metric("Median Price", "N/A", "📊")
           
            # Charts
            fig = create_charts_for_category(df, cat_name, cat_info_dash['color'])
            if fig:
                st.pyplot(fig)
           
            st.markdown("---")
    else:
        st.warning("⚠️ No data available. Please scrape data first.")
elif option_choice == "Evaluate the App":
    st.markdown("## ⭐ App Evaluation")
    st.markdown("Please take a moment to evaluate our application. Your feedback is valuable for its improvement.")
   
    # MODIFICATION 2 : Suppression du KoboToolbox et de l'iframe, ajout d'un bouton pour Google Forms
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div id="button-evaluate">', unsafe_allow_html=True)
        st.link_button(
            label="✨ Fill out the Evaluation Form (Google Forms)",
            url=GOOGLE_FORMS_LINK,
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)


# Affichage des données si elles existent
if 'current_category' in st.session_state and option_choice == "Scrape data using BeautifulSoup":
    cat_name = st.session_state['current_category']
    df = st.session_state[f'scraped_data_{cat_name}']
    num_pages = st.session_state.get('num_pages', 0)
   
    st.markdown("---")
    st.markdown(f"## 📊 Results: {cat_name}")
    st.markdown(f"**Data dimension:** {len(df)} rows and {len(df.columns)} columns.")
   
    st.markdown("<br>", unsafe_allow_html=True)
   
    # Display table
    st.dataframe(df, use_container_width=True, height=400)
   
    st.markdown("<br>", unsafe_allow_html=True)
   
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name=f"coinafrique_{cat_name.lower().replace(' ', '_').replace(chr(39), '')}_{num_pages}pages.csv",
            mime="text/csv",
            use_container_width=True
        )
   
    st.markdown("<br>", unsafe_allow_html=True)
   
    # Image gallery
    st.markdown("### 🖼️ Preview of Items")
    cols = st.columns(5)
    # S'assurer que la colonne 'img' existe et que la DataFrame n'est pas vide
    if 'img' in df.columns and not df.empty:
        for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
            with col:
                # Utiliser une image de substitution si l'image est manquante
                img_url = row.img if row.img != "No Image" else "https://via.placeholder.com/300x400.png?text=No+Image"
                st.image(img_url, use_container_width=True)
                st.caption(f"💰 {row.price} CFA")
                st.caption(f"📍 {row.adress[:15]}...")
    else:
        st.info("No images to display or 'img' column missing.")
