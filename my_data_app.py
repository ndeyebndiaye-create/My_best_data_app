import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time

# Configuration de la page
st.set_page_config(
    page_title="Scraper Coinafrique - Multi-Catégories",
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
    
    /* Tabs stylisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.6);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(255, 182, 193, 0.3), rgba(255, 218, 185, 0.3));
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 700;
        border: 2px solid rgba(255, 182, 193, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF69B4, #FFD700) !important;
        color: white !important;
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
</style>
""", unsafe_allow_html=True)

# Configuration des catégories
CATEGORIES = {
    "Vêtements Homme 👔": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "icon": "👔",
        "column": "type_habits"
    },
    "Chaussures Homme 👞": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "icon": "👞",
        "column": "type_shoes"
    },
    "Vêtements Enfants 👶": {
        "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "icon": "👶",
        "column": "type_clothes"
    },
    "Chaussures Enfants 👟": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "icon": "👟",
        "column": "type_shoes"
    }
}

# Fonction de scraping
def scrape_category(url, num_pages, column_name):
    """Scrape une catégorie spécifique"""
    data = []
    
    for i in range(num_pages):
        try:
            page_url = f'{url}?page={i}'
            res = get(page_url)
            soup = bs(res.content, 'html.parser')
            containers = soup.find_all('div', class_='col s6 m4 l3')
            
            for container in containers:
                try:
                    item_type = container.find('p', 'ad__card-description').text.strip()
                    price = container.find('p', class_='ad__card-price').text.replace('CFA', '').strip()
                    adress = container.find('p', class_='ad__card-location').text.strip()
                    img = (container.find('img', class_='ad__card-img'))['src']
                    
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

# Sidebar
with st.sidebar:
    st.markdown("## 🛍️ User Input Features")
    st.markdown("---")
    
    st.markdown("### Catégorie")
    selected_category = st.selectbox(
        "Choisir une catégorie",
        list(CATEGORIES.keys()),
        key="category_select"
    )
    
    st.markdown("### Pages Indexes")
    num_pages = st.selectbox(
        "Nombre de pages",
        options=[5, 10, 15, 20, 25, 30, 50, 75, 100, 120],
        index=0,
        key="pages_select"
    )
    
    st.markdown("---")
    st.markdown("### Options")
    
    option_choice = st.selectbox(
        "Choisir une option",
        [
            "Scrape data using BeautifulSoup",
            "Download scraped data",
            "Dashboard of the data",
            "Scrape ALL categories",
            "Evaluate the App"
        ],
        key="option_select"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Info")
    st.info(f"**Catégorie:** {selected_category}\n\n**Pages:** {num_pages}")

# Zone principale
st.markdown('<h1 class="main-title">🛍️ Scraper Coinafrique Multi-Catégories</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Scrapez des données de 4 catégories : vêtements homme, chaussures homme, vêtements enfants et chaussures enfants depuis coinafrique.com</p>', unsafe_allow_html=True)

st.markdown("**Python libraries:** base64, pandas, streamlit, requests, bs4")
st.markdown("**Data source:** [Coinafrique Sénégal](https://sn.coinafrique.com)")

st.markdown("<br>", unsafe_allow_html=True)

# Logique selon l'option choisie
if option_choice == "Scrape data using BeautifulSoup":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        category_info = CATEGORIES[selected_category]
        if st.button(f"{category_info['icon']} Scraper {selected_category}"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            status_text.markdown(f"**⏳ Scraping de {selected_category} en cours...**")
            
            df = scrape_category(
                category_info['url'], 
                num_pages, 
                category_info['column']
            )
            
            elapsed_time = time.time() - start_time
            progress_bar.progress(1.0)
            status_text.markdown(f"**✅ Scraping terminé en {elapsed_time:.2f} secondes !**")
            
            if not df.empty:
                st.session_state[f'scraped_data_{selected_category}'] = df
                st.session_state['current_category'] = selected_category
                st.session_state['num_pages'] = num_pages
                st.session_state['elapsed_time'] = elapsed_time
            else:
                st.error("❌ Aucune donnée récupérée.")

elif option_choice == "Scrape ALL categories":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Scraper TOUTES les catégories"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            total_categories = len(CATEGORIES)
            
            for idx, (cat_name, cat_info) in enumerate(CATEGORIES.items()):
                status_text.markdown(f"**⏳ Scraping {cat_name}... ({idx+1}/{total_categories})**")
                
                df = scrape_category(
                    cat_info['url'], 
                    num_pages, 
                    cat_info['column']
                )
                
                if not df.empty:
                    st.session_state[f'scraped_data_{cat_name}'] = df
                
                progress_bar.progress((idx + 1) / total_categories)
            
            elapsed_time = time.time() - start_time
            status_text.markdown(f"**✅ Toutes les catégories scrapées en {elapsed_time:.2f} secondes !**")
            st.session_state['all_scraped'] = True
            st.session_state['elapsed_time'] = elapsed_time

elif option_choice == "Download scraped data":
    available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
    
    if available_data:
        st.success(f"✅ {len(available_data)} catégorie(s) disponible(s) pour téléchargement")
        
        for cat_name in available_data:
            df = st.session_state[f'scraped_data_{cat_name}']
            csv = df.to_csv(index=False).encode('utf-8')
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label=f"📥 Télécharger {cat_name} ({len(df)} lignes)",
                    data=csv,
                    file_name=f"coinafrique_{cat_name.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.warning("⚠️ Aucune donnée scrapée disponible. Veuillez d'abord scraper les données.")

elif option_choice == "Dashboard of the data":
    available_data = [cat for cat in CATEGORIES.keys() if f'scraped_data_{cat}' in st.session_state]
    
    if available_data:
        st.markdown("## 📊 Dashboard des données")
        
        # Créer des onglets pour chaque catégorie
        tabs = st.tabs(available_data)
        
        for idx, cat_name in enumerate(available_data):
            with tabs[idx]:
                df = st.session_state[f'scraped_data_{cat_name}']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total annonces", len(df), "📦")
                with col2:
                    st.metric("Adresses uniques", df['adress'].nunique(), "📍")
                with col3:
                    try:
                        avg_price = df['price'].astype(str).str.replace(' ', '').str.replace(',', '').apply(
                            lambda x: float(x) if x.replace('.','').isdigit() else 0
                        ).mean()
                        st.metric("Prix moyen", f"{avg_price:.0f} CFA", "💰")
                    except:
                        st.metric("Prix moyen", "N/A", "💰")
                
                st.markdown("### 📈 Distribution des localisations")
                st.bar_chart(df['adress'].value_counts().head(10))
    else:
        st.warning("⚠️ Aucune donnée disponible. Veuillez d'abord scraper les données.")

elif option_choice == "Evaluate the App":
    st.markdown("## ⭐ Évaluation de l'application")
    
    rating = st.slider("Note globale", 1, 5, 5)
    feedback = st.text_area("Vos commentaires", placeholder="Partagez votre expérience...")
    
    if st.button("Soumettre l'évaluation"):
        st.success(f"Merci pour votre note de {rating}/5 étoiles ! 🌟")

# Affichage des données si elles existent
if 'current_category' in st.session_state and option_choice == "Scrape data using BeautifulSoup":
    cat_name = st.session_state['current_category']
    df = st.session_state[f'scraped_data_{cat_name}']
    num_pages = st.session_state.get('num_pages', 0)
    
    st.markdown("---")
    st.markdown(f"## 📊 Résultats : {cat_name}")
    st.markdown(f"**Data dimension:** {len(df)} rows and {len(df.columns)} columns.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Affichage du tableau
    st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton téléchargement
    csv = df.to_csv(index=False).encode('utf-8')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name=f"coinafrique_{cat_name.lower().replace(' ', '_')}_{num_pages}pages.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Galerie d'images
    st.markdown("### 🖼️ Aperçu des articles")
    cols = st.columns(5)
    for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
        with col:
            st.image(row.img, use_container_width=True)
            st.caption(f"💰 {row.price} CFA")
            st.caption(f"📍 {row.adress[:15]}...")

if 'all_scraped' in st.session_state and option_choice == "Scrape ALL categories":
    st.markdown("---")
    st.markdown("## 🎉 Toutes les catégories ont été scrapées !")
    
    for cat_name in CATEGORIES.keys():
        if f'scraped_data_{cat_name}' in st.session_state:
            df = st.session_state[f'scraped_data_{cat_name}']
            st.success(f"✅ {cat_name}: {len(df)} annonces récupérées")

if option_choice not in ["Scrape data using BeautifulSoup", "Download scraped data", "Dashboard of the data", "Scrape ALL categories", "Evaluate the App"]:
    st.info("🔧 Cette fonctionnalité est en cours de développement...")
