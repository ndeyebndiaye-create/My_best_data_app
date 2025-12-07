import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time

# Configuration de la page
st.set_page_config(
    page_title="Scraper Coinafrique - Vêtements",
    page_icon="👔",
    layout="wide"
)

# CSS personnalisé avec thème vêtements (couleurs fashion)
st.markdown("""
<style>
    /* Couleurs principales - thème mode/vêtements */
    :root {
        --primary-color: #E91E63;
        --secondary-color: #9C27B0;
        --accent-color: #FF4081;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Fond principal */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #89CFF0 0%, #6B8DD6 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #89CFF0 0%, #6B8DD6 100%);
    }
    
    /* Titres sidebar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700;
    }
    
    /* Labels sidebar */
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Zone principale */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    /* Titre principal */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        color: #764ba2;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(90deg, #E91E63 0%, #9C27B0 100%) !important;
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 15px;
        padding: 15px 30px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(233, 30, 99, 0.4);
    }
    
    /* Cartes de données */
    .data-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid #f0f0f0;
    }
    
    /* Tableau */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 15px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #E91E63 0%, #9C27B0 100%);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 👔 User Input Features")
    st.markdown("---")
    
    st.markdown("### Pages Indexes")
    num_pages = st.selectbox(
        "Nombre de pages",
        options=[5, 10, 15, 20, 25, 30, 50, 75, 100, 120],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### Options")
    scrape_option = st.selectbox(
        "Mode de scraping",
        ["Scrape data using BeautifulSoup", "Load data from CSV"]
    )
    
    st.markdown("---")
    st.markdown("### 📊 Info")
    st.info(f"**Pages sélectionnées:** {num_pages}\n\n**Source:** Coinafrique Sénégal")

# Zone principale
st.markdown('<h1 class="main-title">🛍️ Scraper Coinafrique - Vêtements Homme</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Cette application permet de scraper les données de vêtements depuis coinafrique.com sur plusieurs pages. Vous pouvez également télécharger les données directement sans les scraper.</p>', unsafe_allow_html=True)

st.markdown("**Python libraries:** base64, pandas, streamlit, requests, bs4")
st.markdown("**Data source:** [Expat-Dakar](https://sn.coinafrique.com) — [Dakar-Auto](https://sn.coinafrique.com)")

st.markdown("<br>", unsafe_allow_html=True)

# Bouton principal
if scrape_option == "Scrape data using BeautifulSoup":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👕 Scraper les vêtements"):
            data = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_ads = 0
            start_time = time.time()
            
            for i in range(num_pages):
                status_text.markdown(f"**⏳ Scraping en cours... Page {i+1}/{num_pages}**")
                
                try:
                    url = f'https://sn.coinafrique.com/categorie/vetements-homme?page={i}'
                    res = get(url)
                    soup = bs(res.content, 'html.parser')
                    containers = soup.find_all('div', class_='col s6 m4 l3')
                    
                    for container in containers:
                        try:
                            type_habits = container.find('p', 'ad__card-description').text.strip()
                            price = container.find('p', class_='ad__card-price').text.replace('CFA', '').strip()
                            adress = container.find('p', class_='ad__card-location').text.strip()
                            img = (container.find('img', class_='ad__card-img'))['src']
                            
                            dic = {
                                'type_habits': type_habits,
                                'price': price,
                                'adress': adress,
                                'img': img
                            }
                            data.append(dic)
                            total_ads += 1
                        except:
                            pass
                    
                    progress_bar.progress((i + 1) / num_pages)
                    
                except Exception as e:
                    st.warning(f"Erreur page {i+1}")
            
            elapsed_time = time.time() - start_time
            status_text.markdown(f"**✅ Scraping terminé en {elapsed_time:.2f} secondes !**")
            
            if data:
                df = pd.DataFrame(data)
                st.session_state['scraped_data'] = df
                st.session_state['num_pages'] = num_pages
                st.session_state['elapsed_time'] = elapsed_time

# Affichage des données si elles existent
if 'scraped_data' in st.session_state:
    df = st.session_state['scraped_data']
    num_pages = st.session_state.get('num_pages', 0)
    elapsed_time = st.session_state.get('elapsed_time', 0)
    
    st.markdown("---")
    st.markdown("## 📊 Display data dimension")
    st.markdown(f"**Data dimension:** {len(df)} rows and {len(df.columns)} columns.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Affichage du tableau
    st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton téléchargement
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download data as CSV",
        data=csv,
        file_name=f"coinafrique_vetements_{num_pages}pages.csv",
        mime="text/csv"
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

else:
    st.info("👈 Sélectionnez les options dans le menu latéral et cliquez sur le bouton pour commencer le scraping !")
    st.markdown("<br><br>", unsafe_allow_html=True)
