import streamlit as st

# Configuración inicial para móvil
st.set_page_config(
    page_title="Mi App Diaria",
    page_icon="⚡",
    layout="centered"
)

# Estilo CSS para fijar los botones en horizontal y darles aspecto de barra de navegación
st.markdown("""
    <style>
        /* Forzar que las columnas de la navegación inferior no se apilen y estén juntas */
        div.row-widget.stHorizontal {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }
        /* Estética de los botones de navegación */
        .stButton button {
            width: 100%;
            border-radius: 8px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Mi Panel Diario")

# Inicializar el estado de la navegación si no existe
if 'seccion_activa' not in st.session_state:
    st.session_state.seccion_activa = "Wellness"

# Separador visual superior
st.markdown("---")

# Contenido según la sección activa
if st.session_state.seccion_activa == "Wellness":
    st.header("🌿 Sección de Wellness")
    st.write("Aquí irá todo sobre dieta, lecturas, meditación y bienestar diario.")

elif st.session_state.seccion_activa == "Workout":
    st.header("💪 Sección de Workout")
    st.write("Aquí registrarás tus entrenamientos, rutinas, pesas y cardio.")

elif st.session_state.seccion_activa == "Profile":
    st.header("👤 Perfil y Métricas")
    st.write("Aquí verás tus metas personales, cálculos (TMB, macros) y resumen general.")

# --- BARRA DE NAVEGACIÓN INFERIOR HORIZONTAL ---
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌿 Wellness", use_container_width=True):
        st.session_state.seccion_activa = "Wellness"
        st.rerun()

with col2:
    if st.button("💪 Workout", use_container_width=True):
        st.session_state.seccion_activa = "Workout"
        st.rerun()

with col3:
    if st.button("👤 Profile", use_container_width=True):
        st.session_state.seccion_activa = "Profile"
        st.rerun()
