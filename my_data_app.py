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
GOOGLE_FORMS_LINK = "https://docs.google.com/forms/d/e/1FAIpQLScPZoL1rmqr3nJvRqixLlvBphF4Tbj3MrLd9U6WyQjTLzs5hg/viewform?usp=dialog"
KOBOTOOLBOX_LINK = "https://ee.kobotoolbox.org/x/LNbLn5W1"

# Page Configuration
st.set_page_config(
    page_title="Coinafrique Scraper Pro",
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS with Fashion Theme (BACKGROUND FIX APPLIED HERE)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* WELCOME PAGE - Shopping Background (INCHANGÉ) */
    .welcome-container {
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)),
                    url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1920&q=90');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        border-radius: 25px;
        padding: 4rem 2rem;
        margin: -1rem -2rem;
        min-height: 85vh;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    /* ALL ACTION PAGES - NOUVEAU STYLE AVEC FOND ET OVERLAY */
    .scraping-page, .download-page, .dashboard-page, .evaluation-page {
        /* Copie de la structure du Welcome Container */
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)),
                    url('https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=1920&q=90'); /* Image Ventes/Sacs */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        border-radius: 20px; /* Légèrement plus petit pour l'action */
        padding: 2rem;
        margin: -1rem -2rem;
        min-height: 100vh;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(21, 101, 192, 0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .welcome-title {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(21, 101, 192, 0.2);
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    .welcome-subtitle {
        text-align: center;
        color: #546e7a;
        font-size: 1.4rem;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(21, 101, 192, 0.1);
        position: relative;
        z-index: 1;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(21, 101, 192, 0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1565c0;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #546e7a;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* MAIN APP BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* SIDEBAR - Elegant Navy Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #0d47a1 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* MAIN CONTENT CARD - Rendre la carte plus transparente pour voir le fond */
    .main .block-container {
        /* Opacité à 0.85 pour laisser l'image de fond transparaître */
        background: rgba(255, 255, 255, 0.85); 
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
    }
    
    /* TITLES */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 50%, #42a5f5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #546e7a;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.7;
    }
    
    /* BUTTONS - Primary (Scrape) */
    .stButton>button {
        background: linear-gradient(135deg, #1565c0 0%, #1976d2 100%) !important;
        color: white !important;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 18px 40px;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        width: 100%;
        box-shadow: 0 8px 25px rgba(21, 101, 192, 0.4);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(21, 101, 192, 0.6);
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    
    /* START BUTTON (Welcome Page) */
    .start-button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%) !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.5);
    }
    
    .start-button:hover {
        background: linear-gradient(135deg, #388e3c 0%, #4caf50 100%) !important;
        box-shadow: 0 15px 40px rgba(76, 175, 80, 0.7);
    }
    
    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ff9800 0%, #ffa726 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 15px 30px;
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
        border: none;
        text-transform: uppercase;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 152, 0, 0.6);
    }
    
    /* METRICS */
    [data-testid="stMetricValue"] {
        color: #1565c0;
        font-weight: 800;
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #546e7a;
        font-weight: 600;
    }
    
    /* ALERTS */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #1976d2;
        background: rgba(25, 118, 210, 0.05);
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1565c0 0%, #42a5f5 100%);
        border-radius: 10px;
    }
    
    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* IMAGES */
    img {
        border-radius: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    img:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 35px rgba(21, 101, 192, 0.3);
    }
    
    /* SEPARATOR */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #1976d2 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* LINK BUTTONS (Evaluation) */
    .stLinkButton > a {
        background: linear-gradient(135deg, #00897b 0%, #26a69a 100%) !important;
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 15px 30px;
        text-decoration: none;
        display: inline-block;
        width: 100%;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 137, 123, 0.4);
        transition: all 0.3s ease;
    }
    
    .stLinkButton > a:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 137, 123, 0.6);
    }
    
    /* ANIMATIONS */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: fadeInUp 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ... (Le reste du code Python est inchangé) ...
