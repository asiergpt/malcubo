import streamlit as st
import pandas as pd
import base64
import os

def get_image_base64(path):
    try:
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    except Exception:
        return ""

def btn_disabled_html(label):
    st.markdown(f"""
    <div style="
        width:100%; padding:9px 12px; border-radius:8px;
        border:1px solid #f0f0f0; background:#fafafa;
        font-family:'Manrope',sans-serif; font-size:0.78rem; font-weight:500;
        color:#cccccc; text-align:center; cursor:not-allowed; box-sizing:border-box;
    ">{label}</div>
    """, unsafe_allow_html=True)


def show_headhunters(df_headhunters, df_alumni, df_conexiones):

    current_dir = os.path.dirname(__file__)
    img_abierto = get_image_base64(os.path.join(current_dir, "..", "assets", "abierto.png"))
    img_tag = (
        f'<img src="{img_abierto}" alt="Headhunters" '
        f'style="height:80px;object-fit:contain;filter:drop-shadow(0 4px 16px rgba(255,204,102,0.2));">'
        if img_abierto else "🏹"
    )

    # ---- Captura navegación desde botón HTML del hero ----
    if st.query_params.get("nav") == "home":
        st.query_params.clear()
        st.session_state.page = 'home'
        st.rerun()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main .block-container {
        background-color: #ffffff !important;
    }

    /* ---- HERO ---- */
    .hh-hero {
        background: #0d0d0d;
        border-radius: 20px;
        padding: 32px 44px 52px 44px;
        display: flex; align-items: center; gap: 32px;
        border: 1px solid rgba(255,204,102,0.15);
        margin-bottom: 20px;
        position: relative;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .hh-hero:hover {
        border-color: rgba(255,204,102,0.6);
        box-shadow: 0 0 0 1px rgba(255,204,102,0.25), 0 0 28px rgba(255,204,102,0.12);
    }
    .hh-hero-img { flex:0 0 auto; width:90px; display:flex; align-items:center; }
    .hh-hero-text { flex:1; }
    .hh-hero-title {
        font-family:'Quicksand',sans-serif; font-size:1.9rem; font-weight:700;
        color:transparent; -webkit-text-stroke:1.4px #ffcc66;
        text-shadow:0 0 16px rgba(255,204,102,0.2); line-height:1.1; margin-bottom:10px;
    }
    .hh-hero-sub {
        font-family:'Manrope',sans-serif; font-size:0.88rem; font-weight:300;
        color:#999; line-height:1.65;
    }

    /* Botón volver — esquina inferior izquierda del hero */
    .hh-back-btn {
        position:absolute; bottom:18px; left:44px;
        font-family:'Manrope',sans-serif; font-size:0.62rem; font-weight:600;
        letter-spacing:2.5px; text-transform:uppercase;
        color:rgba(255,204,102,0.55) !important;
        border:1px solid rgba(255,204,102,0.2); border-radius:6px;
        padding:5px 12px; cursor:pointer; background:transparent;
        transition:all 0.2s ease; text-decoration:none !important; display:inline-block;
        -webkit-text-fill-color:rgba(255,204,102,0.55);
    }
    .hh-back-btn:hover {
        color:#ffcc66 !important; border-color:rgba(255,204,102,0.6);
        background:rgba(255,204,102,0.06); -webkit-text-fill-color:#ffcc66;
    }
    .hh-back-btn:visited, .hh-back-btn:link {
        color:rgba(255,204,102,0.55) !important;
        -webkit-text-fill-color:rgba(255,204,102,0.55);
        text-decoration:none !important;
    }

    /* ---- TABS ---- */
    [data-testid="stTabs"] [data-testid="stTabBar"] {
        background:transparent !important;
        border-bottom:1.5px solid #eeeeee !important;
        gap:0 !important;
    }
    [data-testid="stTabs"] button[role="tab"] {
        font-family:'Quicksand',sans-serif !important; font-size:0.82rem !important;
        font-weight:700 !important; color:#aaaaaa !important;
        border:none !important; border-bottom:2px solid transparent !important;
        border-radius:0 !important; padding:10px 18px !important;
        background:transparent !important; box-shadow:none !important;
        outline:none !important; transition:color 0.2s !important;
    }
    [data-testid="stTabs"] button[role="tab"]:hover { color:#111111 !important; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color:#111111 !important; border-bottom:2px solid #111111 !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color:#111111 !important; height:2px !important;
    }

    /* ---- EXPANSORES BLANCOS ---- */
    [data-testid="stExpander"] {
        background-color:#ffffff !important;
        border:1px solid #e8e8e8 !important;
        border-radius:12px !important; margin-bottom:10px !important;
        overflow:hidden !important; box-shadow:0 1px 4px rgba(0,0,0,0.04) !important;
        transition:border-color 0.25s, box-shadow 0.25s !important;
    }
    [data-testid="stExpander"]:hover {
        border-color:rgba(255,204,102,0.55) !important;
        box-shadow:0 4px 20px rgba(255,204,102,0.1), 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    details summary, details summary:hover, details summary:focus {
        background-color:#ffffff !important;
    }
    details [data-testid="stExpanderDetails"] { background-color:#ffffff !important; }

    details summary [data-testid="stMarkdownContainer"],
    details summary [data-testid="stMarkdownContainer"] * {
        font-family:'Quicksand',sans-serif !important; font-size:0.92rem !important;
        font-weight:700 !important; color:#111111 !important;
        -webkit-text-stroke:0px !important; text-shadow:none !important;
    }
    details summary svg { color:#cccccc !important; fill:#cccccc !important; transition:color 0.2s !important; }
    [data-testid="stExpander"]:hover details summary svg { color:#ffcc66 !important; fill:#ffcc66 !important; }

    /* ---- BOTONES ACTIVOS ---- */
    details [data-testid="stExpanderDetails"] [data-testid="stLinkButton"] > a {
        font-family:'Manrope',sans-serif !important; font-size:0.78rem !important;
        font-weight:600 !important; background:#ffffff !important; color:#333333 !important;
        border:1px solid #e0e0e0 !important; border-radius:8px !important;
        padding:8px 12px !important; width:100% !important; text-align:center !important;
        text-decoration:none !important; display:block !important;
        transition:all 0.2s ease !important; box-shadow:none !important;
    }
    details [data-testid="stExpanderDetails"] [data-testid="stLinkButton"] > a:hover {
        border-color:rgba(255,204,102,0.55) !important;
        background:rgba(255,204,102,0.04) !important; color:#111111 !important;
    }
    details [data-testid="stExpanderDetails"] [data-testid="stButton"] > button {
        font-family:'Manrope',sans-serif !important; font-size:0.78rem !important;
        font-weight:600 !important; background:#ffffff !important; color:#333333 !important;
        border:1px solid #e0e0e0 !important; border-radius:8px !important;
        padding:8px 12px !important; width:100% !important;
        transition:all 0.2s ease !important; box-shadow:none !important;
        text-transform:none !important; letter-spacing:normal !important;
    }
    details [data-testid="stExpanderDetails"] [data-testid="stButton"] > button:hover {
        border-color:rgba(255,204,102,0.55) !important;
        background:rgba(255,204,102,0.04) !important; color:#111111 !important;
    }

    @media (max-width:768px) {
        .hh-hero { flex-direction:column; padding:28px 24px 48px; text-align:center; }
        .hh-hero-img { width:70px; }
        .hh-back-btn { left:50%; transform:translateX(-50%); }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- HERO ----
    st.markdown(f"""
    <div class="hh-hero">
        <div class="hh-hero-img">{img_tag}</div>
        <div class="hh-hero-text">
            <div class="hh-hero-title">Red de Headhunters</div>
            <div class="hh-hero-sub">Conoce a las principales firmas de selección ejecutiva y boutique de talento en el territorio.</div>
        </div>
        <a class="hh-back-btn" href="?nav=home">← Inicio</a>
    </div>
    """, unsafe_allow_html=True)

    if df_headhunters.empty:
        st.warning("⚠️ No se ha encontrado el archivo 'red_headhunters.csv' o está vacío.")
        return

    col_linkedin_name = next(
        (c for c in df_headhunters.columns if str(c).strip().upper() == 'LINKEDIN'), None
    )

    categorias = sorted(df_headhunters['CATEGORÍA'].dropna().unique())
    if not categorias:
        st.info("No hay categorías definidas en los datos.")
        return

    tabs = st.tabs([cat.title() for cat in categorias])

    for i, cat in enumerate(categorias):
        with tabs[i]:
            df_cat = df_headhunters[df_headhunters['CATEGORÍA'] == cat]

            for index, row in df_cat.iterrows():
                nombre             = row.get('NOMBRE', 'Sin nombre')
                pod                = row.get('POD', '')
                ciudad             = row.get('CIUDAD', '-')
                definicion         = row.get('DEFINICION', 'Sin descripción')
                web                = row.get('WEB', '#')
                personas_clave_str = row.get('PERSONAS_CLAVE', '')

                linkedin_entidad = '#'
                if col_linkedin_name is not None and pd.notna(row[col_linkedin_name]):
                    val = str(row[col_linkedin_name]).strip()
                    if val and val.lower() not in ['nan', 'none', '-', '']:
                        linkedin_entidad = val

                # Título: Nombre — POD  📍 Ciudad
                titulo = f"**{nombre}**"
                if pd.notna(pod) and str(pod).strip() not in ['', 'nan']:
                    titulo += f" — {str(pod).strip()}"
                titulo += f"  📍 {ciudad}"

                tiene_web      = pd.notna(web) and str(web).strip() not in ['#', '', 'nan', 'none']
                tiene_linkedin = linkedin_entidad != '#'
                tiene_personas = (
                    pd.notna(personas_clave_str)
                    and str(personas_clave_str).strip() != ''
                    and str(personas_clave_str).lower() not in ['nan', 'none']
                )

                with st.expander(titulo):
                    st.markdown(
                        f"<p style='font-family:Manrope,sans-serif;font-size:0.88rem;"
                        f"color:#555;line-height:1.7;margin-bottom:16px;'>{definicion}</p>",
                        unsafe_allow_html=True
                    )

                    col_web, col_link, col_personas = st.columns(3)

                    with col_web:
                        if tiene_web:
                            st.link_button("🌐 Web Oficial", web, use_container_width=True)
                        else:
                            btn_disabled_html("🌐 Sin web")

                    with col_link:
                        if tiene_linkedin:
                            st.link_button("🏢 LinkedIn", linkedin_entidad, use_container_width=True)
                        else:
                            btn_disabled_html("🏢 Sin LinkedIn")

                    with col_personas:
                        if tiene_personas:
                            lista_personas = [p.strip() for p in str(personas_clave_str).split('|') if p.strip()]
                            if len(lista_personas) == 1:
                                st.button(
                                    f"👤 {lista_personas[0].title()}",
                                    key=f"btn_hh_single_{index}",
                                    use_container_width=True
                                )
                            else:
                                opciones = [p.title() for p in lista_personas]
                                st.selectbox(
                                    "Contactos",
                                    options=["👤 Ver contactos…"] + opciones,
                                    key=f"sel_hh_{index}",
                                    label_visibility="collapsed"
                                )
                        else:
                            btn_disabled_html("👤 Sin contactos")