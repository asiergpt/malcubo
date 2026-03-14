import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    /* =========================================
       1. FONDO GLOBAL BLANCO Y LIMPIEZA
       ========================================= */
    #MainMenu, header, footer { visibility: hidden; display: none; }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }

    .block-container {
        padding: 4rem 1rem 3rem 1rem !important;
        max-width: 1000px !important;
    }

    /* =========================================
       BOTÓN COLAPSO SIDEBAR — visible y dorado
       ========================================= */

    /* Ocultar el texto "keyboard_double" de Material Icons
       manteniendo el botón completamente funcional */
    [data-testid="stSidebarCollapseButton"] button span {
        display: none !important;
    }

    /* Estilizar el botón completo */
    [data-testid="stSidebarCollapseButton"] button {
        background: #0d0d0d !important;
        border: 1px solid rgba(255,204,102,0.4) !important;
        border-radius: 8px !important;
        width: 36px !important;
        height: 36px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
        padding: 0 !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #1a1a1a !important;
        border-color: #ffcc66 !important;
        box-shadow: 0 0 16px rgba(255,204,102,0.2) !important;
    }

    /* SVG dentro del botón — dorado */
    [data-testid="stSidebarCollapseButton"] button svg {
        color: rgba(255,204,102,0.7) !important;
        fill: rgba(255,204,102,0.7) !important;
        width: 18px !important;
        height: 18px !important;
        display: block !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover svg {
        color: #ffcc66 !important;
        fill: #ffcc66 !important;
    }

    /* =========================================
       2. EXPANSORES OSCUROS (HOME)
       — Solo afectan cuando hay clase .home-page
       ========================================= */
    .home-page details {
        background-color: #0d0d0d !important;
        border: 1px solid rgba(255, 204, 102, 0.18) !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
        transition: border-color 0.3s ease !important;
    }
    .home-page details:hover {
        border-color: rgba(255,204,102,0.45) !important;
    }
    .home-page details summary,
    .home-page details summary:hover,
    .home-page details summary:focus {
        background-color: #0d0d0d !important;
    }
    .home-page details [data-testid="stExpanderDetails"] {
        background-color: #0d0d0d !important;
    }
    .home-page details summary [data-testid="stMarkdownContainer"],
    .home-page details summary [data-testid="stMarkdownContainer"] * {
        font-family: 'Quicksand', sans-serif !important;
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        color: transparent !important;
        -webkit-text-stroke: 0.7px rgba(255,204,102,0.85) !important;
        text-shadow: 0 0 10px rgba(255,204,102,0.2) !important;
        margin: 0 !important;
    }
    .home-page details summary:hover [data-testid="stMarkdownContainer"],
    .home-page details summary:hover [data-testid="stMarkdownContainer"] * {
        -webkit-text-stroke: 1px #ffcc66 !important;
        text-shadow: 0 0 16px rgba(255,204,102,0.4) !important;
    }
    .home-page details summary svg {
        color: rgba(255,204,102,0.6) !important;
        fill: rgba(255,204,102,0.6) !important;
    }
    .home-page details summary:hover svg {
        color: #ffcc66 !important;
        fill: #ffcc66 !important;
    }

    /* =========================================
       3. BOTONES HOME — solo dentro de .home-page
       ========================================= */
    .home-page div[data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
        gap: 20px !important;
    }
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] div[data-testid="stButton"] {
        width: 100%;
        margin: 0 !important;
        padding: 0 !important;
    }
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] div[data-testid="stButton"] > button {
        width: 100% !important;
        background-color: #0d0d0d !important;
        color: #ffcc66 !important;
        border: 1px solid rgba(255,204,102,0.2) !important;
        border-top: none !important;
        border-radius: 0 0 18px 18px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.68rem !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        padding: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] div[data-testid="stButton"] > button:hover {
        background-color: #ffcc66 !important;
        color: #0d0d0d !important;
        border-color: #ffcc66 !important;
        letter-spacing: 4px !important;
        box-shadow: 0 8px 24px rgba(255,204,102,0.25) !important;
    }
    /* Doble botón tarjeta 3 */
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stButton"] > button {
        border-radius: 0 0 0 18px !important;
        border-right: 1px solid rgba(255,204,102,0.12) !important;
    }
    .home-page div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] > button {
        border-radius: 0 0 18px 0 !important;
        border-left: none !important;
    }

    @media (max-width: 768px) {
        .block-container { padding-top: 4rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)