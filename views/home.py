# ARCHIVO: .\views\home.py

import streamlit as st
import base64
import os

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 12a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm9 11a1 1 0 0 1-2 0v-2a3 3 0 0 0-3-3H8a3 3 0 0 0-3 3v2a1 1 0 0 1-2 0v-2a5 5 0 0 1 5-5h8a5 5 0 0 1 5 5v2z' fill='rgba(255,255,255,0.2)'/%3E%3C/svg%3E"

def show_home():
    # --- PREPARAR IMAGEN ---
    img_path = os.path.join("assets", "foto_perfil.png")
    img_base64 = get_image_base64(img_path)
    
    # --- ESTILOS CSS ---
    st.markdown(f"""
    <style>
        .hero-container {{ display: flex; align-items: center; justify-content: center; gap: 40px; flex-wrap: wrap; text-align: left; }}
        .profile-avatar {{ width: 180px; height: 180px; border-radius: 50%; border: 5px solid rgba(255,255,255,0.2); object-fit: cover; box-shadow: 0 10px 25px rgba(0,0,0,0.25); }}
        .hero-text {{ max-width: 800px; }}
        .mobile-br {{ display: none; }} 
        
        @media (max-width: 768px) {{ 
            .hero-container {{ text-align: center; flex-direction: column; gap: 20px; }} 
            .hero-text {{ margin-bottom: 20px; }} 
            .mobile-br {{ display: block; content: ""; margin-top: 5px; }} 
            .hero-desc {{ font-size: 1.1em !important; }} 
        }}

        /* --- COLORES DE BOTONES CON INTERACCIÓN MEJORADA --- */
        
        /* 1. Institucional - Verde */
        [data-testid="stHorizontalBlock"] > div:nth-child(1) button {{
            border: 1.5px solid #2E7D32 !important;
            color: #2E7D32 !important;
            background-color: #F4F9F5 !important;
            transition: all 0.2s ease-in-out !important;
        }}
        [data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover {{
            background-color: #DDEEDF !important; /* Pastel más oscuro en hover */
            border-color: #2E7D32 !important;
        }}
        [data-testid="stHorizontalBlock"] > div:nth-child(1) button:active {{
            background-color: #C1DEC5 !important; /* Aún más oscuro al click */
            transform: scale(0.98) !important;
        }}

        /* 2. Abierto - Naranja */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) button {{
            border: 1.5px solid #E67E22 !important;
            color: #E67E22 !important;
            background-color: #FFF8F0 !important;
            transition: all 0.2s ease-in-out !important;
        }}
        [data-testid="stHorizontalBlock"] > div:nth-child(2) button:hover {{
            background-color: #FFEAD2 !important; /* Pastel más oscuro en hover */
            border-color: #E67E22 !important;
        }}
        [data-testid="stHorizontalBlock"] > div:nth-child(2) button:active {{
            background-color: #FCD5AC !important; /* Aún más oscuro al click */
            transform: scale(0.98) !important;
        }}

        /* 3. Oculto - Púrpura */
        /* Aplicamos a los botones dentro de la tercera columna principal */
        [data-testid="stHorizontalBlock"] > div:nth-child(3) button {{
            border: 1.5px solid #8E44AD !important;
            color: #8E44AD !important;
            background-color: #F8F4FA !important;
            transition: all 0.2s ease-in-out !important;
        }}
        [data-testid="stHorizontalBlock"] > div:nth-child(3) button:hover {{
            background-color: #F0E2F5 !important; /* Pastel más oscuro en hover */
            border-color: #8E44AD !important;
        }}
        [data-testid="stHorizontalBlock"] > div:nth-child(3) button:active {{
            background-color: #E4C9E9 !important; /* Aún más oscuro al click */
            transform: scale(0.98) !important;
        }}
        
        button p {{ font-weight: 700 !important; }}

    </style>
    
    <div style="background: linear-gradient(135deg, #1F4E79 0%, #0D253F 100%); padding: 50px 30px; border-radius: 20px; color: white; box-shadow: 0 10px 40px rgba(31, 78, 121, 0.3); margin-bottom: 40px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -60px; right: -60px; width: 250px; height: 250px; background: rgba(255,255,255,0.04); border-radius: 50%; z-index: 0;"></div>
        <div class="hero-container" style="position: relative; z-index: 1;">
            <img src="{img_base64}" alt="Asier Dorronsoro" class="profile-avatar">
            <div class="hero-text">
                <h1 style="font-size: 3.2em; font-weight: 800; margin: 0 0 15px 0; letter-spacing: -1px; line-height: 1.1; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);"> Asier Dorronsoro </h1>
                <p class="hero-desc" style="font-size: 1.25em; margin: 0 0 25px 0; opacity: 0.95; font-weight: 300; line-height: 1.5;">
                    <strong>Objetivo: </strong>Encontrar mi siguiente reto profesional.<br class="mobile-br"> Viviendo en San&nbsp;Sebastián.
                </p>
                <a href="https://www.linkedin.com/in/asierdorronsoro/" target="_blank" style="text-decoration: none; background: white; color: #1F4E79; padding: 12px 28px; border-radius: 30px; font-weight: 700; font-size: 1em; display: inline-flex; align-items: center; gap: 8px; border: 2px solid white;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#1F4E79"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                    Conectar en LinkedIn
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- TÍTULO SECCIÓN M AL CUBO ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="color: #1F4E79; font-weight: 900; font-size: 3.2rem; margin-bottom: 5px; letter-spacing: -1px;">
            M³ <span style="font-size: 1.8rem; font-weight: 500; color: #1F4E79; vertical-align: middle;">— M al cubo</span>
        </h2>
        <p style="color: #555; font-size: 1.15rem; max-width: 850px; margin: 0 auto; line-height: 1.6;">
            Un producto de autor para penetrar el ecosistema empresarial vasco a escala, diseñado para generar y materializar oportunidades directivas de forma inteligente, proactiva y anticipada.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- COLUMNAS INTEGRADAS ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; border-top: 4px solid #2E7D32; padding: 25px 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; height: 350px;">
            <div style="font-size: 2.2rem; margin-bottom: 15px;">🏛️</div>
            <h3 style="color: #1F4E79; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; letter-spacing: -0.5px; ">
                <span style="color: #2E7D32; font-size: 1.7rem; font-weight: 900;">M</span>ercado Institucional
            </h3>
            <p style="font-size: 0.95rem; color: #444; line-height: 1.5; margin-bottom: 25px;text-align: justify;">
                Es el mercado de retos y proyectos estratégicos articulado por el ecosistema público-privado. Proporciona capilaridad y respaldo oficial, posicionando el perfil en el radar institucional del territorio. 
            </p>
            <div style="font-size: 0.75rem; font-weight: 800; color: #2E7D32; text-transform: uppercase; letter-spacing: 1px; border-top: 1px solid #eee; padding-top: 15px;">
                ⚙️ Accionar Mercado:
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Explorar Instituciones", key="btn_home_ecosistema", use_container_width=True):
            st.session_state.page = 'entidades'
            st.session_state.scroll_needed = True
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background-color: white; border-top: 4px solid #E67E22; padding: 25px 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; height: 350px;">
            <div style="font-size: 2.2rem; margin-bottom: 15px;">🏹</div>
            <h3 style="color: #1F4E79; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; letter-spacing: -0.5px;">
                <span style="color: #E67E22; font-size: 1.7rem; font-weight: 900;">M</span>ercado Abierto
            </h3>
            <p style="font-size: 0.95rem; color: #444; line-height: 1.5; margin-bottom: 25px; text-align: justify;">
                Es el mercado de procesos formales que las compañías delegan a headhunters para encontrar el talento perfecto. El acceso se gestiona mediante entrevistas de posicionamiento y validación de credenciales. 
            </p>
            <div style="font-size: 0.75rem; font-weight: 800; color: #E67E22; text-transform: uppercase; letter-spacing: 1px; border-top: 1px solid #eee; padding-top: 15px;">
                ⚙️ Accionar Mercado:
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Explorar Headhunters", key="btn_home_headhunters", use_container_width=True):
            st.session_state.page = 'headhunters'
            st.session_state.scroll_needed = True
            st.rerun()

    with col3:
        st.markdown("""
        <div style="background-color: white; border-top: 4px solid #8E44AD; padding: 25px 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; height: 350px;">
            <div style="font-size: 2.2rem; margin-bottom: 15px;">👁️‍🗨️</div>
            <h3 style="color: #1F4E79; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; letter-spacing: -0.5px;">
                <span style="color: #8E44AD; font-size: 1.7rem; font-weight: 900;">M</span>ercado Oculto
            </h3>
            <p style="font-size: 0.95rem; color: #444; line-height: 1.5; margin-bottom: 25px; text-align: justify;">
                Es el mercado de posiciones críticas previo a su publicación, al que se accede como consecuencia de las referencias y la reputación personal, constituyendo el núcleo del volumen de oportunidades.
            </p>
            <div style="font-size: 0.75rem; font-weight: 800; color: #8E44AD; text-transform: uppercase; letter-spacing: 1px; border-top: 1px solid #eee; padding-top: 15px;">
                ⚙️ Accionar Mercado:
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Explorar Empresas", key="btn_home_empresas", use_container_width=True):
                st.session_state.page = 'explorer'
                st.session_state.scroll_needed = True
                st.session_state.selected_empresa = None
                st.session_state.current_page = 0
                st.rerun()
                
        with b2:
            if st.button("Explorar Personas", key="btn_home_personas", use_container_width=True):
                st.session_state.page = 'personas'
                st.session_state.scroll_needed = True
                st.rerun()
    
    st.write("")
    st.write("")
    
    # --- NOTA ---
    st.markdown("""
    <div class="note-section" style="margin-top: 20px;">
        <p><strong>📌 Nota metodológica:</strong> Los datos provienen de inteligencia artificial e información pública (prensa, rankings, webs corporativas). Aunque procuro máxima precisión, algunos datos pueden estar sujetos a cambios o ser inexactos.</p>
    </div>
    """, unsafe_allow_html=True)