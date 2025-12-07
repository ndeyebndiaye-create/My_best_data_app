import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time

# Configuration de la page
st.set_page_config(
    page_title="Scraper Coinafrique",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour une meilleure esthétique
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 15px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1 {
        color: #667eea;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🛍️ Scraper Coinafrique")
st.markdown('<p class="subtitle">Récupérez facilement les annonces de vêtements pour homme</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2331/2331966.png", width=100)
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    
    num_pages = st.slider(
        "📄 Nombre de pages à scraper",
        min_value=1,
        max_value=120,
        value=5,
        help="Sélectionnez le nombre de pages (1-120)"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Informations")
    st.info(f"**Pages sélectionnées:** {num_pages}")
    st.warning("⚠️ Le scraping peut prendre quelques minutes selon le nombre de pages")
    
    st.markdown("---")
    st.markdown("### 💡 Astuce")
    st.markdown("Commencez avec 5 pages pour un test rapide")

# Zone principale
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    start_scraping = st.button("🚀 LANCER LE SCRAPING", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Logique de scraping
if start_scraping:
    data = []
    
    # Conteneur pour les messages
    status_container = st.container()
    progress_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        progress_text = st.empty()
    
    with status_container:
        status_placeholder = st.empty()
    
    total_ads = 0
    start_time = time.time()
    
    for i in range(num_pages):
        progress_text.markdown(f"**⏳ Progression:** Page {i+1} sur {num_pages}")
        
        try:
            url = f'https://sn.coinafrique.com/categorie/vetements-homme?page={i}'
            res = get(url)
            soup = bs(res.content, 'html.parser')
            containers = soup.find_all('div', class_='col s6 m4 l3')
            
            page_ads = 0
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
                    page_ads += 1
                except:
                    pass
            
            status_placeholder.success(f"✅ Page {i+1} : {page_ads} annonces récupérées")
            progress_bar.progress((i + 1) / num_pages)
            
        except Exception as e:
            status_placeholder.error(f"❌ Erreur page {i+1}: {str(e)}")
    
    elapsed_time = time.time() - start_time
    progress_text.markdown(f"**✅ Scraping terminé en {elapsed_time:.2f} secondes !**")
    
    # Affichage des résultats
    if data:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## 📈 Résultats du Scraping")
        
        # Métriques
        col1, col2, col3, col4 = st.columns(4)
        
        df = pd.DataFrame(data)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <h2 style="color: #667eea; margin: 0;">📦</h2>
                    <h3 style="margin: 10px 0;">{}</h3>
                    <p style="color: #6c757d; margin: 0;">Annonces totales</p>
                </div>
            """.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <h2 style="color: #f093fb; margin: 0;">📄</h2>
                    <h3 style="margin: 10px 0;">{}</h3>
                    <p style="color: #6c757d; margin: 0;">Pages scrapées</p>
                </div>
            """.format(num_pages), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <h2 style="color: #4facfe; margin: 0;">📍</h2>
                    <h3 style="margin: 10px 0;">{}</h3>
                    <p style="color: #6c757d; margin: 0;">Adresses uniques</p>
                </div>
            """.format(df['adress'].nunique()), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <h2 style="color: #43e97b; margin: 0;">⚡</h2>
                    <h3 style="margin: 10px 0;">{:.1f}s</h3>
                    <p style="color: #6c757d; margin: 0;">Temps écoulé</p>
                </div>
            """.format(elapsed_time), unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Tableau de données
        st.markdown("### 📊 Données récupérées")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Téléchargement
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name=f"coinafrique_vetements_{num_pages}pages.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Galerie d'images
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🖼️ Galerie d'images")
        
        cols = st.columns(5)
        for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
            with col:
                st.image(row.img, use_container_width=True)
                st.caption(f"💰 {row.price} CFA")
                st.caption(f"📍 {row.adress[:20]}...")
    else:
        st.error("❌ Aucune donnée récupérée. Vérifiez votre connexion internet.")

else:
    # Message d'accueil
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 Configurez le nombre de pages dans le menu latéral, puis cliquez sur le bouton pour commencer !")
        
        # Image de démonstration
        st.image("https://cdn-icons-png.flaticon.com/512/1170/1170678.png", width=200)
