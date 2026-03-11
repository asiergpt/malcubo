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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600&family=Manrope:wght@300;400;500;600;800&display=swap');

[data-testid="stAppViewContainer"], .main { background-color: #ffffff !important; }

/* ---- BLOQUE ACORDEONES — FUENTE ACTUALIZADA ---- */
.origen-black-block {
    background-color: #0d0d0d;
    border-radius: 20px;
    padding: 60px 50px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.2);
    max-width: 1000px;
    margin: 80px auto 60px auto;
}

.elegant-header-dark {
    font-family: 'Manrope', sans-serif;  
    color: #ffffff;
    font-size: 3rem;  
    text-align: center;
    margin-bottom: 50px;
    font-weight: 600;  
    letter-spacing: 0.5px;  
}

.elegant-header-dark i { 
    color: #bfa15a; 
    font-style: italic;
}

.step-item {
    background: #181818;
    border: 1px solid #282828;
    border-radius: 12px;
    margin-bottom: 20px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.step-item:hover { 
    border-color: #bfa15a; 
}

.step-summary {
    display: flex;
    align-items: stretch;
    cursor: pointer;
    list-style: none;
}

.step-summary::-webkit-details-marker { 
    display: none; 
}

.step-num {
    background: rgba(191, 161, 90, 0.1);
    color: #bfa15a;
    font-family: 'Manrope', sans-serif;  
    font-weight: 700;
    font-size: 1.8rem;
    width: 80px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid #282828;
}

.step-title {
    color: #ffffff;
    font-family: 'Manrope', sans-serif;  
    font-weight: 600;  
    font-size: 1.3rem;  
    padding: 25px;
    display: flex;
    align-items: center;
    flex-grow: 1;
    letter-spacing: 0.3px;
}

.step-body {
    padding: 10px 40px 30px 110px;
    color: #cccccc;
    font-size: 1rem;  
    line-height: 1.8;  
    font-family: 'Manrope', sans-serif;  
    text-align: justify;
}

.neon-highlight { 
    color: #bfa15a; 
    font-weight: 700;  
}

/* ================================================
   LAYOUT COLUMNAS PRINCIPALES
   ================================================ */
[data-testid="stHorizontalBlock"] {
    max-width: 1080px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    align-items: stretch !important;
    gap: 24px !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    display: flex !important;
    flex-direction: column !important;
    padding: 0 !important;
    min-width: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div > [data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;
    gap: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div
> [data-testid="stVerticalBlock"] > div {
    margin: 0 !important;
    padding: 0 !important;
}

/* ================================================
   CARD OUTER
   ================================================ */
.market-card-outer {
    display: flex;
    flex-direction: column;
    border-radius: 16px 16px 0 0;
    overflow: hidden;
    box-shadow: 1px 0 0 0 #ececec,
               -1px 0 0 0 #ececec,
                0 -1px 0 0 #ececec,
                0 15px 40px rgba(0,0,0,0.08);
    border: none;
    transition: box-shadow 0.4s ease, transform 0.4s ease;
    background: #ffffff;
}
.market-card-outer:hover {
    transform: translateY(-4px);
    box-shadow: 0 25px 55px rgba(191, 161, 90, 0.18),
                0 0 0 1px rgba(191, 161, 90, 0.35);
}
.market-card-img-wrap {
    width: 100%;
    height: 200px;
    flex-shrink: 0;
    overflow: hidden;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
}
.market-card-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 18px;
    transition: transform 0.4s ease;
}
.market-card-outer:hover .market-card-img-wrap img {
    transform: scale(1.06);
}
.market-card-body {
    padding: 22px 22px 20px 22px;
    flex: 1;
    display: flex;
    flex-direction: column;
}
.market-card-title {
    font-family: 'Cormorant Garamond', serif;
    color: #111111;
    font-weight: 600;
    font-size: 1.65rem;
    margin-bottom: 10px;
    line-height: 1.2;
    flex-shrink: 0;
}
.market-card-title span {
    color: #bfa15a;
    font-size: 2rem;
}
.market-card-desc {
    font-family: 'Manrope', sans-serif;
    font-size: 0.88rem;
    color: #666666;
    line-height: 1.7;
    text-align: justify;
    flex: 1;
}

/* ================================================
   BOTONES NEGROS — SELECTOR AMPLIO
   ================================================ */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]
[data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    display: block !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]
[data-testid="stButton"] > button {
    width: 100% !important;
    background-color: #0d0d0d !important;
    color: #bfa15a !important;
    border: none !important;
    border-top: 1px solid #1a1a1a !important;
    border-radius: 0 0 14px 14px !important;
    font-family: 'Manrope', sans-serif !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    font-size: 0.68rem !important;
    padding: 15px 18px !important;
    cursor: pointer !important;
    min-height: 0 !important;
    height: auto !important;
    line-height: 1 !important;
    box-shadow: 1px 0 0 0 #1a1a1a,
               -1px 0 0 0 #1a1a1a,
                0 1px 0 0 #1a1a1a !important;
    transition: background-color 0.3s ease, color 0.3s ease, letter-spacing 0.3s ease, box-shadow 0.3s ease !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]
[data-testid="stButton"] > button:hover {
    background-color: #bfa15a !important;
    color: #0d0d0d !important;
    letter-spacing: 4px !important;
    box-shadow: 0 -4px 20px rgba(191, 161, 90, 0.3),
                1px 0 0 0 rgba(191,161,90,0.5),
               -1px 0 0 0 rgba(191,161,90,0.5),
                0 1px 0 0 rgba(191,161,90,0.5) !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]
[data-testid="stButton"] > button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* ================================================
   CARD 3 — DOBLE BTN
   ================================================ */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child
[data-testid="stButton"] > button {
    border-radius: 0 0 0 14px !important;
    border-right: 1px solid #2a2a2a !important;
    box-shadow: -1px 0 0 0 #1a1a1a, 0 1px 0 0 #1a1a1a !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
[data-testid="stButton"] > button {
    border-radius: 0 0 14px 0 !important;
    box-shadow: 1px 0 0 0 #1a1a1a, 0 1px 0 0 #1a1a1a !important;
}

/* ================================================
   MÓVIL / RESPONSIVE (CORREGIDO)
   ================================================ */
@media (max-width: 768px) {
    /* Ajustes generales de bloque negro */
    .origen-black-block {
        padding: 30px 20px;
        margin: 30px auto 40px auto;
        border-radius: 12px;
    }
    .elegant-header-dark {
        font-size: 2rem;
        margin-bottom: 30px;
    }
    
    /* Ajustes de acordeones (quitar sangrías masivas) */
    .step-num {
        width: 60px;
        font-size: 1.4rem;
    }
    .step-title {
        font-size: 1.1rem;
        padding: 15px;
    }
    .step-body {
        padding: 15px 20px 25px 20px;
        font-size: 0.95rem;
    }
    
    /* 1. Apilar las 3 tarjetas principales */
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 20px !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 100% !important;
        min-width: 100% !important;
    }
    
    /* 2. EXCEPCIÓN: Mantener los dos botones finales lado a lado */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child [data-testid="stHorizontalBlock"] {
        flex-direction: row !important; 
        gap: 0 !important;
    }
    
    /* Forzar a que cada botón (Empresas / Personas) ocupe exactamente el 50% */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        width: 50% !important;
        min-width: 50% !important;
        flex: 1 1 50% !important;
    }
    
    .market-card-img-wrap {
        height: 160px;
    }
}
</style>
""", unsafe_allow_html=True)

    # --- 1. POSTER PRINCIPAL ---
    img_path = os.path.join("assets", "hero_total.png")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

    # --- 2. ACORDEONES ---
    st.markdown("""
<div class="origen-black-block">
    <div class="elegant-header-dark">&iquest;Por qu&eacute; es <i>necesario</i>?</div>
    <details class="step-item">
        <summary class="step-summary">
            <div class="step-num">#1</div>
            <div class="step-title">LinkedIn es un canal ineficaz para roles ejecutivos</div>
        </summary>
        <div class="step-body">
            A diferencia de los grandes hubs corporativos europeos (Madrid, Londres, Ginebra, etc), en Euskadi el canal digital se utiliza casi en exclusiva para posiciones entry/middle-management.
            <span class="neon-highlight">El acceso a la alta direcci&oacute;n exige penetrar un c&iacute;rculo
            exclusivo dominado por la confianza y las referencias.</span>
        </div>
    </details>
    <details class="step-item">
        <summary class="step-summary">
            <div class="step-num">#2</div>
            <div class="step-title">El tejido empresarial vasco es complejo y fragmentado</div>
        </summary>
        <div class="step-body">
            Se sustenta en un potente grupo de empresas tractoras y, sobre todo, en una masiva red de industria mediana y familiar de alto rendimiento. Este ecosistema ofrece un volumen ingente de oportunidades que, por su atomización, 
            <span class="neon-highlight">exigen un estudio de mayor profundidad para responder a la pregunta
            estrat&eacute;gica: &iquest;D&oacute;nde quiero realmente trabajar?</span>
        </div>
    </details>
    <details class="step-item">
        <summary class="step-summary">
            <div class="step-num">#3</div>
            <div class="step-title">El sello de gigantes corporativos requiere traducci&oacute;n local</div>
        </summary>
        <div class="step-body">
            <span class="neon-highlight">El prestigio de firmas l&iacute;deres (BCG, Amazon, McKinsey)
            no act&uacute;a como aval autom&aacute;tico en el ecosistema local.</span>
            A menudo se desconoce la excelencia y la exigente "escuela de negocio" que hay detrás de estas trayectorias. Lo que en otros hubs globales tiene un efecto multiplicador — donde unos pocos años de experiencia equivalen a una década en entornos estándar—, en Euskadi requiere de un interlocutor que traduzca ese valor.
        </div>
    </details>
</div>
""", unsafe_allow_html=True)

    # --- 3. CARDS DE MERCADO ---
    b64_inst    = get_image_base64(os.path.join("assets", "institucional.png"))
    b64_abierto = get_image_base64(os.path.join("assets", "abierto.png"))
    b64_oculto  = get_image_base64(os.path.join("assets", "oculto.png"))

    col1, col2, col3 = st.columns(3, gap="medium")

    # ---- CARD 1: INSTITUCIONAL ----
    with col1:
        st.markdown(f"""
<div class="market-card-outer">
    <div class="market-card-img-wrap">
        <img src="{b64_inst}" alt="Mercado Institucional">
    </div>
    <div class="market-card-body">
        <div class="market-card-title"><span>M</span>ercado Institucional</div>
        <div class="market-card-desc">Es el mercado de retos y proyectos estratégicos articulado por el ecosistema público-privado. Proporciona capilaridad y respaldo oficial, posicionando el perfil en el radar institucional del territorio.</div>
    </div>
</div>
""", unsafe_allow_html=True)
        if st.button("Explorar Instituciones", key="btn_inst", use_container_width=True):
            st.session_state.page = 'entidades'
            st.rerun()

    # ---- CARD 2: ABIERTO ----
    with col2:
        st.markdown(f"""
<div class="market-card-outer">
    <div class="market-card-img-wrap">
        <img src="{b64_abierto}" alt="Mercado Abierto">
    </div>
    <div class="market-card-body">
        <div class="market-card-title"><span>M</span>ercado Abierto</div>
        <div class="market-card-desc">Es el mercado de procesos formales que las compañías delegan a headhunters para encontrar el talento perfecto. El acceso se gestiona mediante entrevistas de posicionamiento y validación de credenciales.</div>
    </div>
</div>
""", unsafe_allow_html=True)
        if st.button("Explorar Headhunters", key="btn_head", use_container_width=True):
            st.session_state.page = 'headhunters'
            st.rerun()

    # ---- CARD 3: OCULTO (2 botones) ----
    with col3:
        st.markdown(f"""
<div class="market-card-outer">
    <div class="market-card-img-wrap">
        <img src="{b64_oculto}" alt="Mercado Oculto">
    </div>
    <div class="market-card-body">
        <div class="market-card-title"><span>M</span>ercado Oculto</div>
        <div class="market-card-desc">Es el mercado de posiciones críticas previo a su publicación, al que se accede como consecuencia de las referencias y la reputación personal, constituyendo el núcleo del volumen de oportunidades.</div>
    </div>
</div>
""", unsafe_allow_html=True)
        b1, b2 = st.columns(2, gap="small")
        with b1:
            if st.button("Empresas", key="btn_emp", use_container_width=True):
                st.session_state.page = 'explorer'
                st.rerun()
        with b2:
            if st.button("Personas", key="btn_pers", use_container_width=True):
                st.session_state.page = 'personas'
                st.rerun()

    # --- NOTA METODOLÓGICA ---
    st.markdown("""
<div style="
    max-width: 1080px;
    margin: 60px auto 40px auto;
    padding: 30px 40px;
    background: #f9f9f9;
    border-left: 4px solid #bfa15a;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
">
    <p style="
        font-family: 'Manrope', sans-serif;
        color: #333333;
        font-size: 0.95rem;
        line-height: 1.7;
        margin: 0;
        text-align: justify;
    ">
        <strong style="color: #bfa15a; font-size: 1.1rem;">📌 Nota metodológica:</strong> 
        Los datos provienen de inteligencia artificial e información pública (prensa, rankings, webs corporativas). 
        Aunque procuro máxima precisión, algunos datos pueden estar sujetos a cambios o ser inexactos.
    </p>
</div>
""", unsafe_allow_html=True)