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

# CSS personnalisé avec images de fond
st.markdown("""
<style>
    /* Fond principal avec image de vêtements */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
                    url('https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=1200&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    
    /* Sidebar avec image de mode */
    [data-testid="stSidebar"] {
        background: linear-gradient(rgba(176, 224, 230, 0.95), rgba(176, 224, 230, 0.95)),
                    url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&q=80');
        background-size: cover;
        background-position: center;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Titres sidebar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #2c3e50 !important;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
    }
    
    /* Labels sidebar */
    [data-testid="stSidebar"] label {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    /* Select boxes sidebar */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    
    /* Zone principale */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    
    /* Titre principal */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(90deg, #48c9b0 0%, #20a39e 100%) !important;
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(72, 201, 176, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(72, 201, 176, 0.4);
        background: linear-gradient(90deg, #20a39e 0%, #48c9b0 100%) !important;
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
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #48c9b0 0%, #20a39e 100%);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
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
        index=0,
        key="pages_select"
    )
    
    st.markdown("---")
    st.markdown("### Options")
    
    option_choice = st.selectbox(
        "Choisir une option",
        [
            "Scrape data using BeautifulSoup",
            "Scrape data using beautiful...",
            "Download scraped data",
            "Dashboard of the data",
            "Evaluate the App"
        ],
        key="option_select"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Info")
    st.info(f"**Pages:** {num_pages}\n\n**Option:** {option_choice[:20]}...")

# Zone principale
st.markdown('<h1 class="main-title">🛍️ Scraper Coinafrique - Vêtements Homme</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Cette application permet de scraper les données de vêtements depuis coinafrique.com sur plusieurs pages. Vous pouvez également télécharger les données scrapées directement ou visualiser un dashboard.</p>', unsafe_allow_html=True)

st.markdown("**Python libraries:** base64, pandas, streamlit, requests, bs4")
st.markdown("**Data source:** [Coinafrique Sénégal](https://sn.coinafrique.com) — [Catégorie Vêtements](https://sn.coinafrique.com/categorie/vetements-homme)")

st.markdown("<br>", unsafe_allow_html=True)

# Logique selon l'option choisie
if option_choice == "Scrape data using BeautifulSoup":
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

elif option_choice == "Download scraped data":
    if 'scraped_data' in st.session_state:
        df = st.session_state['scraped_data']
        st.success(f"✅ {len(df)} annonces disponibles pour téléchargement")
        
        csv = df.to_csv(index=False).encode('utf-8')
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Télécharger les données CSV",
                data=csv,
                file_name=f"coinafrique_vetements.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.warning("⚠️ Aucune donnée scrapée disponible. Veuillez d'abord scraper les données.")

elif option_choice == "Dashboard of the data":
    if 'scraped_data' in st.session_state:
        df = st.session_state['scraped_data']
        
        st.markdown("## 📊 Dashboard des données")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total annonces", len(df), "📦")
        with col2:
            st.metric("Adresses uniques", df['adress'].nunique(), "📍")
        with col3:
            st.metric("Prix moyen", f"{df['price'].astype(str).str.replace(' ', '').str.replace(',', '').apply(lambda x: float(x) if x.replace('.','').isdigit() else 0).mean():.0f} CFA", "💰")
        
        st.markdown("### 📈 Distribution des prix")
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
if 'scraped_data' in st.session_state and option_choice == "Scrape data using BeautifulSoup":
    df = st.session_state['scraped_data']
    num_pages = st.session_state.get('num_pages', 0)
    
    st.markdown("---")
    st.markdown("## 📊 Display data dimension")
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
            file_name=f"coinafrique_vetements_{num_pages}pages.csv",
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

if option_choice not in ["Scrape data using BeautifulSoup", "Download scraped data", "Dashboard of the data", "Evaluate the App"]:
    st.info("🔧 Cette fonctionnalité est en cours de développement...")
