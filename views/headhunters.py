# ARCHIVO: .\views\headhunters.py

import streamlit as st
import pandas as pd

def show_headhunters(df_headhunters, df_alumni, df_conexiones):
    st.title("🏹 Red de Headhunters")
    st.markdown("Conoce a las principales firmas de selección ejecutiva y boutique de talento en el territorio.")
    
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("⬅️ Volver al Inicio", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    st.divider()

    if df_headhunters.empty:
        st.warning("⚠️ No se ha encontrado el archivo 'red_headhunters.csv' o está vacío.")
        return

    # Buscar la columna de LinkedIn de forma segura
    col_linkedin_name = next((c for c in df_headhunters.columns if str(c).strip().upper() == 'LINKEDIN'), None)

    categorias = sorted(df_headhunters['CATEGORÍA'].dropna().unique())
    
    if categorias:
        tabs = st.tabs([cat.title() for cat in categorias])
        
        for i, cat in enumerate(categorias):
            with tabs[i]:
                df_cat = df_headhunters[df_headhunters['CATEGORÍA'] == cat]
                
                for index, row in df_cat.iterrows():
                    nombre = row.get('NOMBRE', 'Sin nombre')
                    pod = row.get('POD', '')
                    ciudad = row.get('CIUDAD', '-')
                    definicion = row.get('DEFINICION', 'Sin descripción')
                    web = row.get('WEB', '#')
                    personas_clave_str = row.get('PERSONAS_CLAVE', '')
                    
                    # Preparar enlace LinkedIn
                    linkedin_entidad = '#'
                    if col_linkedin_name is not None and pd.notna(row[col_linkedin_name]):
                        val = str(row[col_linkedin_name]).strip()
                        if val and val.lower() not in ['nan', 'none', '-', '']:
                            linkedin_entidad = val
                    
                    # --- CONSTRUIR EL TÍTULO DEL EXPANDER ---
                    # Formato: 💼 **Nombre** — POD  📍 Ciudad
                    titulo_tarjeta = f"💼 **{nombre}**"
                    if pd.notna(pod) and str(pod).strip() != '':
                        titulo_tarjeta += f" — {str(pod).strip()}"
                    
                    titulo_tarjeta += f"  📍 {ciudad}"
                    
                    # Tarjeta de cada Headhunter
                    with st.expander(titulo_tarjeta):
                        
                        # Definición general directa
                        st.markdown(f"**¿En qué destacan?**\n\n{definicion}")
                        st.write("") # Pequeño espaciador
                        
                        # Directamente a los botones
                        col_web, col_link, col_personas = st.columns(3)
                        
                        with col_web:
                            if pd.notna(web) and str(web).strip() != '#' and str(web).lower() not in ['nan', 'none']:
                                st.link_button("🌐 Web Oficial", web, use_container_width=True)
                            else:
                                st.button("🌐 Sin Web", key=f"noweb_hh_{index}", disabled=True, use_container_width=True)
                        
                        with col_link:
                            if linkedin_entidad != '#':
                                st.link_button("🏢 LinkedIn Firma", linkedin_entidad, use_container_width=True)
                            else:
                                st.button("🏢 Sin LinkedIn", key=f"nolink_hh_{index}", disabled=True, use_container_width=True)
                        
                        with col_personas:
                            # Comprobamos si hay personas clave válidas
                            if pd.notna(personas_clave_str) and str(personas_clave_str).strip() != '' and str(personas_clave_str).lower() not in ['nan', 'none']:
                                with st.popover("👤 Contactos", use_container_width=True):
                                    st.markdown("**Contactos de referencia:**")
                                    # Separamos por punto y coma
                                    lista_personas = [p.strip() for p in str(personas_clave_str).split(';') if p.strip()]
                                    
                                    # Mostramos los nombres en texto
                                    for p_nombre in lista_personas:
                                        p_nombre_formateado = p_nombre.title()
                                        st.markdown(f"👤 **{p_nombre_formateado}**")
                            else:
                                st.button("👤 Sin contactos", key=f"nopc_hh_{index}", disabled=True, use_container_width=True)
    else:
        st.info("No hay categorías definidas en los datos.")