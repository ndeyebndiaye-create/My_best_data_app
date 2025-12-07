import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time
import numpy as np
from scipy import stats

# ===================== CONFIGURATION =====================
st.set_page_config(
    page_title="Coinafrique Scraper 2025 - Mode & Chaussures Sénégal",
    page_icon="Shopping Bag",
    layout="wide"
)

# ===================== CSS ULTRA PREMIUM =====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(255, 245, 250, 0.95), rgba(255, 240, 245, 0.95)),
                    url('https://images.unsplash.com/photo-1558769132-cb1aea1f19e0?w=1400');
        background-size: cover;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFB6C1 0%, #FF69B4 50%, #FF1493 100%);
        box-shadow: 4px 0 20px rgba(255,20,147,0.3);
    }
    .main .block-container {
        background: rgba(255,255,255,0.98);
        border-radius: 25px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(255,105,180,0.25);
        border: 2px solid rgba(255,182,193,0.4);
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #FF1493, #FF69B4, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 5px 15px rgba(255,20,147,0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF1493, #FF69B4);
        color: white;
        font-weight: 800;
        border: none;
        border-radius: 20px;
        padding: 18px 40px;
        font-size: 1.3rem;
        box-shadow: 0 10px 30px rgba(255,20,147,0.4);
        transition: all 0.4s;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        transform: translateY(-7px);
        box-shadow: 0 20px 40px rgba(255,20,147,0.6);
        background: linear-gradient(135deg, #C71585, #FF1493);
    }
    .eval-button a {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #8B4513 !important;
        padding: 20px 50px;
        border-radius: 20px;
        font-size: 1.5rem;
        font-weight: 900;
        text-decoration: none;
        box-shadow: 0 12px 35px rgba(255,215,0,0.5);
        transition: all 0.4s;
        text-align: center;
    }
    .eval-button a:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 25px 50px rgba(255,215,0,0.7);
    }
</style>
""", unsafe_allow_html=True)

# ===================== CATÉGORIES AVEC LIENS DIRECTS =====================
CATEGORIES = {
    "Vêtements Homme": {
        "url": "https://sn.coinafrique.com/categorie/vetements-homme",
        "icon": "Men's Clothing",
        "column": "type_vetement"
    },
    "Chaussures Homme": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "icon": "Men's Shoes",
        "column": "type_chaussure"
    },
    "Vêtements Enfants": {
        "url": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "icon": "Children's Clothing",
        "column": "type_vetement_enfant"
    },
    "Chaussures Enfants": {
        "url": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "icon": "Children's Shoes",
        "column": "type_chaussure_enfant"
    }
}

# ===================== FONCTIONS SCRAPING =====================
def scrape_category(url, num_pages, column_name):
    data = []
    for page in range(1, num_pages + 1):
        try:
            res = get(f"{url}?page={page}", headers={"User-Agent": "Mozilla/5.0"})
            soup = bs(res.content, 'html.parser')
            items = soup.find_all('div', class_='col s6 m4 l3')
            for item in items:
                try:
                    title = item.find('p', class_='ad__card-description').text.strip()
                    price = item.find('p', class_='ad__card-price').text.replace('CFA','').strip()
                    location = item.find('p', class_='ad__card-location').text.strip()
                    img = item.find('img', class_='ad__card-img')['src']
                    data.append({
                        column_name: title,
                        "Prix": price,
                        "Lieu": location,
                        "Image": img
                    })
                except: pass
        except: pass
    return pd.DataFrame(data)

def clean_price(p):
    try:
        return float(str(p).replace(' ','').replace(',','').replace('.',''))
    except:
        return 0

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("<h2 style='color:#8B4513; text-align:center;'>Configuration</h2>", unsafe_allow_html=True)
    selected_category = st.selectbox("Catégorie à scraper", list(CATEGORIES.keys()))
    num_pages = st.slider("Nombre de pages", 1, 50, 10)
    
    option = st.radio("Que veux-tu faire ?", [
        "Scraper les données",
        "Télécharger les données",
        "Voir le tableau de bord",
        "Évaluer l'application"
    ])

# ===================== HEADER =====================
st.markdown('<h1 class="main-title">Coinafrique Scraper Sénégal 2025</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.3rem; color:#555;'>Scraping intelligent des catégories mode & chaussures sur Coinafrique.sn</p>", unsafe_allow_html=True)

# ===================== DATA SOURCE AVEC LIENS =====================
st.markdown("### Data source: Coinafrique Sénégal")
cols = st.columns(len(CATEGORIES))
for idx, (name, info) in enumerate(CATEGORIES.items()):
    with cols[idx]:
        st.markdown(f"[{info['icon']} {name}]({info['url']})", unsafe_allow_html=True)

st.markdown("---")

# ===================== LOGIQUE PRINCIPALE =====================
category_info = CATEGORIES[selected_category]
key = selected_category

if option == "Scraper les données":
    if st.button(f"Scraper {selected_category} ({num_pages} pages)", use_container_width=True):
        with st.spinner(f"Scraping en cours... {num_pages} pages"):
            df = scrape_category(category_info["url"], num_pages, category_info["column"])
            if not df.empty:
                st.session_state[key] = df
                st.success(f"Scraping terminé ! {len(df)} annonces récupérées")
            else:
                st.error("Aucune donnée récupérée. Vérifie ta connexion ou le site.")

elif option == "Télécharger les données":
    if key in st.session_state:
        df = st.session_state[key]
        csv = df.to_csv(index=False).encode()
        st.download_button(
            "Télécharger en CSV",
            csv,
            f"coinafrique_{selected_category.lower().replace(' ', '_')}.csv",
            "text/csv",
            use_container_width=True
        )
    else:
        st.warning("Aucune donnée scrapée pour le moment.")

elif option == "Voir le tableau de bord":
    if key in st.session_state:
        df = st.session_state[key]
        st.dataframe(df, use_container_width=True, height=500)
        
        col1, col2, col3 = st.columns(3)
        df['price_num'] = df['Prix'].apply(clean_price)
        clean = df[df['price_num'] > 0]
        col1.metric("Annonces", len(df))
        col2.metric("Prix moyen", f"{clean['price_num'].mean():,.0f} CFA")
        col3.metric("Lieux différents", df['Lieu'].nunique())
        
        st.markdown("### Aperçu des articles")
        cols = st.columns(5)
        for i, row in df.head(10).iterrows():
            with cols[i%5]:
                st.image(row['Image'], use_column_width=True)
                st.caption(f"{row['Prix']} CFA\n{row['Lieu']}")
    else:
        st.warning("Scrape d'abord des données !")

elif option == "Évaluer l'application":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;'>
        <h2>Donne-nous ton avis !</h2>
        <p>Ton retour nous aide à améliorer l'outil</p>
        <div class='eval-button'>
            <a href='https://docs.google.com/forms/d/e/1FAIpQLScPZoL1rmqr3nJvRqixQlvBphF4Tbj3MrLd9U6WyQjTLzs5hg/viewform' target='_blank'>
                Évaluer l'application maintenant
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== FIN =====================
st.markdown("<br><hr><p style='text-align:center; color:#888; font-size:0.9rem;'>Made with Streamlit + BeautifulSoup • 2025</p>", unsafe_allow_html=True)
