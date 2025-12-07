import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import time

# Configuration de la page
st.set_page_config(
    page_title="Scraper Coinafrique 2025",
    page_icon="🛍️",
    layout="wide"
)

# CSS personnalisé pour le même style
st.markdown("""
<style>
    .css-1d391kg {padding-top: 1rem; padding-bottom: 3rem;}
    .big-title {font-size: 4rem !important; font-weight: 800; text-align: center; 
                background: linear-gradient(90deg, #667eea, #764ba2); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .card {background: white; padding: 2rem; border-radius: 20px; 
           box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; margin: 1rem;}
    .metric-value {font-size: 3rem; font-weight: bold; color: #667eea;}
    .metric-label {font-size: 1.2rem; color: #888;}
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-size: 1.3rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="big-title">SCRAPER COINAFRIQUE 2025</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#555;'>Récupérez les meilleures annonces de vêtements pour homme</h3>", unsafe_allow_html=True)

# Input pour le nombre de pages
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    num_pages = st.slider(
        "📄 Nombre de pages à scraper",
        min_value=1,
        max_value=120,
        value=5,
        help="Sélectionnez le nombre de pages (1-120)"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    start_scraping = st.button("🚀 LANCER LE SCRAPING")

st.markdown("---")

# Logique de scraping
if start_scraping:
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
            st.warning(f"Erreur lors du scraping de la page {i+1}")
    
    elapsed_time = time.time() - start_time
    status_text.markdown(f"**✅ Scraping terminé en {elapsed_time:.2f} secondes !**")
    
    # Affichage des résultats en cartes
    if data:
        df = pd.DataFrame(data)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Création des données pour les cartes
        stats_data = {
            "Catégorie": ["Annonces totales", "Pages scrapées", "Adresses uniques", "Temps écoulé"],
            "Valeur": [len(df), num_pages, df['adress'].nunique(), f"{elapsed_time:.1f}s"],
            "Évolution": ["📦", "📄", "📍", "⚡"]
        }
        stats_df = pd.DataFrame(stats_data)
        
        # Affichage en cartes magnifiques
        cols = st.columns(4)
        for i, row in stats_df.iterrows():
            with cols[i]:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">{row['Évolution']}</div>
                    <div class="metric-value">{row['Valeur']}</div>
                    <div class="metric-label">{row['Catégorie']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Section données
        st.subheader("📊 Données récupérées")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Bouton téléchargement
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
        
        st.markdown("---")
        
        # Galerie d'images
        st.subheader("🖼️ Aperçu des premières annonces")
        cols = st.columns(5)
        for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
            with col:
                st.image(row.img, use_container_width=True)
                st.caption(f"💰 **{row.price} CFA**")
                st.caption(f"📍 {row.adress[:20]}...")
    
    else:
        st.error("❌ Aucune donnée récupérée. Vérifiez votre connexion internet.")

else:
    # Message d'accueil
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👆 Sélectionnez le nombre de pages avec le slider ci-dessus, puis cliquez sur le bouton pour commencer le scraping !")
