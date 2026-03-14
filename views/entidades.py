import streamlit as st
import pandas as pd
import re
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

# =========================================
# MODAL DE CONEXIONES
# =========================================
@st.dialog("🤝 Red de Conexiones")
def modal_conectar(persona_clave, entidad, df_alumni, df_conexiones):
    persona_clave_display = str(persona_clave).title()
    st.markdown(f"¿Te gustaría conocer a **{persona_clave_display}** de **{entidad}**?")

    conexiones_directas = pd.DataFrame()
    if not df_conexiones.empty:
        conexiones_directas = df_conexiones[
            (df_conexiones['persona_objetivo'].astype(str).str.strip().str.lower() == str(persona_clave).strip().lower()) &
            (df_conexiones['entidad_objetivo'].astype(str).str.strip().str.lower() == str(entidad).strip().lower())
        ]

    url_persona_objetivo = "#"
    if not conexiones_directas.empty and 'persona_objetivo_linkedin' in conexiones_directas.columns:
        val_url = str(conexiones_directas.iloc[0]['persona_objetivo_linkedin']).strip()
        if val_url and val_url.lower() not in ['nan', 'none', '-', '']:
            url_persona_objetivo = val_url

    if url_persona_objetivo != "#":
        st.link_button(f"🔗 Ver perfil de {persona_clave_display}", url_persona_objetivo)

    st.divider()

    if not conexiones_directas.empty:
        st.success(f"🌟 Tienes {len(conexiones_directas)} contacto(s) que pueden introducirte.")
        for _, relacion in conexiones_directas.iterrows():
            nombre_puente_raw   = relacion.get('nombre_puente', 'Desconocido')
            nombre_puente_display = str(nombre_puente_raw).title()
            contexto            = relacion.get('contexto_relacion', 'Sin contexto especificado')
            cargo_actual        = "Profesional"
            empresa_actual      = "empresa no especificada"
            url_linkedin_puente = "#"

            if not df_alumni.empty:
                datos_puente = df_alumni[
                    df_alumni['Nombre'].astype(str).str.strip().str.lower() == str(nombre_puente_raw).strip().lower()
                ]
                if not datos_puente.empty:
                    row_p = datos_puente.iloc[0]
                    c = str(row_p.get('Cargo', '')).strip()
                    if c and c.lower() not in ['nan', '-', '']: cargo_actual = c.title()
                    matriz = str(row_p.get('nombre_matriz_einforma', '-')).strip()
                    dba    = str(row_p.get('nombre_dba', '-')).strip()
                    if matriz and matriz.lower() not in ['nan', '-', '']:
                        empresa_actual = matriz.title()
                    elif dba and dba.lower() not in ['nan', '-', '']:
                        empresa_actual = dba.title()
                    link = str(row_p.get('url_linkedin', '')).strip()
                    if link and link.lower() not in ['nan', '-', '']:
                        url_linkedin_puente = link

            st.markdown(f"""
            <div style="border:1px solid #e0e0e0;padding:15px;border-radius:10px;margin-bottom:10px;background:#fafafa;">
                <b style="color:#111;font-size:1em;">👤 {nombre_puente_display}</b><br>
                <span style="color:#777;font-size:0.85em;">💼 {cargo_actual} en {empresa_actual}</span>
                <div style="margin-top:8px;font-size:0.82em;background:#f0f0f0;padding:8px 10px;
                            border-radius:6px;border-left:3px solid #ffcc66;color:#444;">
                    💡 <b>Contexto:</b> {contexto}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if url_linkedin_puente != "#":
                st.link_button(f"💼 Ver LinkedIn de {nombre_puente_display}", url_linkedin_puente)
            st.write("")
    else:
        st.warning(f"No tienes contactos directos registrados que conozcan a {persona_clave_display}.")
        match_empresa = pd.DataFrame()
        if not df_alumni.empty:
            match_empresa = df_alumni[
                df_alumni['nombre_matriz_einforma'].astype(str).str.contains(
                    re.escape(str(entidad).strip()), case=False, na=False
                )
            ]
        if not match_empresa.empty:
            st.info(f"Sin embargo, tienes {len(match_empresa)} contacto(s) en **{entidad}** que podrían orientarte:")
            for _, row in match_empresa.iterrows():
                st.markdown(f"- 👤 **{str(row.get('Nombre','Contacto')).title()}** ({str(row.get('Cargo','Sin cargo')).title()})")


# =========================================
# BOTÓN DESHABILITADO — HTML puro, opción A
# fondo #fafafa, borde #f0f0f0, texto #cccccc
# Sin tocar st.button para evitar conflictos con styles.py
# =========================================
def btn_disabled_html(label, key):
    st.markdown(f"""
    <div style="
        width:100%; padding:9px 12px; border-radius:8px;
        border:1px solid #f0f0f0; background:#fafafa;
        font-family:'Manrope',sans-serif; font-size:0.78rem; font-weight:500;
        color:#cccccc; text-align:center; cursor:not-allowed;
        box-sizing:border-box;
    ">{label}</div>
    """, unsafe_allow_html=True)


# =========================================
# VISTA PRINCIPAL
# =========================================
def show_entidades(df_entidades, df_alumni, df_conexiones):

    current_dir = os.path.dirname(__file__)
    img_inst = get_image_base64(os.path.join(current_dir, "..", "assets", "institucional.png"))
    img_tag  = (
        f'<img src="{img_inst}" alt="Instituciones" '
        f'style="height:80px;object-fit:contain;filter:drop-shadow(0 4px 16px rgba(255,204,102,0.2));">'
        if img_inst else "🏛️"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    /* Fondo blanco */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main .block-container {
        background-color: #ffffff !important;
    }

    /* ---- HERO ---- */
    .ent-hero {
        background: #0d0d0d;
        border-radius: 20px;
        padding: 32px 44px 52px 44px;
        display: flex; align-items: center; gap: 32px;
        border: 1px solid rgba(255,204,102,0.15);
        margin-bottom: 20px;
        position: relative;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .ent-hero:hover {
        border-color: rgba(255,204,102,0.6);
        box-shadow: 0 0 0 1px rgba(255,204,102,0.25), 0 0 28px rgba(255,204,102,0.12);
    }
    .ent-hero-img { flex:0 0 auto; width:90px; display:flex; align-items:center; }
    .ent-hero-text { flex:1; }
    .ent-hero-title {
        font-family:'Quicksand',sans-serif; font-size:1.9rem; font-weight:700;
        color:transparent; -webkit-text-stroke:1.4px #ffcc66;
        text-shadow:0 0 16px rgba(255,204,102,0.2); line-height:1.1; margin-bottom:10px;
    }
    .ent-hero-sub {
        font-family:'Manrope',sans-serif; font-size:0.88rem; font-weight:300;
        color:#999; line-height:1.65;
    }

    /* Botón volver — dentro del hero, esquina inferior izquierda */
    .ent-back-btn {
        position:absolute; bottom:18px; left:44px;
        font-family:'Manrope',sans-serif; font-size:0.62rem; font-weight:600;
        letter-spacing:2.5px; text-transform:uppercase;
        color:rgba(255,204,102,0.55) !important;
        border:1px solid rgba(255,204,102,0.2); border-radius:6px;
        padding:5px 12px; cursor:pointer; background:transparent;
        transition:all 0.2s ease; text-decoration:none !important; display:inline-block;
        -webkit-text-fill-color: rgba(255,204,102,0.55);
    }
    .ent-back-btn:hover {
        color:#ffcc66 !important; border-color:rgba(255,204,102,0.6);
        background:rgba(255,204,102,0.06);
        -webkit-text-fill-color: #ffcc66;
    }
    .ent-back-btn:visited, .ent-back-btn:link {
        color:rgba(255,204,102,0.55) !important;
        -webkit-text-fill-color: rgba(255,204,102,0.55);
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
        background:transparent !important; box-shadow:none !important; outline:none !important;
        transition:color 0.2s !important;
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

    /* Título expansor — negro legible */
    details summary [data-testid="stMarkdownContainer"],
    details summary [data-testid="stMarkdownContainer"] * {
        font-family:'Quicksand',sans-serif !important; font-size:0.92rem !important;
        font-weight:700 !important; color:#111111 !important;
        -webkit-text-stroke:0px !important; text-shadow:none !important;
    }
    details summary svg { color:#cccccc !important; fill:#cccccc !important; transition:color 0.2s !important; }
    [data-testid="stExpander"]:hover details summary svg { color:#ffcc66 !important; fill:#ffcc66 !important; }

    /* ---- BOTONES ACTIVOS dentro del expansor ---- */
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

    /* Botones st.button dentro del expansor — activos */
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

    /* Selectbox contactos */
    details [data-testid="stExpanderDetails"] [data-testid="stSelectbox"] > div > div {
        font-family:'Manrope',sans-serif !important; font-size:0.78rem !important;
        border:1px solid #e0e0e0 !important; border-radius:8px !important;
        background:#ffffff !important; color:#333333 !important; box-shadow:none !important;
    }

    @media (max-width:768px) {
        .ent-hero { flex-direction:column; padding:28px 24px; text-align:center; }
        .ent-hero-img { width:70px; }
        .ent-back-btn { position:static; display:inline-block; margin-bottom:12px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- Captura del click del botón HTML del hero ----
    if st.query_params.get("nav") == "home":
        st.query_params.clear()
        st.session_state.page = 'home'
        st.rerun()

    # ---- HERO con botón volver dentro del bloque negro ----
    st.markdown(f"""
    <div class="ent-hero">
        <div class="ent-hero-img">{img_tag}</div>
        <div class="ent-hero-text">
            <div class="ent-hero-title">Instituciones Vascas</div>
            <div class="ent-hero-sub">Navega por las distintas categorías para conocer a los jugadores clave que impulsan la industria y tecnología local.</div>
        </div>
        <a class="ent-back-btn" href="?nav=home">← Inicio</a>
    </div>
    """, unsafe_allow_html=True)

    if df_entidades.empty:
        st.warning("⚠️ No se ha encontrado el archivo 'ecosistema_vasco.csv' o está vacío.")
        return

    col_linkedin_name = next(
        (col for col in df_entidades.columns if str(col).strip().upper() == 'LINKEDIN'), None
    )

    categorias = sorted(df_entidades['CATEGORÍA'].dropna().unique())
    if not categorias:
        st.info("No hay categorías definidas en los datos.")
        return

    tabs = st.tabs([cat.title() for cat in categorias])

    for i, cat in enumerate(categorias):
        with tabs[i]:
            df_cat = df_entidades[df_entidades['CATEGORÍA'] == cat]

            for index, row in df_cat.iterrows():
                nombre             = row.get('NOMBRE', 'Sin nombre')
                ciudad             = row.get('Ciudad', '-')
                definicion         = row.get('DEFINICION', 'Sin descripción')
                web                = row.get('Web', '#')
                personas_clave_str = row.get('PERSONAS_CLAVE', '')

                linkedin_entidad = '#'
                if col_linkedin_name is not None and pd.notna(row[col_linkedin_name]):
                    val = str(row[col_linkedin_name]).strip()
                    if val and val.lower() not in ['nan', 'none', '-', '']:
                        linkedin_entidad = val

                tiene_web = (
                    web and str(web).strip() not in ['#', '', 'nan', 'none']
                    and str(web).lower() not in ['nan', 'none']
                )
                tiene_linkedin = linkedin_entidad != '#'
                tiene_personas = (
                    pd.notna(personas_clave_str)
                    and str(personas_clave_str).strip() != ''
                    and str(personas_clave_str).lower() not in ['nan', 'none']
                )

                with st.expander(f"**{nombre}** — 📍 {ciudad}"):
                    st.markdown(
                        f"<p style='font-family:Manrope,sans-serif;font-size:0.88rem;"
                        f"color:#555;line-height:1.7;margin-bottom:16px;'>{definicion}</p>",
                        unsafe_allow_html=True
                    )

                    col_web, col_link, col_personas = st.columns(3)

                    # WEB
                    with col_web:
                        if tiene_web:
                            st.link_button("🌐 Web Oficial", web, use_container_width=True)
                        else:
                            btn_disabled_html("🌐 Sin web", f"noweb_{index}")

                    # LINKEDIN
                    with col_link:
                        if tiene_linkedin:
                            st.link_button("🏢 LinkedIn", linkedin_entidad, use_container_width=True)
                        else:
                            btn_disabled_html("🏢 Sin LinkedIn", f"nolink_{index}")

                    # CONTACTOS
                    with col_personas:
                        if tiene_personas:
                            lista_personas = [p.strip() for p in str(personas_clave_str).split('|') if p.strip()]
                            if len(lista_personas) == 1:
                                if st.button(f"👤 {lista_personas[0].title()}", key=f"btn_single_{index}", use_container_width=True):
                                    modal_conectar(lista_personas[0].title(), nombre, df_alumni, df_conexiones)
                            else:
                                opciones = [p.title() for p in lista_personas]
                                seleccion = st.selectbox(
                                    "Contactos",
                                    options=["👤 Ver contactos…"] + opciones,
                                    key=f"sel_{index}",
                                    label_visibility="collapsed"
                                )
                                if seleccion != "👤 Ver contactos…":
                                    modal_conectar(seleccion, nombre, df_alumni, df_conexiones)
                        else:
                            btn_disabled_html("👤 Sin contactos", f"nocontact_{index}")