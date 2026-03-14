import streamlit as st
import base64
import os

def get_image_base64(path):
    try:
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except Exception:
        return ""

def show_home():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Manrope:wght@300;400;500;600&display=swap');

    /* =========================================
       RESET Y FONDO BLANCO GLOBAL
       ========================================= */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .main .block-container {
        background-color: #ffffff !important;
    }

    /* =========================================
       HERO BLOCK + HOVER DORADO
       ========================================= */
    .hero-block {
        background-color: #0d0d0d;
        border-radius: 24px;
        padding: 52px 56px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 40px;
        margin-bottom: 40px;
        border: 1px solid rgba(255,204,102,0.15);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        overflow: hidden;
        position: relative;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        cursor: default;
    }

    .hero-block:hover {
        border-color: rgba(255,204,102,0.7) !important;
        box-shadow:
            0 0 0 1px rgba(255,204,102,0.4),
            0 0 30px rgba(255,204,102,0.2),
            0 20px 60px rgba(0,0,0,0.2) !important;
    }

    .hero-block::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 80% 50%, rgba(255,204,102,0.06) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-text {
        flex: 1;
        min-width: 0;
        position: relative;
        z-index: 1;
    }

    .hero-title {
        font-family: 'Quicksand', sans-serif;
        font-size: clamp(2.8rem, 5vw, 4.4rem);
        font-weight: 700;
        color: transparent;
        -webkit-text-stroke: 1.8px #ffcc66;
        text-shadow: 0 0 20px rgba(255, 204, 102, 0.25);
        line-height: 1.05;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }

    .hero-subtitle {
        font-family: 'Manrope', sans-serif;
        font-size: 0.95rem;
        font-weight: 300;
        color: #aaaaaa;
        line-height: 1.75;
        max-width: 420px;
    }

    .hero-divider {
        width: 48px;
        height: 2px;
        background: linear-gradient(90deg, #ffcc66, transparent);
        margin: 22px 0;
    }

    .hero-image-wrap {
        flex: 0 0 auto;
        width: clamp(160px, 26%, 260px);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 1;
    }

    .hero-image-wrap img {
        width: 100%;
        object-fit: contain;
        filter: drop-shadow(0 8px 32px rgba(255,204,102,0.2));
        transition: transform 0.5s ease, filter 0.5s ease;
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%   { transform: translateY(0px) rotate(0deg); }
        25%  { transform: translateY(-6px) rotate(1deg); }
        50%  { transform: translateY(-10px) rotate(0deg); }
        75%  { transform: translateY(-6px) rotate(-1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    .hero-image-wrap img:hover {
        transform: scale(1.06) rotate(-2deg) !important;
        animation-play-state: paused;
        filter: drop-shadow(0 12px 40px rgba(255,204,102,0.35));
    }

    /* =========================================
       TÍTULOS DE SECCIÓN
       ========================================= */
    .home-section-title {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #111111;
        letter-spacing: 0.3px;
        display: block;
        margin-bottom: 16px;
        margin-top: 4px;
    }

    /* =========================================
       EXPANSORES — hover dorado fuerte
       El truco: usamos el selector [data-testid="stExpander"]
       que es el wrapper real que Streamlit renderiza
       ========================================= */
    [data-testid="stExpander"] {
        background-color: #0d0d0d !important;
        border: 1px solid rgba(255,204,102,0.2) !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }

    [data-testid="stExpander"]:hover {
        border-color: rgba(255,204,102,0.8) !important;
        box-shadow:
            0 0 0 1px rgba(255,204,102,0.35),
            0 0 24px rgba(255,204,102,0.18),
            0 6px 20px rgba(0,0,0,0.2) !important;
    }

    details {
        background-color: #0d0d0d !important;
    }

    details summary,
    details summary:hover,
    details summary:focus {
        background-color: #0d0d0d !important;
    }

    details [data-testid="stExpanderDetails"] {
        background-color: #0d0d0d !important;
    }

    details summary [data-testid="stMarkdownContainer"],
    details summary [data-testid="stMarkdownContainer"] * {
        font-family: 'Quicksand', sans-serif !important;
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        color: transparent !important;
        -webkit-text-stroke: 0.7px rgba(255,204,102,0.85) !important;
        text-shadow: 0 0 10px rgba(255,204,102,0.2) !important;
        transition: text-shadow 0.25s ease, -webkit-text-stroke 0.25s ease !important;
        margin: 0 !important;
    }

    [data-testid="stExpander"]:hover details summary [data-testid="stMarkdownContainer"],
    [data-testid="stExpander"]:hover details summary [data-testid="stMarkdownContainer"] * {
        -webkit-text-stroke: 1px #ffcc66 !important;
        text-shadow: 0 0 20px rgba(255,204,102,0.5) !important;
    }

    details summary svg {
        color: rgba(255,204,102,0.6) !important;
        fill: rgba(255,204,102,0.6) !important;
        transition: color 0.25s ease !important;
    }

    [data-testid="stExpander"]:hover details summary svg {
        color: #ffcc66 !important;
        fill: #ffcc66 !important;
    }

    /* =========================================
       TARJETAS DE MERCADO + hover dorado fuerte
       ========================================= */
    .market-card-outer {
        display: flex;
        flex-direction: column;
        border-radius: 18px 18px 0 0;
        overflow: hidden;
        background-color: #0d0d0d;
        border: 1px solid rgba(255,204,102,0.15);
        border-bottom: none;
        transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }

    .market-card-outer:hover {
        border-color: rgba(255,204,102,0.75);
        box-shadow:
            0 0 0 1px rgba(255,204,102,0.35),
            0 0 28px rgba(255,204,102,0.2),
            0 12px 32px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }

    .market-card-img-wrap {
        height: 180px;
        background: #111111;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid rgba(255,204,102,0.07);
    }

    .market-card-img-wrap img {
        height: 72%;
        object-fit: contain;
        transition: transform 0.35s ease;
    }

    .market-card-outer:hover .market-card-img-wrap img {
        transform: scale(1.07);
    }

    .market-card-body {
        padding: 22px 20px 18px;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        text-align: center;
    }

    .market-card-title {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: transparent;
        -webkit-text-stroke: 0.8px rgba(255,204,102,0.9);
        text-shadow: 0 0 10px rgba(255,204,102,0.15);
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .market-card-title .gold-letter {
        font-size: 1.55rem;
        -webkit-text-stroke: 1.2px #ffcc66;
        text-shadow: 0 0 14px rgba(255,204,102,0.3);
    }

    .market-card-desc {
        font-family: 'Manrope', sans-serif;
        color: #888888;
        font-size: 0.84rem;
        line-height: 1.65;
        flex-grow: 1;
    }

    /* ---- BOTONES pegados a tarjeta ---- */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] div[data-testid="stButton"] {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        display: block !important;
    }

    /* Anular estilos de enlace en botones HTML de Empresas/Personas */
    a[href*="goto"] {
        text-decoration: none !important;
        outline: none !important;
        -webkit-text-fill-color: #ffcc66 !important;
    }
    a[href*="goto"]:visited,
    a[href*="goto"]:link,
    a[href*="goto"]:focus {
        text-decoration: none !important;
        -webkit-text-fill-color: #ffcc66 !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] div[data-testid="stButton"] > button {
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
        padding: 15px 10px !important;
        min-height: 52px !important;
        transition: all 0.25s ease !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] div[data-testid="stButton"] > button:hover {
        background-color: #ffcc66 !important;
        color: #0d0d0d !important;
        letter-spacing: 4px !important;
        border-color: #ffcc66 !important;
        box-shadow:
            0 0 20px rgba(255,204,102,0.35),
            0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* Tarjeta 3 — dos botones */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child div[data-testid="stHorizontalBlock"] > div:first-child div[data-testid="stButton"] > button {
        border-radius: 0 0 0 18px !important;
        border-right: 1px solid rgba(255,204,102,0.12) !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stButton"] > button {
        border-radius: 0 0 18px 0 !important;
        border-left: none !important;
    }

    /* =========================================
       NOTA METODOLÓGICA
       ========================================= */
    .nota-box {
        background: #fafafa;
        border-left: 3px solid #ffcc66;
        border-radius: 10px;
        padding: 22px 28px;
        margin-top: 40px;
        border: 1px solid rgba(255,204,102,0.15);
        border-left: 3px solid #ffcc66;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .nota-box:hover {
        border-color: rgba(255,204,102,0.6);
        box-shadow:
            0 0 0 1px rgba(255,204,102,0.25),
            0 0 20px rgba(255,204,102,0.12);
    }

    .nota-box p {
        font-family: 'Manrope', sans-serif;
        font-size: 0.86rem;
        color: #555555;
        line-height: 1.7;
        margin: 0;
    }

    .nota-box strong { color: #a07c2a; }

    /* =========================================
       RESPONSIVE
       ========================================= */
    @media (max-width: 768px) {
        .hero-block { flex-direction: column; padding: 36px 28px; text-align: center; }
        .hero-image-wrap { width: 55%; }
        .hero-subtitle { max-width: 100%; }
        .hero-divider { margin-left: auto; margin-right: auto; }

        /* Las 3 tarjetas se apilan en móvil */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: 100% !important; min-width: 100% !important;
        }

        /* EXCEPCIÓN: los dos botones Empresas/Personas se mantienen en fila */
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            gap: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: 50% !important; min-width: 50% !important; flex: 1 1 50% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================================
    # 1. HERO BLOCK
    # =========================================
    current_dir = os.path.dirname(__file__)
    img_hero = get_image_base64(os.path.join(current_dir, "..", "assets", "malcubo-removebg-preview.png"))
    img_tag = f'<img src="{img_hero}" alt="M al cubo">' if img_hero else ""

    # Abrimos el wrapper .home-page para aislar los estilos de styles.py
    st.markdown('<div class="home-page">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hero-block">
        <div class="hero-text">
            <div class="hero-title">M al cubo</div>
            <div class="hero-divider"></div>
            <p class="hero-subtitle">Un producto estratégico para penetrar el mercado ejecutivo vasco. Conoce el tejido, mapea las conexiones y activa tu red.</p>
            <a href="https://asierdorronsoro.streamlit.app/" target="_blank" style="
                display: inline-flex;
                align-items: center;
                gap: 8px;
                margin-top: 20px;
                font-family: 'Manrope', sans-serif;
                font-size: 0.65rem;
                font-weight: 600;
                letter-spacing: 2.5px;
                text-transform: uppercase;
                color: rgba(255,204,102,0.65) !important;
                -webkit-text-fill-color: rgba(255,204,102,0.65);
                border: 1px solid rgba(255,204,102,0.25);
                border-radius: 8px;
                padding: 8px 16px;
                text-decoration: none !important;
                transition: all 0.25s ease;
                background: transparent;
            "
            onmouseover="this.style.borderColor='rgba(255,204,102,0.7)';this.style.background='rgba(255,204,102,0.07)';this.style.webkitTextFillColor='#ffcc66';"
            onmouseout="this.style.borderColor='rgba(255,204,102,0.25)';this.style.background='transparent';this.style.webkitTextFillColor='rgba(255,204,102,0.65)';"
            >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                          stroke="#ffcc66" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Inicio
            </a>
        </div>
        <div class="hero-image-wrap">
            {img_tag}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # 2. EXPANSORES METODOLÓGICOS
    # =========================================
    st.markdown('<span class="home-section-title">¿Por qué es necesario?</span>', unsafe_allow_html=True)

    with st.expander("#1 — LinkedIn es un canal ineficaz para roles ejecutivos"):
        st.markdown("""
        <p style='color:#bbbbbb; font-family: Manrope, sans-serif; font-size:0.93rem; line-height:1.75; text-align:justify;'>
            A diferencia de los grandes hubs corporativos europeos (Madrid, Londres, Ginebra, etc), en Euskadi el canal digital
            se utiliza casi en exclusiva para posiciones entry/middle-management.
            <span style='color:#ffcc66; font-weight:600;'>El acceso a la alta dirección exige penetrar un círculo
            exclusivo dominado por la confianza y las referencias.</span>
        </p>
        """, unsafe_allow_html=True)

    with st.expander("#2 — El tejido empresarial vasco es complejo y fragmentado"):
        st.markdown("""
        <p style='color:#bbbbbb; font-family: Manrope, sans-serif; font-size:0.93rem; line-height:1.75; text-align:justify;'>
            Se sustenta en un potente grupo de empresas tractoras y, sobre todo, en una masiva red de industria mediana y familiar
            de alto rendimiento. Este ecosistema ofrece un volumen ingente de oportunidades que, por su atomización,
            <span style='color:#ffcc66; font-weight:600;'>exigen un estudio de mayor profundidad para responder a la pregunta
            estratégica: ¿Dónde quiero realmente trabajar?</span>
        </p>
        """, unsafe_allow_html=True)

    with st.expander("#3 — El sello de gigantes corporativos requiere traducción local"):
        st.markdown("""
        <p style='color:#bbbbbb; font-family: Manrope, sans-serif; font-size:0.93rem; line-height:1.75; text-align:justify;'>
            <span style='color:#ffcc66; font-weight:600;'>El prestigio de firmas líderes (BCG, Amazon, McKinsey)
            no actúa como aval automático en el ecosistema local.</span>
            A menudo se desconoce la excelencia y la exigente "escuela de negocio" que hay detrás de estas trayectorias.
            Lo que en otros hubs globales tiene un efecto multiplicador —donde unos pocos años equivalen a una década—,
            en Euskadi requiere de un interlocutor que traduzca ese valor.
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================
    # 3. TARJETAS DE MERCADO
    # =========================================
    st.markdown('<span class="home-section-title">Los tres mercados</span>', unsafe_allow_html=True)

    img_inst    = get_image_base64(os.path.join(current_dir, "..", "assets", "institucional.png"))
    img_abierto = get_image_base64(os.path.join(current_dir, "..", "assets", "abierto.png"))
    img_oculto  = get_image_base64(os.path.join(current_dir, "..", "assets", "oculto.png"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="market-card-outer">
            <div class="market-card-img-wrap"><img src="{img_inst}" alt="Mercado Institucional"></div>
            <div class="market-card-body">
                <div class="market-card-title"><span class="gold-letter">M</span>ercado Institucional</div>
                <div class="market-card-desc">El mercado de retos y proyectos estratégicos articulado por el ecosistema público-privado vasco.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explorar Instituciones", key="btn_inst", use_container_width=True):
            st.session_state.page = 'entidades'
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class="market-card-outer">
            <div class="market-card-img-wrap"><img src="{img_abierto}" alt="Mercado Abierto"></div>
            <div class="market-card-body">
                <div class="market-card-title"><span class="gold-letter">M</span>ercado Abierto</div>
                <div class="market-card-desc">El mercado de procesos formales que las compañías delegan a headhunters para encontrar talento.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explorar Headhunters", key="btn_head", use_container_width=True):
            st.session_state.page = 'headhunters'
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class="market-card-outer">
            <div class="market-card-img-wrap"><img src="{img_oculto}" alt="Mercado Oculto"></div>
            <div class="market-card-body">
                <div class="market-card-title"><span class="gold-letter">M</span>ercado Oculto</div>
                <div class="market-card-desc">El mercado de posiciones críticas previo a su publicación, accesible solo por referencias y reputación.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Empresas", key="btn_emp", use_container_width=True):
                st.session_state.page = 'explorer'
                st.rerun()
        with b2:
            if st.button("Personas", key="btn_pers", use_container_width=True):
                st.session_state.page = 'personas'
                st.rerun()

    # =========================================
    # 4. NOTA METODOLÓGICA
    # =========================================
    st.markdown("""
    <div class="nota-box">
        <p>
            <strong>📌 Nota metodológica:</strong>&nbsp;
            Los datos provienen de inteligencia artificial e información pública (prensa, rankings, webs corporativas).
            Aunque procuro máxima precisión, algunos datos pueden estar sujetos a cambios o ser inexactos.
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    # ↑ El </div> extra cierra el .home-page wrapper
