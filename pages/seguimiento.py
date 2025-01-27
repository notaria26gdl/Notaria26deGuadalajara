import streamlit as st

def seguimiento_tramites():
    st.title("📂 Seguimiento de Trámites")

    # Agregar funcionalidad de filtro o tabla aquí
    estado = st.selectbox("Filtrar por estado", ["Todos", "Pendiente", "Completado"])
    
    # Simulación de tabla (debería cargarse desde Google Sheets)
    data = []  # Aquí iría la carga de datos real
    st.table(data)
