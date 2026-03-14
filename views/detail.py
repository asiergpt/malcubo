import streamlit as st
import pandas as pd
import re
from utils.helpers import (
    clean_number_format, safe_get_val, capitalize_first_letter,
    get_hierarchy_order
)

def show_detail(nombre_empresa, df_main, df_alumni):

    if st.query_params.get("nav") == "explorer":
        st.query_params.clear()
        st.session_state.page = 'explorer'
        st.rerun()

    row_data = df_main[df_main['Nombre'] == nombre_empresa]
    if row_data.empty:
        st.error("No se encontraron datos de la empresa.")
        if st.button("← Volver"):
            st.session_state.page = 'explorer'
            st.rerun()
        return

    r = row_data.iloc[0]

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main .block-container {
        background-color: #ffffff !important;
    }

    /* ---- HERO ---- */
    .det-hero {
        background: #0d0d0d;
        border-radius: 20px;
        padding: 32px 40px 48px;
        border: 1px solid rgba(255,204,102,0.15);
        margin-bottom: 28px;
        position: relative;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    .det-hero:hover {
        border-color: rgba(255,204,102,0.5);
        box-shadow: 0 0 28px rgba(255,204,102,0.1);
    }
    .det-hero-eyebrow {
        font-family: 'Manrope', sans-serif;
        font-size: 0.62rem; font-weight: 600;
        letter-spacing: 3px; text-transform: uppercase;
        color: rgba(255,204,102,0.5); margin-bottom: 10px;
    }
    .det-hero-title {
        font-family: 'Quicksand', sans-serif;
        font-size: clamp(1.4rem, 3vw, 2.2rem); font-weight: 700;
        color: transparent;
        -webkit-text-stroke: 1.3px #ffcc66;
        text-shadow: 0 0 16px rgba(255,204,102,0.2);
        line-height: 1.1; margin-bottom: 14px;
    }
    .det-hero-badges {
        display: flex; gap: 10px; flex-wrap: wrap;
    }
    .det-badge {
        font-family: 'Manrope', sans-serif;
        font-size: 0.68rem; font-weight: 600;
        padding: 4px 12px; border-radius: 20px;
        border: 1px solid rgba(255,204,102,0.25);
        color: rgba(255,204,102,0.7);
        background: rgba(255,204,102,0.06);
    }
    .det-badge.viable {
        border-color: rgba(46,125,50,0.4);
        color: #81c784; background: rgba(46,125,50,0.08);
    }
    .det-badge.dificil {
        border-color: rgba(198,40,40,0.4);
        color: #ef9a9a; background: rgba(198,40,40,0.08);
    }

    /* Botones de navegación dentro del hero */
    .det-nav {
        position: absolute; top: 18px; right: 24px;
        display: flex; gap: 8px;
    }
    .det-nav-btn {
        font-family: 'Manrope', sans-serif;
        font-size: 0.58rem; font-weight: 600;
        letter-spacing: 2px; text-transform: uppercase;
        color: rgba(255,204,102,0.5) !important;
        -webkit-text-fill-color: rgba(255,204,102,0.5);
        border: 1px solid rgba(255,204,102,0.18);
        border-radius: 6px; padding: 4px 10px;
        background: transparent; text-decoration: none !important;
        transition: all 0.2s ease; display: inline-block;
    }
    .det-nav-btn:hover {
        color: #ffcc66 !important; -webkit-text-fill-color: #ffcc66;
        border-color: rgba(255,204,102,0.55);
        background: rgba(255,204,102,0.06);
    }
    .det-nav-btn:visited, .det-nav-btn:link {
        color: rgba(255,204,102,0.5) !important;
        -webkit-text-fill-color: rgba(255,204,102,0.5);
        text-decoration: none !important;
    }

    /* ---- KPIs PRINCIPALES ---- */
    .kpi-row {
        display: flex; gap: 10px; margin-bottom: 24px;
    }
    .kpi-card {
        flex: 1; background: #f8f8f8; border: 1px solid #f0f0f0;
        border-radius: 12px; padding: 16px;
        display: flex; flex-direction: column;
    }
    .kpi-label {
        font-family: 'Manrope', sans-serif;
        font-size: 0.58rem; font-weight: 600;
        letter-spacing: 2px; text-transform: uppercase;
        color: #aaaaaa; margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.1rem; font-weight: 700;
        color: #111111;
    }

    /* ---- SECCIONES ---- */
    .det-section {
        margin-bottom: 24px;
    }
    .det-section-title {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.05rem; font-weight: 700;
        color: #111111; margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid #f0f0f0;
        display: flex; align-items: center; gap: 10px;
    }
    .det-section-title .section-icon {
        width: 28px; height: 28px; border-radius: 6px;
        background: #0d0d0d; display: flex;
        align-items: center; justify-content: center;
        font-size: 14px; flex-shrink: 0;
    }

    /* Grid de cajas de contenido */
    .det-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
    }
    .det-box {
        background: #f8f8f8; border: 1px solid #f0f0f0;
        border-radius: 12px; padding: 16px 18px;
        transition: border-color 0.2s;
    }
    .det-box:hover { border-color: rgba(255,204,102,0.35); }
    .det-box-label {
        font-family: 'Manrope', sans-serif;
        font-size: 0.60rem; font-weight: 600;
        letter-spacing: 1.5px; text-transform: uppercase;
        color: #aaaaaa; margin-bottom: 8px;
    }
    .det-box-value {
        font-family: 'Manrope', sans-serif;
        font-size: 0.88rem; font-weight: 500;
        color: #333333; line-height: 1.5;
    }

    /* Tech cards */
    .det-tech-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px; margin-top: 12px;
    }
    .det-tech-card {
        background: #0d0d0d; border: 1px solid rgba(255,204,102,0.12);
        border-radius: 12px; padding: 16px;
        text-align: center;
        transition: border-color 0.25s;
    }
    .det-tech-card:hover { border-color: rgba(255,204,102,0.4); }
    .det-tech-icon { font-size: 1.4rem; margin-bottom: 8px; }
    .det-tech-label {
        font-family: 'Manrope', sans-serif;
        font-size: 0.60rem; font-weight: 600;
        letter-spacing: 1.5px; text-transform: uppercase;
        color: rgba(255,204,102,0.45); margin-bottom: 6px;
    }
    .det-tech-value {
        font-family: 'Quicksand', sans-serif;
        font-size: 0.88rem; font-weight: 600;
        color: #ffffff;
    }

    /* Tabs alumni */
    [data-testid="stTabs"] [data-testid="stTabBar"] {
        background: transparent !important;
        border-bottom: 1.5px solid #eeeeee !important;
        gap: 0 !important;
    }
    [data-testid="stTabs"] button[role="tab"] {
        font-family: 'Quicksand', sans-serif !important;
        font-size: 0.82rem !important; font-weight: 700 !important;
        color: #aaaaaa !important; border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important; padding: 10px 18px !important;
        background: transparent !important; box-shadow: none !important;
        transition: color 0.2s !important;
    }
    [data-testid="stTabs"] button[role="tab"]:hover { color: #111111 !important; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #111111 !important; border-bottom: 2px solid #111111 !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: #111111 !important; height: 2px !important;
    }

    /* Tabla alumni */
    .alumni-table { width: 100%; border-collapse: collapse; }
    .alumni-table th {
        font-family: 'Manrope', sans-serif;
        font-size: 0.60rem; font-weight: 600;
        letter-spacing: 2px; text-transform: uppercase;
        color: #aaaaaa; text-align: left;
        padding: 8px 12px; border-bottom: 1px solid #f0f0f0;
    }
    .alumni-table td {
        font-family: 'Manrope', sans-serif;
        font-size: 0.84rem; color: #333;
        padding: 10px 12px; border-bottom: 1px solid #f8f8f8;
    }
    .alumni-table tr:last-child td { border-bottom: none; }
    .alumni-table tr:hover td { background: #fafafa; }

    /* Badges jerarquía */
    .badge-top {
        background: #0d0d0d; color: #ffcc66;
        border: 1px solid rgba(255,204,102,0.3);
        padding: 2px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600;
        font-family: 'Manrope', sans-serif;
    }
    .badge-mid {
        background: #f0f0f0; color: #555;
        border: 1px solid #e0e0e0;
        padding: 2px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600;
        font-family: 'Manrope', sans-serif;
    }
    .badge-entry {
        background: #fafafa; color: #999;
        border: 1px solid #eeeeee;
        padding: 2px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600;
        font-family: 'Manrope', sans-serif;
    }

    /* Botón volver abajo */
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
        .det-hero { padding: 28px 24px 44px; }
        .det-tech-grid { grid-template-columns: 1fr; }
        .det-nav { position: static; margin-bottom: 16px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================================
    # HERO
    # =========================================
    nombre  = safe_get_val(r, 'Nombre')
    prov    = capitalize_first_letter(safe_get_val(r, 'provincia'))
    verdict = safe_get_val(r, 'veredicto_final')
    v_raw   = safe_get_val(r, 'conclusion_sueldo_80k')
    v_text  = "Viable" if "VIABLE" in v_raw.upper() else "Difícil" if "DIFICIL" in v_raw.upper() else "Neutro"
    v_class = "viable" if "VIABLE" in v_raw.upper() else "dificil" if "DIFICIL" in v_raw.upper() else ""
    sector  = safe_get_val(r, 'SECTOR_NOMBRE')

    st.markdown(f"""
    <div class="det-hero">
        <div class="det-nav">
            <a class="det-nav-btn" href="?nav=explorer">← Explorador</a>
            <a class="det-nav-btn" href="?nav=home">⌂ Inicio</a>
        </div>
        <div class="det-hero-eyebrow">📍 {prov} &nbsp;·&nbsp; {sector}</div>
        <div class="det-hero-title">{nombre}</div>
        <div class="det-hero-badges">
            <span class="det-badge">{verdict}</span>
            <span class="det-badge {v_class}">💰 {v_text}</span>
            <span class="det-badge">📅 {safe_get_val(r, 'ano_constitucion')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Capturar navegación de los botones HTML
    if st.query_params.get("nav") == "explorer":
        st.query_params.clear()
        st.session_state.page = 'explorer'
        st.rerun()
    if st.query_params.get("nav") == "home":
        st.query_params.clear()
        st.session_state.page = 'home'
        st.rerun()

    # =========================================
    # 1. KPIs PRINCIPALES
    # =========================================
    st.markdown("""
    <div class="det-section">
        <div class="det-section-title">
            <div class="section-icon">📊</div>
            Datos Clave
        </div>
    </div>
    """, unsafe_allow_html=True)

    ventas = clean_number_format(safe_get_val(r, 'ventas_estimado'))
    empleados = clean_number_format(safe_get_val(r, 'numero_empleados'))
    patentes = str(r.get('patentes', 0))
    web = safe_get_val(r, 'web_oficial')

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Ventas Est.</div>
            <div class="kpi-value">{ventas}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Empleados</div>
            <div class="kpi-value">{empleados}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Patentes</div>
            <div class="kpi-value">{patentes}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Web</div>
            <div class="kpi-value" style="font-size:0.78rem;word-break:break-all;">{web}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # 2. SECTOR Y ACTIVIDAD
    # =========================================
    st.markdown("""
    <div class="det-section-title">
        <div class="section-icon">🏭</div>
        Sector y Actividad
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="det-grid" style="margin-bottom:24px;">
        <div class="det-box">
            <div class="det-box-label">Sector</div>
            <div class="det-box-value">{safe_get_val(r, 'SECTOR_NOMBRE')}</div>
        </div>
        <div class="det-box">
            <div class="det-box-label">Actividad Principal</div>
            <div class="det-box-value">{safe_get_val(r, 'actividad_resumen')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # 3. PROPIEDAD Y SOLVENCIA
    # =========================================
    st.markdown("""
    <div class="det-section-title">
        <div class="section-icon">🏦</div>
        Propiedad y Solvencia
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="det-grid" style="margin-bottom:24px;">
        <div class="det-box">
            <div class="det-box-label">Accionistas</div>
            <div class="det-box-value">{safe_get_val(r, 'propiedad_accionistas')}</div>
        </div>
        <div class="det-box">
            <div class="det-box-label">Private Equity</div>
            <div class="det-box-value">{safe_get_val(r, 'private_equity_firmas')}</div>
        </div>
        <div class="det-box">
            <div class="det-box-label">Financiación Pública</div>
            <div class="det-box-value">{safe_get_val(r, 'financiacion_publica_detalle')}</div>
        </div>
        <div class="det-box">
            <div class="det-box-label">Solvencia</div>
            <div class="det-box-value">{safe_get_val(r, 'solvencia_txt')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # 4. MADUREZ TECNOLÓGICA — sección negra
    # =========================================
    st.markdown("""
    <div class="det-section-title">
        <div class="section-icon">⚙️</div>
        Madurez Tecnológica
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="det-grid" style="margin-bottom:12px;">
        <div class="det-box">
            <div class="det-box-label">CTO / Responsable Tech</div>
            <div class="det-box-value">{safe_get_val(r, 'cto_actual')}</div>
        </div>
        <div class="det-box">
            <div class="det-box-label">Equipo de Ingeniería</div>
            <div class="det-box-value">{safe_get_val(r, 'tamano_ing')} personas</div>
        </div>
    </div>
    <div class="det-tech-grid" style="margin-bottom:24px;">
        <div class="det-tech-card">
            <div class="det-tech-icon">🧠</div>
            <div class="det-tech-label">IA & Automatización</div>
            <div class="det-tech-value">{safe_get_val(r, 'usa_inteligencia_artificial')}</div>
        </div>
        <div class="det-tech-card">
            <div class="det-tech-icon">☁️</div>
            <div class="det-tech-label">Infraestructura</div>
            <div class="det-tech-value">{safe_get_val(r, 'plataforma_cloud')}</div>
        </div>
        <div class="det-tech-card">
            <div class="det-tech-icon">💻</div>
            <div class="det-tech-label">Stack Técnico</div>
            <div class="det-tech-value">{safe_get_val(r, 'perfil_txt')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # 5. NETWORKING — ALUMNI
    # =========================================
    st.markdown("""
    <div class="det-section-title">
        <div class="section-icon">🤝</div>
        Networking · Alumni
    </div>
    """, unsafe_allow_html=True)

    match = pd.DataFrame()
    if not df_alumni.empty:
        match = df_alumni[
            df_alumni['nombre_matriz_einforma'].astype(str).str.strip() == str(nombre_empresa).strip()
        ]
        if match.empty:
            match = df_alumni[
                df_alumni['nombre_matriz_einforma'].astype(str).str.contains(
                    re.escape(str(nombre_empresa).strip()), case=False, na=False
                )
            ]

    if not match.empty:
        st.markdown(f"""
        <div style="background:#f0fff4;border:1px solid #c8e6c9;border-radius:10px;
                    padding:12px 16px;margin-bottom:16px;font-family:'Manrope',sans-serif;
                    font-size:0.85rem;color:#2e7d32;">
            ✅ <b>{len(match)} contactos</b> encontrados en esta empresa
        </div>
        """, unsafe_allow_html=True)

        if 'jerarquía' in match.columns:
            match = match.copy()
            match['sort_order'] = match['jerarquía'].apply(get_hierarchy_order)
            df_sorted = match.sort_values(by=['sort_order', 'Nombre']).drop('sort_order', axis=1)
        else:
            df_sorted = match.copy()

        t1, t2 = st.tabs(["Resumen por nivel", "Lista detallada"])

        with t1:
            if 'jerarquía' in df_sorted.columns:
                rows_html = ""
                for hierarchy, label, badge in [
                    ('top management', 'Top Management', 'badge-top'),
                    ('middle management', 'Middle Management', 'badge-mid'),
                    ('entry level/others', 'Entry Level', 'badge-entry'),
                ]:
                    count = len(df_sorted[
                        df_sorted['jerarquía'].astype(str).str.lower().str.strip() == hierarchy
                    ])
                    if count > 0:
                        rows_html += f"""
                        <tr>
                            <td><span class="{badge}">{label}</span></td>
                            <td style="text-align:center;font-family:'Quicksand',sans-serif;
                                       font-size:1.1rem;font-weight:700;color:#111;">{count}</td>
                        </tr>"""

                st.markdown(f"""
                <table class="alumni-table">
                    <thead><tr><th>Nivel</th><th style="text-align:center;">Cantidad</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
                """, unsafe_allow_html=True)
            else:
                st.info("No hay datos de jerarquía disponibles.")

        with t2:
            cols_view = ['Nombre', 'Cargo', 'jerarquía', 'función']
            cols_exist = [c for c in cols_view if c in df_sorted.columns]
            df_display = df_sorted[cols_exist].copy()

            if 'Nombre' in df_display.columns:
                df_display['Nombre'] = df_display['Nombre'].apply(capitalize_first_letter)

            def get_badge_html(h):
                if pd.isna(h): return '-'
                h = str(h).strip().lower()
                if "top" in h: return f'<span class="badge-top">Top</span>'
                elif "middle" in h: return f'<span class="badge-mid">Middle</span>'
                else: return f'<span class="badge-entry">Entry</span>'

            rows_html = ""
            for _, row_a in df_display.iterrows():
                nombre_a = row_a.get('Nombre', '-')
                cargo_a  = capitalize_first_letter(str(row_a.get('Cargo', '-'))) if 'Cargo' in row_a else '-'
                jer_a    = get_badge_html(row_a.get('jerarquía', '')) if 'jerarquía' in row_a else '-'
                fun_a    = capitalize_first_letter(str(row_a.get('función', '-'))) if 'función' in row_a else '-'
                rows_html += f"""
                <tr>
                    <td><b>{nombre_a}</b></td>
                    <td>{cargo_a}</td>
                    <td>{jer_a}</td>
                    <td style="color:#888;">{fun_a}</td>
                </tr>"""

            st.markdown(f"""
            <table class="alumni-table">
                <thead><tr><th>Nombre</th><th>Cargo</th><th>Nivel</th><th>Función</th></tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#f8f8f8;border:1px solid #eeeeee;border-radius:10px;
                    padding:16px;font-family:'Manrope',sans-serif;font-size:0.85rem;color:#999;
                    text-align:center;">
            No hay contactos alumni registrados en esta empresa.
        </div>
        """, unsafe_allow_html=True)

    # =========================================
    # BOTÓN VOLVER
    # =========================================
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("← Volver al Explorador", use_container_width=True):
        st.session_state.page = 'explorer'
        st.rerun()