import streamlit as st
import gspread
import bcrypt
import datetime
from utils.google_sheets import get_credentials_from_secrets


# Función para conectar con Google Sheets y obtener usuarios
def get_users_from_sheets():
    try:
        creds = get_credentials_from_secrets()
        client = gspread.authorize(creds)
        sheet_url = "https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0"
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.worksheet("Usuarios")
        data = worksheet.get_all_records()

        # Limpieza de espacios en claves y valores
        cleaned_data = {
            str(row["usuario"]).strip().lower(): {
                "password": str(row["contraseña"]).strip(),
                "role": str(row["rol"]).strip().lower(),
            }
            for row in data if "usuario" in row and "contraseña" in row and "rol" in row
        }

        return cleaned_data
    except gspread.exceptions.WorksheetNotFound:
        st.error("La hoja 'Usuarios' no fue encontrada. Verifica el nombre.")
        return {}
    except Exception as e:
        st.error(f"Error al obtener usuarios de Google Sheets: {e}")
        return {}

# Función para registrar actividad en la hoja "Registro"
def log_access(username, status):
    try:
        creds = get_credentials_from_secrets()
        client = gspread.authorize(creds)
        sheet_url = "https://docs.google.com/spreadsheets/d/1qZX98WUaUGyUL5xSP0lHb7K7MfH7_ny8bRGOZnU1gGc/edit#gid=0"
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.worksheet("Registro")

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([username, status, now])
    except gspread.exceptions.WorksheetNotFound:
        st.error("La hoja 'Registro' no fue encontrada. Verifica el nombre.")
    except Exception as e:
        st.error(f"Error al registrar acceso en Google Sheets: {e}")

# Función de autenticación
def authenticate():
    st.title("🔐 Inicio de Sesión")
    st.markdown("### Bienvenido a **Lestrip**, por favor inicia sesión.")

    col1, col2, col3 = st.columns([1, 2, 1])  # Centrar los elementos
    with col2:
        username = st.text_input("Usuario", placeholder="Introduce tu usuario").strip().lower()
        password = st.text_input("Contraseña", type="password", placeholder="Introduce tu contraseña").strip()
        login_button = st.button("Iniciar sesión")

    users = get_users_from_sheets()

    if login_button:
        if username in users:
            stored_password = users[username]["password"]
            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = users[username]["role"]
                st.success(f"Bienvenido, {username}. Rol: {st.session_state['role']}")
                log_access(username, "Inicio de sesión exitoso")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
                log_access(username, "Intento fallido de inicio de sesión")
        else:
            st.error("Usuario no encontrado")
            log_access(username, "Intento de acceso con usuario no registrado")

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

# Función para cerrar sesión
def logout():
    if "logout_button_rendered" not in st.session_state:
        if st.sidebar.button("Cerrar sesión", key=f"logout_button_{st.session_state.get('username', '')}"):
            st.session_state.clear()
            st.success("Sesión cerrada correctamente.")
            st.rerun()
        st.session_state["logout_button_rendered"] = True  # Marcar como renderizado
