import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs

st.title("🛍️ Scraper Coinafrique - Vêtements Homme")
st.write("Scraper les annonces de vêtements pour homme sur Coinafrique")

# Input pour le nombre de pages
num_pages = st.number_input(
    "Nombre de pages à scraper:",
    min_value=1,
    max_value=120,
    value=5,
    step=1,
    help="Entrez le nombre de pages que vous souhaitez scraper (maximum 120)"
)

# Bouton pour lancer le scraping
if st.button("🚀 Lancer le scraping", type="primary"):
    data = []
    
    # Barre de progression
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Compteur d'annonces
    total_ads = 0
    
    for i in range(num_pages):
        status_text.text(f"Scraping de la page {i+1}/{num_pages}...")
        
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
            
            # Mise à jour de la barre de progression
            progress_bar.progress((i + 1) / num_pages)
        
        except Exception as e:
            st.warning(f"Erreur lors du scraping de la page {i+1}: {str(e)}")
    
    status_text.text(f"✅ Scraping terminé ! {total_ads} annonces récupérées.")
    
    # Création du DataFrame
    if data:
        df = pd.DataFrame(data)
        
        # Affichage des statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total d'annonces", len(df))
        with col2:
            st.metric("Pages scrapées", num_pages)
        with col3:
            st.metric("Adresses uniques", df['adress'].nunique())
        
        # Affichage du DataFrame
        st.subheader("📊 Données récupérées")
        st.dataframe(df, use_container_width=True)
        
        # Bouton de téléchargement
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name="coinafrique_vetements_homme.csv",
            mime="text/csv"
        )
        
        # Affichage des images (échantillon)
        st.subheader("🖼️ Aperçu des images (5 premières)")
        cols = st.columns(5)
        for idx, (col, row) in enumerate(zip(cols, df.head(5).itertuples())):
            with col:
                st.image(row.img, use_container_width=True)
                st.caption(f"{row.price} CFA")
    else:
        st.error("Aucune donnée n'a été récupérée. Vérifiez la connexion ou le site web.")
else:
    st.info("👆 Entrez le nombre de pages et cliquez sur 'Lancer le scraping' pour commencer")
