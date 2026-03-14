import streamlit as st
import pandas as pd
import math
import base64
import os
from utils.helpers import (
    clean_number_format, safe_get_val, capitalize_first_letter,
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

def get_empresa_name(row):
    matriz = safe_get_val(row, 'nombre_matriz_einforma', default=None)
    if matriz and matriz != "-":
        return matriz
    return safe_get_val(row, 'nombre_dba', default="-")

def btn_disabled_html(label):
    st.markdown(f"""
    <div style="
        width:100%; padding:9px 12px; border-radius:8px;
        border:1px solid #f0f0f0; background:#fafafa;
        font-family:'Manrope',sans-serif; font-size:0.78rem; font-weight:500;
        color:#cccccc; text-align:center; cursor:not-allowed; box-sizing:border-box;
    ">{label}</div>
    """, unsafe_allow_html=True)


def show_personas(df_main, df_alumni):

    if st.query_params.get("nav") == "home":
        st.query_params.clear()
        st.session_state.page = 'home'
        st.rerun()

    current_dir = os.path.dirname(__file__)
    img_personas = get_image_base64(os.path.join(current_dir, "..", "assets", "oculto.png"))
    img_tag = (
        f'<img src="{img_personas}" alt="Personas" '
        f'style="height:80px;object-fit:contain;filter:drop-shadow(0 4px 16px rgba(255,204,102,0.2));">'
        if img_personas else "👤"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main .block-container {
        background-color: #ffffff !important;
    }

    /* ---- HERO ---- */
    .per-hero {
        background: #0d0d0d;
        border-radius: 20px;
        padding: 32px 44px 52px 44px;
        display: flex; align-items: center; gap: 32px;
        border: 1px solid rgba(255,204,102,0.15);
        margin-bottom: 20px;
        position: relative;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .per-hero:hover {
        border-color: rgba(255,204,102,0.6);
        box-shadow: 0 0 0 1px rgba(255,204,102,0.25), 0 0 28px rgba(255,204,102,0.12);
    }
    .per-hero-img { flex:0 0 auto; width:90px; display:flex; align-items:center; }
    .per-hero-text { flex:1; }
    .per-hero-title {
        font-family:'Quicksand',sans-serif; font-size:1.9rem; font-weight:700;
        color:transparent; -webkit-text-stroke:1.4px #ffcc66;
        text-shadow:0 0 16px rgba(255,204,102,0.2); line-height:1.1; margin-bottom:10px;
    }
    .per-hero-sub {
        font-family:'Manrope',sans-serif; font-size:0.88rem; font-weight:300;
        color:#999; line-height:1.65;
    }
    .per-back-btn {
        position:absolute; bottom:18px; left:44px;
        font-family:'Manrope',sans-serif; font-size:0.62rem; font-weight:600;
        letter-spacing:2.5px; text-transform:uppercase;
        color:rgba(255,204,102,0.55) !important;
        -webkit-text-fill-color:rgba(255,204,102,0.55);
        border:1px solid rgba(255,204,102,0.2); border-radius:6px;
        padding:5px 12px; background:transparent;
        text-decoration:none !important; display:inline-block;
        transition:all 0.2s ease;
    }
    .per-back-btn:hover {
        color:#ffcc66 !important; -webkit-text-fill-color:#ffcc66;
        border-color:rgba(255,204,102,0.6); background:rgba(255,204,102,0.06);
    }
    .per-back-btn:visited, .per-back-btn:link {
        color:rgba(255,204,102,0.55) !important;
        -webkit-text-fill-color:rgba(255,204,102,0.55);
        text-decoration:none !important;
    }

    /* ---- FILTROS ---- */
    .per-filter-block {
        background: #f8f8f8; border-radius: 14px;
        padding: 18px 20px; margin-bottom: 20px;
        border: 1px solid #eeeeee;
    }
    .per-filter-title {
        font-family: 'Manrope', sans-serif;
        font-size: 0.60rem; font-weight: 600;
        letter-spacing: 2.5px; text-transform: uppercase;
        color: #aaaaaa; margin-bottom: 14px;
        display: flex; align-items: center; gap: 7px;
    }
    .per-filter-block [data-testid="stWidgetLabel"] p {
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.65rem !important; font-weight: 600 !important;
        letter-spacing: 1px !important; text-transform: uppercase !important;
        color: #999999 !important;
    }
    .per-filter-block [data-testid="stTextInput"] input,
    .per-filter-block [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        font-family: 'Manrope', sans-serif !important;
        color: #333333 !important;
    }
    .per-filter-block [data-testid="stTextInput"] input:focus,
    .per-filter-block [data-baseweb="select"] > div:focus-within {
        border-color: rgba(255,204,102,0.5) !important;
        box-shadow: 0 0 0 1px rgba(255,204,102,0.12) !important;
    }
    /* Botón limpiar dentro del bloque filtros */
    .per-filter-block [data-testid="stButton"] > button {
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.72rem !important; font-weight: 600 !important;
        background: #ffffff !important; color: #888888 !important;
        border: 1px solid #e0e0e0 !important; border-radius: 8px !important;
        box-shadow: none !important; transition: all 0.2s ease !important;
        text-transform: none !important; letter-spacing: normal !important;
    }
    .per-filter-block [data-testid="stButton"] > button:hover {
        border-color: rgba(255,204,102,0.4) !important;
        color: #555 !important;
    }

    /* ---- BARRA RESULTADOS ---- */
    .results-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 16px; background: #f8f8f8;
        border-radius: 8px; margin-bottom: 14px;
        font-family: 'Manrope', sans-serif; font-size: 0.82rem; color: #666;
    }
    .results-bar b { color: #111; }

    /* ---- EXPANSORES BLANCOS ---- */
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

    /* ---- BOTONES DENTRO DEL EXPANSOR ---- */
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

    /* ---- INFO CARD DENTRO DEL EXPANSOR ---- */
    .persona-info {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 10px; margin-bottom: 14px;
    }
    .persona-info-item {
        background: #f8f8f8; border: 1px solid #f0f0f0;
        border-radius: 8px; padding: 10px 14px;
    }
    .persona-info-label {
        font-family: 'Manrope', sans-serif;
        font-size: 0.58rem; font-weight: 600;
        letter-spacing: 1.5px; text-transform: uppercase;
        color: #aaaaaa; margin-bottom: 4px;
    }
    .persona-info-value {
        font-family: 'Manrope', sans-serif;
        font-size: 0.84rem; font-weight: 500; color: #333;
    }

    /* Paginación */
    [data-testid="stButton"] > button {
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.78rem !important; font-weight: 600 !important;
        background: #ffffff !important; color: #333333 !important;
        border: 1px solid #e0e0e0 !important; border-radius: 8px !important;
        transition: all 0.2s ease !important; box-shadow: none !important;
        text-transform: none !important; letter-spacing: normal !important;
    }
    [data-testid="stButton"] > button:hover {
        border-color: rgba(255,204,102,0.55) !important;
        background: rgba(255,204,102,0.04) !important; color: #111 !important;
    }

    @media (max-width: 768px) {
        .per-hero { flex-direction: column; padding: 28px 24px 48px; text-align: center; }
        .per-hero-img { width: 70px; }
        .per-back-btn { left: 50%; transform: translateX(-50%); }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- HERO ----
    st.markdown(f"""
    <div class="per-hero">
        <div class="per-hero-img">{img_tag}</div>
        <div class="per-hero-text">
            <div class="per-hero-title">Buscar Profesionales</div>
            <div class="per-hero-sub">Encuentra a los profesionales clave en tu base de datos de contactos.</div>
        </div>
        <a class="per-back-btn" href="?nav=home">← Inicio</a>
    </div>
    """, unsafe_allow_html=True)

    if df_alumni.empty:
        st.markdown("""
        <div style="text-align:center;padding:40px;color:#aaa;
                    font-family:'Manrope',sans-serif;font-size:0.9rem;">
            No hay datos de contactos disponibles.
        </div>
        """, unsafe_allow_html=True)
        return

    # ---- FILTROS ----

    # Fila 1
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.f_personas_nombre = st.text_input(
            "Nombre", value=st.session_state.f_personas_nombre,
            placeholder="Buscar por nombre..."
        )
    with col2:
        st.session_state.f_personas_empresa = st.text_input(
            "Empresa", value=st.session_state.f_personas_empresa,
            placeholder="Buscar por empresa..."
        )

    # Fila 2
    col3, col4, col5, col6 = st.columns(4)
    with col3:
        if not df_main.empty:
            provs = sorted([str(p) for p in df_main['provincia'].dropna().unique() if str(p).strip()])
            vals_p = [v for v in st.session_state.get('f_personas_provincia', []) if v in provs]
            st.session_state.f_personas_provincia = st.multiselect("Provincia", provs, default=vals_p)

    with col4:
        if 'jerarquía' in df_alumni.columns:
            jerarquias = sorted([str(j).strip() for j in df_alumni['jerarquía'].dropna().unique()
                                 if str(j).strip().lower() not in ['nan', '-', '']])
        else:
            jerarquias = []
        vals_j = [v for v in st.session_state.get('f_personas_jerarquia', []) if v in jerarquias]
        st.session_state.f_personas_jerarquia = st.multiselect("Nivel", jerarquias, default=vals_j)

    with col5:
        if 'función' in df_alumni.columns:
            funciones = sorted([str(f).strip() for f in df_alumni['función'].dropna().unique()
                                if str(f).strip().lower() not in ['nan', '-', '']])
        else:
            funciones = []
        vals_f = [v for v in st.session_state.get('f_personas_funcion', []) if v in funciones]
        st.session_state.f_personas_funcion = st.multiselect("Función", funciones, default=vals_f)

    with col6:
        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Limpiar", use_container_width=True, key="limpiar_filtros"):
            st.session_state.f_personas_nombre = ""
            st.session_state.f_personas_empresa = ""
            st.session_state.f_personas_provincia = []
            st.session_state.f_personas_jerarquia = []
            st.session_state.f_personas_funcion = []
            st.session_state.current_page_personas = 0
            st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ---- FILTRADO ----
    df_personas = df_alumni.copy()
    df_personas['empresa_filtro'] = df_personas.apply(
        lambda row: (
            row['nombre_matriz_einforma']
            if pd.notna(row['nombre_matriz_einforma'])
            and str(row['nombre_matriz_einforma']).strip() not in ['', 'nan', '-']
            else row.get('nombre_dba', '-')
        ), axis=1
    )

    if st.session_state.f_personas_nombre:
        df_personas = df_personas[
            df_personas['Nombre'].astype(str).str.contains(
                st.session_state.f_personas_nombre, case=False, na=False
            )
        ]
    if st.session_state.f_personas_empresa:
        df_personas = df_personas[
            df_personas['empresa_filtro'].astype(str).str.contains(
                st.session_state.f_personas_empresa, case=False, na=False
            )
        ]
    if st.session_state.f_personas_provincia:
        empresas_prov = df_main[
            df_main['provincia'].isin(st.session_state.f_personas_provincia)
        ]['Nombre'].tolist()
        df_personas = df_personas[df_personas['empresa_filtro'].isin(empresas_prov)]
    if st.session_state.f_personas_jerarquia:
        df_personas = df_personas[
            df_personas['jerarquía'].astype(str).str.strip().isin(st.session_state.f_personas_jerarquia)
        ]
    if st.session_state.f_personas_funcion:
        df_personas = df_personas[
            df_personas['función'].astype(str).str.strip().isin(st.session_state.f_personas_funcion)
        ]

    # ---- PAGINACIÓN ----
    total_items = len(df_personas)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    if st.session_state.current_page_personas >= total_pages:
        st.session_state.current_page_personas = 0
    if st.session_state.current_page_personas < 0:
        st.session_state.current_page_personas = 0

    start_idx = st.session_state.current_page_personas * ITEMS_PER_PAGE
    df_page = df_personas.iloc[start_idx:start_idx + ITEMS_PER_PAGE]

    st.markdown(f"""
    <div class="results-bar">
        <div>🎯 <b>{total_items}</b> profesionales encontrados</div>
        <div>Página {st.session_state.current_page_personas + 1} de {max(1, total_pages)}</div>
    </div>
    """, unsafe_allow_html=True)

    # ---- TARJETAS ----
    if not df_page.empty:
        for index, row in df_page.iterrows():
            nombre    = capitalize_first_letter(safe_get_val(row, 'Nombre'))
            empresa   = get_empresa_name(row)
            jerarquia = safe_get_val(row, 'jerarquía')
            funcion   = capitalize_first_letter(safe_get_val(row, 'función'))
            provincia = "-"

            if empresa != "-":
                emp_data = df_main[df_main['Nombre'] == empresa]
                if not emp_data.empty:
                    provincia = capitalize_first_letter(safe_get_val(emp_data.iloc[0], 'provincia'))

            # Badge jerarquía
            h = str(jerarquia).strip().lower()
            if "top" in h:
                badge = f'<span style="background:#0d0d0d;color:#ffcc66;border:1px solid rgba(255,204,102,0.3);padding:2px 10px;border-radius:20px;font-size:0.7rem;font-family:Manrope,sans-serif;font-weight:600;">Top</span>'
            elif "middle" in h:
                badge = f'<span style="background:#f0f0f0;color:#555;border:1px solid #e0e0e0;padding:2px 10px;border-radius:20px;font-size:0.7rem;font-family:Manrope,sans-serif;font-weight:600;">Middle</span>'
            elif jerarquia and jerarquia != "-":
                badge = f'<span style="background:#fafafa;color:#999;border:1px solid #eee;padding:2px 10px;border-radius:20px;font-size:0.7rem;font-family:Manrope,sans-serif;font-weight:600;">Entry</span>'
            else:
                badge = ""

            with st.expander(f"**{nombre}** — 🏢 {empresa}"):
                st.markdown(f"""
                <div class="persona-info">
                    <div class="persona-info-item">
                        <div class="persona-info-label">Empresa</div>
                        <div class="persona-info-value">{empresa}</div>
                    </div>
                    <div class="persona-info-item">
                        <div class="persona-info-label">Provincia</div>
                        <div class="persona-info-value">{provincia}</div>
                    </div>
                    <div class="persona-info-item">
                        <div class="persona-info-label">Función</div>
                        <div class="persona-info-value">{funcion}</div>
                    </div>
                    <div class="persona-info-item">
                        <div class="persona-info-label">Nivel</div>
                        <div class="persona-info-value">{badge if badge else jerarquia}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if empresa != "-" and empresa in df_main['Nombre'].values:
                    if st.button(
                        f"Ver perfil de {empresa} →",
                        key=f"btn_p_{index}",
                        use_container_width=True
                    ):
                        st.session_state.selected_empresa = empresa
                        st.session_state.page = 'detail'
                        st.session_state.scroll_needed = True
                        st.rerun()
                else:
                    btn_disabled_html("Sin perfil de empresa")

        # ---- PAGINACIÓN ----
        st.write("")
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.session_state.current_page_personas > 0:
                if st.button("← Anterior", use_container_width=True, key="prev_p"):
                    st.session_state.current_page_personas -= 1
                    st.rerun()
        with col_info:
            st.markdown(
                f"<p style='text-align:center;font-family:Manrope,sans-serif;"
                f"font-size:0.78rem;color:#aaa;padding-top:10px;'>"
                f"{st.session_state.current_page_personas + 1} / {max(1, total_pages)}</p>",
                unsafe_allow_html=True
            )
        with col_next:
            if st.session_state.current_page_personas < total_pages - 1:
                if st.button("Siguiente →", use_container_width=True, key="next_p"):
                    st.session_state.current_page_personas += 1
                    st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;color:#aaa;
                    font-family:'Manrope',sans-serif;font-size:0.9rem;">
            No hay profesionales que coincidan con estos filtros.
        </div>
        """, unsafe_allow_html=True)