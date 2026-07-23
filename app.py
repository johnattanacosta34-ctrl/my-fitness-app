import streamlit as st
import pandas as pd
import json
import os

import streamlit as st

# Configuración inicial para móvil
st.set_page_config(
    page_title="Mi App Diaria",
    page_icon="⚡",
    layout="centered"
)

# Estilo visual para simular una barra inferior fija (opcional pero estético)
st.markdown("""
    <style>
        .stButton button {
            width: 100%;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Mi Panel Diario")

# Inicializar el estado de la navegación si no existe
if 'seccion_activa' not in st.session_state:
    st.session_state.seccion_activa = "Wellness"

# Separador visual
st.markdown("---")

# Contenido según la sección activa
if st.session_state.seccion_activa == "Wellness":
    st.header("🌿 Sección de Wellness")
    st.write("Aquí irá todo sobre dieta, lecturas, meditación y bienestar diario.")
    # TODO: Añadir lógica de dieta, lecturas, agua, etc.

elif st.session_state.seccion_activa == "Workout":
    st.header("💪 Sección de Workout")
    st.write("Aquí registrarás tus entrenamientos, rutinas, pesas y cardio.")
    # TODO: Añadir lógica de entrenamientos y ejercicios.

elif st.session_state.seccion_activa == "Profile":
    st.header("👤 Perfil y Métricas")
    st.write("Aquí verás tus metas personales, cálculos (TMB, macros) y resumen general.")
    # TODO: Añadir cálculos, métricas y metas.

# --- BARRA DE NAVEGACIÓN INFERIOR ---
st.markdown("---")
st.write("### Navegación")
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
