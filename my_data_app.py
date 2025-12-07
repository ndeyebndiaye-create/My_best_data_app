import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ------------------------------
# 1. Fonction pour récupérer le HTML d'une page
# ------------------------------
def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, "html.parser")

# ------------------------------
# 2. Trouver le nombre total de pages
# ------------------------------
base_url = "https://sn.coinafrique.com/categorie/vetements-homme?page="
soup = get_page(base_url + "1")

pages = 1
pagination = soup.find_all("a", class_="page-link")
if pagination:
    nums = []
    for p in pagination:
        try:
            nums.append(int(p.text))
        except:
            pass
    if nums:
        pages = max(nums)

print("Nombre total de pages détectées :", pages)

# ------------------------------
# 3. Scraping de toutes les pages
# ------------------------------
data = []

for page in range(1, pages + 1):
    print(f"Scraping page {page} / {pages}")
    url = base_url + str(page)
    soup = get_page(url)

    containers = soup.find_all("div", class_="ad__card")

    for c in containers:
        # Récupérer chaque champ en évitant les erreurs
        type_habits = c.find("p", class_="ad__card-description")
        price = c.find("p", class_="ad__card-price")
        adress = c.find("p", class_="ad__card-location")
        img = c.find("img", class_="ad__card-img")

        data.append({
            "type_habits": type_habits.text.strip() if type_habits else None,
            "price": price.text.replace("CFA", "").strip() if price else None,
            "adress": adress.text.strip() if adress else None,
            "img": img["src"] if img else None
        })

    time.sleep(1)  # éviter de surcharger le serveur

# ------------------------------
# 4. Export CSV
# ------------------------------
df = pd.DataFrame(data)
df.to_csv("vetements_homme.csv", index=False, encoding="utf-8")

print("Scraping terminé ! Fichier créé : vetements_homme.csv")
