import streamlit as st
import pandas as pd
import math
import re
import base64
import os
from utils.helpers import (
    clean_number_format, safe_get_val, capitalize_first_letter,
    has_private_equity, uses_ai
)

ITEMS_PER_PAGE = 20

def get_image_base64(path):
    try:
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except Exception:
        return ""

def show_explorer(df_main, df_alumni, empresas_alumni_set):

    if st.query_params.get("nav") == "home":
        st.query_params.clear()
        st.session_state.page = 'home'
        st.rerun()

    current_dir = os.path.dirname(__file__)
    img_oculto = get_image_base64(os.path.join(current_dir, "..", "assets", "oculto.png"))
    img_tag = (
        f'<img src="{img_oculto}" alt="Explorador" '
        f'style="height:80px;object-fit:contain;filter:drop-shadow(0 4px 16px rgba(255,204,102,0.2));">'
        if img_oculto else "🏢"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main .block-container {
        background-color: #ffffff !important;
    }

    .exp-hero {
        background: #0d0d0d;
        border-radius: 20px;
        padding: 32px 44px 52px 44px;
        display: flex; align-items: center; gap: 32px;
        border: 1px solid rgba(255,204,102,0.15);
        margin-bottom: 20px;
        position: relative;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .exp-hero:hover {
        border-color: rgba(255,204,102,0.6);
        box-shadow: 0 0 0 1px rgba(255,204,102,0.2), 0 0 24px rgba(255,204,102,0.1);
    }
    .exp-hero-img { flex:0 0 auto; width:90px; display:flex; align-items:center; }
    .exp-hero-text { flex: 1; }
    .exp-hero-title {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.6rem; font-weight: 700;
        color: transparent;
        -webkit-text-stroke: 1.2px #ffcc66;
        text-shadow: 0 0 14px rgba(255,204,102,0.2);
        line-height: 1.1; margin-bottom: 8px;
    }
    .exp-hero-sub {
        font-family: 'Manrope', sans-serif;
        font-size: 0.85rem; font-weight: 300;
        color: #888; line-height: 1.6;
    }
    .exp-back-btn {
        position: absolute; bottom: 14px; left: 36px;
        font-family: 'Manrope', sans-serif;
        font-size: 0.60rem; font-weight: 600;
        letter-spacing: 2.5px; text-transform: uppercase;
        color: rgba(255,204,102,0.55) !important;
        -webkit-text-fill-color: rgba(255,204,102,0.55);
        border: 1px solid rgba(255,204,102,0.2); border-radius: 6px;
        padding: 4px 11px; background: transparent;
        text-decoration: none !important; display: inline-block;
        transition: all 0.2s ease;
    }
    .exp-back-btn:hover {
        color: #ffcc66 !important; -webkit-text-fill-color: #ffcc66;
        border-color: rgba(255,204,102,0.6); background: rgba(255,204,102,0.06);
    }
    .exp-back-btn:visited, .exp-back-btn:link {
        color: rgba(255,204,102,0.55) !important;
        -webkit-text-fill-color: rgba(255,204,102,0.55);
        text-decoration: none !important;
    }

    /* Filtros */
    .filter-section {
        background: #f8f8f8; border-radius: 14px;
        padding: 18px 20px; margin-bottom: 20px;
        border: 1px solid #eeeeee;
    }
    .filter-section-title {
        font-family: 'Manrope', sans-serif;
        font-size: 0.60rem; font-weight: 600;
        letter-spacing: 2.5px; text-transform: uppercase;
        color: #aaaaaa; margin-bottom: 14px;
        display: flex; align-items: center; gap: 7px;
    }
    .filter-section [data-testid="stWidgetLabel"] p {
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.65rem !important; font-weight: 600 !important;
        letter-spacing: 1px !important; text-transform: uppercase !important;
        color: #999999 !important;
    }
    .filter-section [data-testid="stTextInput"] input,
    .filter-section [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        font-family: 'Manrope', sans-serif !important;
        color: #333333 !important;
    }
    .filter-section [data-testid="stTextInput"] input:focus,
    .filter-section [data-baseweb="select"] > div:focus-within {
        border-color: rgba(255,204,102,0.5) !important;
        box-shadow: 0 0 0 1px rgba(255,204,102,0.12) !important;
    }

    /* Resultados */
    .results-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 16px; background: #f8f8f8;
        border-radius: 8px; margin-bottom: 14px;
        font-family: 'Manrope', sans-serif; font-size: 0.82rem; color: #666;
    }
    .results-bar b { color: #111; }

    /* Expansores */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e8e8e8 !important;
        border-radius: 12px !important; margin-bottom: 10px !important;
        overflow: hidden !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(255,204,102,0.55) !important;
        box-shadow: 0 4px 20px rgba(255,204,102,0.1), 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    details summary, details summary:hover, details summary:focus {
        background-color: #ffffff !important;
    }
    details [data-testid="stExpanderDetails"] { background-color: #ffffff !important; }
    details summary [data-testid="stMarkdownContainer"],
    details summary [data-testid="stMarkdownContainer"] * {
        font-family: 'Quicksand', sans-serif !important;
        font-size: 0.92rem !important; font-weight: 700 !important;
        color: #111111 !important; -webkit-text-stroke: 0px !important;
        text-shadow: none !important;
    }
    details summary svg { color: #cccccc !important; fill: #cccccc !important; }
    [data-testid="stExpander"]:hover details summary svg {
        color: #ffcc66 !important; fill: #ffcc66 !important;
    }

    /* Métricas */
    .metric-row { display: flex; gap: 10px; margin-bottom: 16px; }
    .metric-card {
        flex: 1; background: #f8f8f8; border: 1px solid #f0f0f0;
        border-radius: 10px; padding: 14px 16px;
        display: flex; flex-direction: column; min-height: 80px;
    }
    .metric-label {
        font-family: 'Manrope', sans-serif; font-size: 0.60rem; font-weight: 600;
        letter-spacing: 2px; text-transform: uppercase; color: #aaaaaa;
        margin-bottom: 10px;
    }
    .metric-value {
        font-family: 'Quicksand', sans-serif; font-size: 1.15rem; font-weight: 700;
        color: #111111; text-align: center; flex: 1;
        display: flex; align-items: center; justify-content: center;
    }

    /* Botón ver perfil */
    details [data-testid="stExpanderDetails"] [data-testid="stButton"] > button {
        font-family: 'Manrope', sans-serif !important; font-size: 0.78rem !important;
        font-weight: 600 !important; background: #ffffff !important;
        color: #333333 !important; border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important; padding: 8px 12px !important;
        width: 100% !important; transition: all 0.2s ease !important;
        box-shadow: none !important; text-transform: none !important;
        letter-spacing: normal !important;
    }
    details [data-testid="stExpanderDetails"] [data-testid="stButton"] > button:hover {
        border-color: rgba(255,204,102,0.55) !important;
        background: rgba(255,204,102,0.04) !important; color: #111111 !important;
    }

@media (max-width: 640px) {
    .metric-row {
        flex-wrap: wrap;
        gap: 8px;
    }
    .metric-card {
        flex: 1 1 calc(50% - 4px);
        min-width: calc(50% - 4px);
        padding: 10px 12px;
        min-height: 68px;
    }
    .metric-label {
        font-size: 0.52rem;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 0.95rem;
    }
}
    </style>
    """, unsafe_allow_html=True)

    # HERO
    st.markdown(f"""
    <div class="exp-hero">
        <div class="exp-hero-img">{img_tag}</div>
        <div class="exp-hero-text">
            <div class="exp-hero-title">Explorador de Empresas</div>
            <div class="exp-hero-sub">Filtra y encuentra tu empresa objetivo en el ecosistema vasco.</div>
        </div>
        <a class="exp-back-btn" href="?nav=home">← Inicio</a>
    </div>
    """, unsafe_allow_html=True)

    # FILTROS

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.f_nombre = st.text_input(
            "Nombre empresa", value=st.session_state.f_nombre,
            placeholder="Buscar por nombre..."
        )
    with col2:
        provs = sorted(df_main['provincia'].dropna().unique().tolist())
        st.session_state.f_provincia = st.multiselect(
            "Provincia", provs, default=st.session_state.f_provincia
        )

    col3, col4, col5, col6 = st.columns(4)
    with col3:
        st.session_state.f_patentes = st.selectbox(
            "Patentes", ["Todos", "Sí", "No"],
            index=["Todos", "Sí", "No"].index(st.session_state.f_patentes)
        )
    with col4:
        st.session_state.f_pe = st.selectbox(
            "Private Equity", ["Todos", "Sí", "No"],
            index=["Todos", "Sí", "No"].index(st.session_state.f_pe)
        )
    with col5:
        st.session_state.f_ia = st.selectbox(
            "Usa IA", ["Todos", "Sí", "No"],
            index=["Todos", "Sí", "No"].index(st.session_state.f_ia)
        )
    with col6:
        st.session_state.f_deusto = st.selectbox(
            "Contactos", ["Todos", "Sí", "No"],
            index=["Todos", "Sí", "No"].index(st.session_state.f_deusto)
        )

    # FILTRADO
    df_show = df_main.copy()
    if st.session_state.f_nombre:
        df_show = df_show[df_show['Nombre'].astype(str).str.contains(st.session_state.f_nombre, case=False, na=False)]
    if st.session_state.f_provincia:
        df_show = df_show[df_show['provincia'].isin(st.session_state.f_provincia)]
    if st.session_state.f_patentes == "Sí": df_show = df_show[df_show['patentes'] > 0]
    elif st.session_state.f_patentes == "No": df_show = df_show[df_show['patentes'] == 0]
    if st.session_state.f_pe == "Sí": df_show = df_show[df_show['private_equity_firmas'].apply(has_private_equity)]
    elif st.session_state.f_pe == "No": df_show = df_show[~df_show['private_equity_firmas'].apply(has_private_equity)]
    if st.session_state.f_ia == "Sí": df_show = df_show[df_show['usa_inteligencia_artificial'].apply(uses_ai)]
    elif st.session_state.f_ia == "No": df_show = df_show[~df_show['usa_inteligencia_artificial'].apply(uses_ai)]
    if st.session_state.f_deusto == "Sí": df_show = df_show[df_show['Nombre'].isin(empresas_alumni_set)]
    elif st.session_state.f_deusto == "No": df_show = df_show[~df_show['Nombre'].isin(empresas_alumni_set)]

    # PAGINACIÓN
    total_items = len(df_show)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    if st.session_state.current_page >= total_pages: st.session_state.current_page = 0
    if st.session_state.current_page < 0: st.session_state.current_page = 0
    start_idx = st.session_state.current_page * ITEMS_PER_PAGE
    df_page = df_show.iloc[start_idx:start_idx + ITEMS_PER_PAGE]

    st.markdown(f"""
    <div class="results-bar">
        <div>🎯 <b>{total_items}</b> empresas encontradas</div>
        <div>Página {st.session_state.current_page + 1} de {max(1, total_pages)}</div>
    </div>
    """, unsafe_allow_html=True)

    if not df_page.empty:
        for index, row in df_page.iterrows():
            nombre = row['Nombre']
            provincia = capitalize_first_letter(safe_get_val(row, 'provincia'))
            num_contactos = 0
            if not df_alumni.empty:
                match = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.strip() == str(nombre).strip()]
                if match.empty:
                    match = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.contains(re.escape(str(nombre).strip()), case=False, na=False)]
                num_contactos = len(match)

            with st.expander(f"**{nombre}** — 📍 {provincia}"):
                pat = str(row.get('patentes', 0))
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card"><div class="metric-label">Empleados</div><div class="metric-value">{safe_get_val(row, 'numero_empleados')}</div></div>
                    <div class="metric-card"><div class="metric-label">Ventas Est.</div><div class="metric-value">{clean_number_format(safe_get_val(row, 'ventas_estimado'))}</div></div>
                    <div class="metric-card"><div class="metric-label">Patentes</div><div class="metric-value">{pat}</div></div>
                    <div class="metric-card"><div class="metric-label">Contactos</div><div class="metric-value">{num_contactos}</div></div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Ver perfil completo →", key=f"btn_{index}", use_container_width=True):
                    st.session_state.selected_empresa = row['Nombre']
                    st.session_state.page = 'detail'
                    st.session_state.scroll_needed = True
                    st.rerun()

        st.write("")
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.session_state.current_page > 0:
                if st.button("← Anterior", use_container_width=True, key="prev"):
                    st.session_state.current_page -= 1
                    st.rerun()
        with col_info:
            st.markdown(f"<p style='text-align:center;font-family:Manrope,sans-serif;font-size:0.78rem;color:#aaa;padding-top:10px;'>{st.session_state.current_page + 1} / {max(1, total_pages)}</p>", unsafe_allow_html=True)
        with col_next:
            if st.session_state.current_page < total_pages - 1:
                if st.button("Siguiente →", use_container_width=True, key="next"):
                    st.session_state.current_page += 1
                    st.rerun()
    else:
        st.markdown("<div style='text-align:center;padding:40px 20px;color:#aaa;font-family:Manrope,sans-serif;font-size:0.9rem;'>No hay empresas que coincidan con estos filtros.</div>", unsafe_allow_html=True)
