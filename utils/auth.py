import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import bcrypt
import datetime

# Función para conectar con Google Sheets
def get_users_from_sheets():
    creds = Credentials.from_service_account_file(
        "credenciales.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit?gid=1178593666"
    )
    worksheet = sheet.worksheet("Usuarios")
    data = worksheet.get_all_records()

    # Limpieza de espacios en claves y valores
    cleaned_data = {
        str(row["usuario"]).strip().lower(): {
            "password": str(row["contraseña"]).strip(),
            "role": str(row["rol"]).strip().lower(),
        }
        for row in data
    }

    return cleaned_data

# Función para registrar actividad en otra hoja de Google Sheets
def log_access(username, status):
    creds = Credentials.from_service_account_file("credenciales.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0")
    worksheet = sheet.worksheet("Registro")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([username, status, now])

# Función de autenticación
def authenticate():
    st.title("🔐 Inicio de Sesión")
    st.markdown("### Bienvenido a **Lestrip**, por favor inicia sesión.")

    col1, col2, col3 = st.columns([1, 2, 1])  # Centrar los elementos
    with col2:
        username = st.text_input("Usuario").strip().lower()
        password = st.text_input("Contraseña", type="password").strip()
        login_button = st.button("Iniciar sesión")

    users = get_users_from_sheets()

    if login_button:
        stored_password = users.get(username, {}).get("password")

        if username in users and bcrypt.checkpw(password.encode(), stored_password.encode()):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]
            st.success(f"Bienvenido, {username}. Rol: {st.session_state['role']}")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")



# Función para verificar si el usuario está autenticado
def check_auth():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        authenticate()
        st.stop()
    
    # Verificar si ya se ha renderizado el menú antes de volver a mostrarlo
    if "menu_rendered" not in st.session_state:
        st.sidebar.title(f"Bienvenido, {st.session_state['username']} ({st.session_state['role']})")
        logout()
        st.session_state["menu_rendered"] = True

if "logout_counter" not in st.session_state:
    st.session_state["logout_counter"] = 0

import uuid

def logout():
    if "logout_button_rendered" not in st.session_state:
        if st.sidebar.button("Cerrar sesión", key=f"logout_button_{st.session_state['username']}"):
            st.session_state.clear()
            st.success("Sesión cerrada correctamente.")
            st.rerun()
        st.session_state["logout_button_rendered"] = True  # Marcar como renderizado

