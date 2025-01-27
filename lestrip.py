import streamlit as st 
from utils.auth import check_auth, logout
from pages.dashboard import show_dashboard
from pages.gestion_escrituras import gestion_escrituras
from pages.usuarios import manage_users
from pages.seguimiento import seguimiento_tramites

# Configuración de la app
st.set_page_config(page_title="Lestrip - Gestión Notarial", page_icon="📜", layout="wide")

# Verificación de autenticación antes de mostrar contenido
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    check_auth()
    st.stop()  # Detiene la ejecución hasta que el usuario inicie sesión

# Manejo de la barra lateral para navegación
with st.sidebar:
    st.title(f"Bienvenido, {st.session_state.get('username', '')} ({st.session_state.get('role', '')})")

    # Definir opciones de navegación según el rol del usuario
    if st.session_state.get("role") == "administrador":
        page = st.radio("Selecciona una opción", 
            ["Dashboard", "Gestión de Escrituras", "Usuarios", "Seguimiento"])
    elif st.session_state.get("role") == "notario":
        page = st.radio("Selecciona una opción", 
            ["Gestión de Escrituras", "Seguimiento"])
    elif st.session_state.get("role") == "cliente":
        page = st.radio("Selecciona una opción", 
            ["Seguimiento"])
    else:
        st.warning("Rol no reconocido.")
        st.stop()

    st.session_state["page"] = page  # Guardar la selección en la sesión

    if st.button("Cerrar sesión"):
        st.session_state.clear()
        st.success("Sesión cerrada correctamente.")
        st.rerun()

# Renderizar la página seleccionada
if st.session_state["page"] == "Dashboard":
    show_dashboard()
elif st.session_state["page"] == "Gestión de Escrituras":
    gestion_escrituras()
elif st.session_state["page"] == "Usuarios":
    manage_users()
elif st.session_state["page"] == "Seguimiento":
    seguimiento_tramites()
