import os
import streamlit as st

# --- BLOQUE DE DIAGNÓSTICO ---
st.write("### 🔍 Diagnóstico de Servidor")
ruta_archivo = os.path.join("data", "alumni_seguro.enc")

# 1. ¿Existe el archivo en la ruta esperada?
if os.path.exists(ruta_archivo):
    st.success(f"✅ El archivo existe en: {ruta_archivo}")
else:
    st.error(f"❌ El archivo NO existe en: {ruta_archivo}")

# 2. ¿Qué archivos ve el servidor en la carpeta data?
if os.path.exists("data"):
    st.write("Archivos encontrados en carpeta 'data':", os.listdir("data"))
else:
    st.write("❌ La carpeta 'data' no existe en el servidor.")

# 3. ¿Está la clave configurada en los Secrets?
if "CLAVE_ENCRIPTACION" in st.secrets:
    st.success("✅ La clave 'CLAVE_ENCRIPTACION' está configurada en Secrets.")
else:
    st.error("❌ Falta la clave 'CLAVE_ENCRIPTACION' en los Secrets de Streamlit Cloud.")
# -----------------------------