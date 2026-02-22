import streamlit as st
import pandas as pd
import re

# --- DEFINICIÓN DE LA VENTANA MODAL (POP-UP) ---
@st.dialog("🤝 Red de Conexiones")
def modal_conectar(persona_clave, entidad, df_alumni, df_conexiones):
    
    # Aseguramos que el nombre se vea bonito (Mayúscula inicial)
    persona_clave_display = str(persona_clave).title()
    
    st.markdown(f"Te gustaría conocer a **{persona_clave_display}** de **{entidad}**?")
    
    # 1. EL CRUCE
    conexiones_directas = pd.DataFrame()
    if not df_conexiones.empty:
        conexiones_directas = df_conexiones[
            (df_conexiones['persona_objetivo'].astype(str).str.strip().str.lower() == str(persona_clave).strip().lower()) &
            (df_conexiones['entidad_objetivo'].astype(str).str.strip().str.lower() == str(entidad).strip().lower())
        ]
        
    # 2. BUSCAR EL LINKEDIN DE LA PERSONA OBJETIVO EN CONEXIONES.CSV
    url_persona_objetivo = "#"
    if not conexiones_directas.empty and 'persona_objetivo_linkedin' in conexiones_directas.columns:
        val_url = str(conexiones_directas.iloc[0]['persona_objetivo_linkedin']).strip()
        if val_url and val_url.lower() not in ['nan', 'none', '-', '']:
            url_persona_objetivo = val_url
            
    # Mostrar el botón de LinkedIn de la persona si lo hemos encontrado
    if url_persona_objetivo != "#":
        st.link_button(f"🔗 Ver perfil de {persona_clave_display}", url_persona_objetivo)

    st.divider()
    
    # --- ESCENARIO A: TENEMOS UN PUENTE DIRECTO ---
    if not conexiones_directas.empty:
        st.success(f"🌟 ¡Genial! Tienes {len(conexiones_directas)} contacto(s) que pueden introducirte a esta persona.")
        
        for _, relacion in conexiones_directas.iterrows():
            nombre_puente_raw = relacion.get('nombre_puente', 'Desconocido')
            nombre_puente_display = str(nombre_puente_raw).title() 
            contexto = relacion.get('contexto_relacion', 'Sin contexto especificado')
            
            cargo_actual = "Profesional"
            empresa_actual = "empresa no especificada"
            url_linkedin_puente = "#"
            
            if not df_alumni.empty:
                datos_puente = df_alumni[df_alumni['Nombre'].astype(str).str.strip().str.lower() == str(nombre_puente_raw).strip().lower()]
                if not datos_puente.empty:
                    row_p = datos_puente.iloc[0]
                    
                    c = str(row_p.get('Cargo', '')).strip()
                    if c and c.lower() not in ['nan', '-', '']: cargo_actual = c.title()
                    
                    matriz = str(row_p.get('nombre_matriz_einforma', '-')).strip()
                    dba = str(row_p.get('nombre_dba', '-')).strip()
                    
                    if matriz and matriz.lower() not in ['nan', '-', '']:
                        empresa_actual = matriz.title()
                    elif dba and dba.lower() not in ['nan', '-', '']:
                        empresa_actual = dba.title()
                        
                    link = str(row_p.get('url_linkedin', '')).strip()
                    if link and link.lower() not in ['nan', '-', '']:
                        url_linkedin_puente = link

            # Tarjeta del Puente
            st.markdown(f"""
            <div style="border: 2px solid #1F4E79; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #f8fbff;">
                <b style="color:#1F4E79; font-size: 1.1em;">👤 {nombre_puente_display}</b><br>
                <span style="color: #666; font-size: 0.9em;">💼 {cargo_actual} en {empresa_actual}</span><br>
                <div style="margin-top:8px; font-size: 0.85em; background-color:#e3f2fd; padding:6px 10px; border-radius:4px; border-left: 3px solid #1F4E79;">
                    💡 <b>Contexto:</b> {contexto}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón LinkedIn del puente (Solo si existe)
            if url_linkedin_puente != "#":
                st.link_button(f"💼 Ver LinkedIn de {nombre_puente_display}", url_linkedin_puente)
                
            st.write("") 


    # --- ESCENARIO B: NO HAY CONEXIÓN DIRECTA ---
    else:
        st.warning(f"No tienes contactos directos registrados que conozcan a {persona_clave_display}.")
        
        match_empresa = pd.DataFrame()
        if not df_alumni.empty:
            # Buscamos a alguien que trabaje en esa misma entidad (usando nombre_matriz_einforma)
            match_empresa = df_alumni[df_alumni['nombre_matriz_einforma'].astype(str).str.contains(re.escape(str(entidad).strip()), case=False, na=False)]
        
        if not match_empresa.empty:
            st.info(f"Sin embargo, tienes {len(match_empresa)} contacto(s) trabajando en **{entidad}** que podrían orientarte:")
            for _, row in match_empresa.iterrows():
                n_colega = str(row.get('Nombre', 'Contacto')).title()
                c_colega = str(row.get('Cargo', 'Sin cargo')).title()
                st.markdown(f"- 👤 **{n_colega}** ({c_colega})")


# --- VISTA PRINCIPAL DE ENTIDADES ---
def show_entidades(df_entidades, df_alumni, df_conexiones):
    st.title("🏛️ Instituciones Vascas")
    st.markdown("Navega por las distintas categorías para conocer a los jugadores clave que impulsan la industria y tecnología local.")
    
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("⬅️ Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    st.divider()

    if df_entidades.empty:
        st.warning("⚠️ No se ha encontrado el archivo 'ecosistema_vasco.csv' o está vacío.")
        return

    col_linkedin_name = None
    for col in df_entidades.columns:
        if str(col).strip().upper() == 'LINKEDIN':
            col_linkedin_name = col
            break

    categorias = sorted(df_entidades['CATEGORÍA'].dropna().unique())
    
    if categorias:
        tabs = st.tabs([cat.title() for cat in categorias])
        
        for i, cat in enumerate(categorias):
            with tabs[i]:
                df_cat = df_entidades[df_entidades['CATEGORÍA'] == cat]
                
                for index, row in df_cat.iterrows():
                    nombre = row.get('NOMBRE', 'Sin nombre')
                    ciudad = row.get('Ciudad', '-')
                    definicion = row.get('DEFINICION', 'Sin descripción')
                    web = row.get('Web', '#')
                    personas_clave_str = row.get('PERSONAS_CLAVE', '')
                    
                    linkedin_entidad = '#'
                    if col_linkedin_name is not None and pd.notna(row[col_linkedin_name]):
                        val = str(row[col_linkedin_name]).strip()
                        if val and val.lower() not in ['nan', 'none', '-', '']:
                            linkedin_entidad = val
                    
                    with st.expander(f"📌 **{nombre}** — 📍 {ciudad}"):
                        st.markdown(f"**¿Qué hacen?**\n\n{definicion}")
                        st.write("")
                        st.caption("🚀 ACCIONES Y CONTACTOS")
                        
                        col_web, col_link, col_personas = st.columns(3)
                        
                        with col_web:
                            if web and str(web).strip() != '#' and str(web).lower() not in ['nan', 'none']:
                                st.link_button("🌐 Web Oficial", web, use_container_width=True)
                            else:
                                st.button("🌐 Sin Web", key=f"noweb_{index}", disabled=True, use_container_width=True)
                        
                        with col_link:
                            if linkedin_entidad != '#':
                                st.link_button("🏢 LinkedIn Entidad", linkedin_entidad, use_container_width=True)
                            else:
                                st.button("🏢 Sin LinkedIn", key=f"nolink_{index}", disabled=True, use_container_width=True)
                        
                        with col_personas:
                            if pd.notna(personas_clave_str) and str(personas_clave_str).strip() != '' and str(personas_clave_str).lower() not in ['nan', 'none']:
                                with st.popover("👤👤 Contactos", use_container_width=True):
                                    st.markdown("**¿Con quién quieres conectar?**")
                                    lista_personas = [p.strip() for p in str(personas_clave_str).split('|') if p.strip()]
                                    
                                    for idx, p_nombre in enumerate(lista_personas):
                                        p_nombre_formateado = p_nombre.title()
                                        if st.button(f"👤 {p_nombre_formateado}", key=f"btn_pc_{index}_{idx}", use_container_width=True):
                                            modal_conectar(p_nombre_formateado, nombre, df_alumni, df_conexiones)
                            else:
                                with st.popover("👤👤 Contactos", use_container_width=True):
                                    st.info("Aún no tenemos contactos mapeados para esta entidad.")
    else:
        st.info("No hay categorías definidas en los datos.")