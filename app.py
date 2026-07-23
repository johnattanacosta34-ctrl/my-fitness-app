import streamlit as st, pandas as pd, json, os

st.set_page_config(page_title="Daily Dashboard", page_icon="⚡", layout="centered")

# --- DISEÑO GENERAL (FONDO NEGRO, LETRAS BLANCAS, CAJAS NARANJAS MÁS PEQUEÑAS) ---
st.markdown("""
    <style>
        :root { color-scheme: dark !important; }
        .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        section[data-testid="stSidebar"], #MainMenu, footer { display: none !important; }
        
        /* Textos generales en blanco */
        h1, h2, h3, h4, h5, h6, p, span, label, div { color: #FFFFFF !important; }
        
        /* Tarjetas / Cajas Naranjas internas */
        .custom-card { background: linear-gradient(135deg, #FF8C42 0%, #FF701A 100%) !important; padding: 20px !important; border-radius: 16px !important; margin-bottom: 15px !important; box-shadow: 0 10px 25px rgba(255, 140, 66, 0.25) !important; border: none !important; }
        .custom-card * { color: #000000 !important; }
        .card-title { font-size: 12px !important; font-weight: 700 !important; text-transform: uppercase !important; opacity: 0.85; margin-bottom: 6px !important; }
        .card-body { font-size: 32px !important; font-weight: 800 !important; }

        /* Estilo para los botones principales (ahora más compactos y con mejor distribución) */
        div.stButton > button {
            background: linear-gradient(135deg, #FF8C42 0%, #FF701A 100%) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px 16px !important;
            box-shadow: 0 6px 15px rgba(255, 140, 66, 0.2) !important;
            transition: all 0.2s ease-in-out;
            width: 100% !important;
        }
        div.stButton > button:hover {
            opacity: 0.9 !important;
            color: #000000 !important;
            border: none !important;
        }
        
        .block-container { padding-bottom: 50px !important; }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTENCIA DE DATOS CON MANEJO SEGURO ---
DATA_FILE = "reading_data.json"
if "active_books" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: data = json.load(f)
        except:
            data = {}
    else:
        data = {}
        
    st.session_state.active_books = data.get("active_books", {
        "Straight Jacket by Matthew Todd": {"read": 135, "total": 300},
        "Heated Rivalry by Rachel Reid": {"read": 255, "total": 300}
    })
    st.session_state.completed_books = data.get("completed_books", [])
    st.session_state.user_profile = data.get("user_profile", {
        "username": "Felipe Acosta",
        "weight": 82.7,
        "bmi": 27.6,
        "fat": 23.4,
        "fat_mass": 19.3
    })

if 'seccion_activa' not in st.session_state: st.session_state.seccion_activa = "Home"
if 'profile_subview' not in st.session_state: st.session_state.profile_subview = "Main"

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "active_books": st.session_state.active_books, 
            "completed_books": st.session_state.completed_books,
            "user_profile": st.session_state.user_profile
        }, f)

# --- NAVEGACIÓN PRINCIPAL ---

# PÁGINA DE INICIO (HOME)
if st.session_state.seccion_activa == "Home":
    
    # Cabecera con Nombre a la izquierda y Botón de Ajustes a la derecha
    col_name, col_settings = st.columns([4, 1])
    with col_name:
        st.markdown(f"## **{st.session_state.user_profile['username']}**")
    with col_settings:
        if st.button("⚙️", help="Settings"):
            st.session_state.seccion_activa = "Settings"
            st.rerun()
        
    st.markdown("<hr style='margin: 15px 0; border-color: #2C2C2E;'>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Cajas principales distribuidas en columnas o más compactas en tamaño
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.seccion_activa = "Profile"
            st.session_state.profile_subview = "Main"
            st.rerun()
    with c2:
        if st.button("🏋️ Workout", use_container_width=True):
            st.session_state.seccion_activa = "Workout"
            st.rerun()
    with c3:
        if st.button("✨ Wellness", use_container_width=True):
            st.session_state.seccion_activa = "Wellness"
            st.rerun()

# SECCIÓN SETTINGS
elif st.session_state.seccion_activa == "Settings":
    if st.button("⬅️ Back"):
        st.session_state.seccion_activa = "Home"
        st.rerun()
    st.title("⚙️ Settings")
    
    with st.form("settings_form"):
        new_name = st.text_input("Nombre de usuario", value=st.session_state.user_profile["username"])
        if st.form_submit_button("Guardar Cambios", use_container_width=True):
            st.session_state.user_profile["username"] = new_name
            save_data()
            st.success("¡Nombre de usuario actualizado con éxito!")

# SECCIÓN PROFILE (Y SUS SUBVISTAS)
elif st.session_state.seccion_activa == "Profile":
    
    if st.button("⬅️ Back"):
        if st.session_state.profile_subview == "Main":
            st.session_state.seccion_activa = "Home"
        else:
            st.session_state.profile_subview = "Main"
        st.rerun()

    if st.session_state.profile_subview == "Main":
        st.title("👤 Profile Dashboard")
        
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("📈 Statistics", use_container_width=True):
                st.session_state.profile_subview = "Statistics"
                st.rerun()
            if st.button("📏 Measures", use_container_width=True):
                st.session_state.profile_subview = "Measures"
                st.rerun()
        with b_col2:
            if st.button("📅 Calendar", use_container_width=True):
                st.session_state.profile_subview = "Calendar"
                st.rerun()
            if st.button("🎯 Goals", use_container_width=True):
                st.session_state.profile_subview = "Goals"
                st.rerun()

    elif st.session_state.profile_subview == "Statistics":
        st.title("📈 Statistics")
        st.info("Aquí verás tus gráficos de rendimiento y estadísticas de progreso.")

    elif st.session_state.profile_subview == "Measures":
        st.title("📏 Measures & Body Metrics")
        
        with st.form("measures_form"):
            c1, c2, c3, c4 = st.columns(4)
            w = c1.number_input("Weight", value=float(st.session_state.user_profile["weight"]), step=0.1)
            bmi = c2.number_input("BMI", value=float(st.session_state.user_profile["bmi"]), step=0.1)
            bf = c3.number_input("Fat %", value=float(st.session_state.user_profile["fat"]), step=0.1)
            fm = c4.number_input("Fat Mass", value=float(st.session_state.user_profile["fat_mass"]), step=0.1)
            
            if st.form_submit_button("Guardar Medidas", use_container_width=True):
                st.session_state.user_profile.update({"weight": w, "bmi": bmi, "fat": bf, "fat_mass": fm})
                save_data()
                st.success("¡Medidas guardadas con éxito!")

        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='custom-card'><div class='card-title'>Weight</div><div class='card-body'>{st.session_state.user_profile['weight']}</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='custom-card'><div class='card-title'>BMI</div><div class='card-body'>{st.session_state.user_profile['bmi']}</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='custom-card'><div class='card-title'>Body Fat</div><div class='card-body'>{st.session_state.user_profile['fat']}%</div></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='custom-card'><div class='card-title'>Fat Mass</div><div class='card-body'>{st.session_state.user_profile['fat_mass']}</div></div>", unsafe_allow_html=True)

    elif st.session_state.profile_subview == "Calendar":
        st.title("📅 Calendar & Schedule")
        schedule_data = {
            "Time Window": ["07:30 – 08:00", "08:00 – 09:30", "09:30 – 10:30"],
            "Activity": ["🌅 Wake Up", "🏋️ Gym", "🍳 Breakfast"],
            "Strategy": ["No scrolling", "Consistency", "Refuel"]
        }
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

    elif st.session_state.profile_subview == "Goals":
        st.title("🎯 Targets & Goals")
        st.write("• Target Weight: 74 kg")
        st.write("• Target BMI: 24")
        st.write("• Target Body Fat: 13%")

# SECCIÓN WORKOUT
elif st.session_state.seccion_activa == "Workout":
    if st.button("⬅️ Back"):
        st.session_state.seccion_activa = "Home"
        st.rerun()
    st.title("🏋️ Workout Session")
    st.write("Sección de entrenamientos...")

# SECCIÓN WELLNESS
elif st.session_state.seccion_activa == "Wellness":
    if st.button("⬅️ Back"):
        st.session_state.seccion_activa = "Home"
        st.rerun()
    st.title("✨ Wellness Hub")
    st.write("Sección de bienestar...")
