from cryptography.fernet import Fernet

# 1. Generamos la llave maestra
key = Fernet.generate_key()

# 2. Imprimimos la llave por pantalla (¡CÓPIALA!)
print("\n" + "="*50)
print("⚠️  TU LLAVE SECRETA (COPIA ESTO):")
print(key.decode())
print("="*50 + "\n")

# 3. Leemos tu archivo de Alumni (el que tiene datos privados)
# Asegúrate de que este nombre sea EXACTO al de tu archivo
archivo_privado = 'deusto_alumni_dba_clean.csv' 

with open(archivo_privado, 'rb') as file:
    datos_originales = file.read()

# 4. Encriptamos los datos
cipher_suite = Fernet(key)
datos_encriptados = cipher_suite.encrypt(datos_originales)

# 5. Guardamos el nuevo archivo seguro
with open('alumni_seguro.enc', 'wb') as file:
    file.write(datos_encriptados)

print(f"✅ ¡Listo! Se ha creado el archivo 'alumni_seguro.enc'.")