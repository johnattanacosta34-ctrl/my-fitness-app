import streamlit as st, pandas as pd, json, os

st.set_page_config(page_title="Daily Dashboard", page_icon="⚡", layout="centered")

# --- DISEÑO GENERAL Y BARRA FLOTANTE ---
st.markdown("""
    <style>
        :root { color-scheme: light !important; }
        .stApp { background-color: #FAFAFC !important; color: #111111 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        section[data-testid="stSidebar"], #MainMenu, footer { display: none !important; }
        
        .custom-card { background: linear-gradient(135deg, #FF8C42 0%, #FF701A 100%) !important; padding: 20px !important; border-radius: 16px !important; margin-bottom: 15px !important; box-shadow: 0 10px 25px rgba(255, 140, 66, 0.25) !important; }
        .custom-card * { color: #000000 !important; }
        .card-title { font-size: 12px !important; font-weight: 700 !important; text-transform: uppercase !important; opacity: 0.85; margin-bottom: 6px !important; }
        .card-body { font-size: 32px !important; font-weight: 800 !important; }
        .card-sub { font-size: 13px !important; font-weight: 600 !important; opacity: 0.9; }
        
        .block-container { padding-bottom: 130px !important; }

        /* Contenedor principal que simula la píldora flotante */
        div.fixed-dock {
            position: fixed !important;
            bottom: 25px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            background-color: #161618 !important;
            padding: 8px 12px !important;
            border-radius: 40px !important;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4) !important;
            z-index: 999999 !important;
            border: 1px solid #2C2C2E !important;
            width: auto !important;
            max-width: 90% !important;
        }

        div.fixed-dock [data-testid="column"] {
            width: auto !important;
            flex: 1 !important;
            min-width: 90px !important;
        }

        div.fixed-dock button {
            background-color: transparent !important;
            color: #8E8E93 !important;
            border: none !important;
            border-radius: 30px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            width: 100% !important;
            padding: 8px 0px !important;
            box-shadow: none !important;
            transition: all 0.2s ease-in-out;
        }
        
        div.fixed-dock button:hover {
            color: #FFFFFF !important;
            background-color: rgba(255, 255, 255, 0.08) !important;
        }
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
        "username": "felipeacosta1",
        "weight": 82.7,
        "bmi": 27.6,
        "fat": 23.4,
        "fat_mass": 19.3
    })

if 'seccion_activa' not in st.session_state: st.session_state.seccion_activa = "Profile"
if 'profile_subview' not in st.session_state: st.session_state.profile_subview = "Main"

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "active_books": st.session_state.active_books, 
            "completed_books": st.session_state.completed_books,
            "user_profile": st.session_state.user_profile
        }, f)

# --- BASES DE DATOS ---
MEALS_DB = {
    "Monday": {"B": "2 Weetabix + 1 banana + 1 scoop Whey", "L": "250g Chicken + 110g Rice", "D": "250g Chicken + Vegetables"},
    "Tuesday": {"B": "40g oats + 1 banana", "L": "200g Beef + 250g Potato", "D": "200g White Fish"},
}
WORKOUTS = {
    "DAY 1 – UPPER (STRENGTH)": [("Barbell Bench Press (kg)", 22.5), ("Barbell Row (kg)", 17.5)]
}

# --- NAVEGACIÓN Y VISTAS PRINCIPALES ---
if st.session_state.seccion_activa == "Profile":
    
    # 1. VISTA PRINCIPAL DEL PERFIL
    if st.session_state.profile_subview == "Main":
        
        # Cabecera limpia con foto y nombre de usuario (sin contadores de workouts/followers)
        col_avatar, col_name, col_settings = st.columns([1, 3, 1])
        with col_avatar:
            st.markdown("👤", help="Tu foto de perfil")
        with col_name:
            st.markdown(f"### **{st.session_state.user_profile['username']}**")
        with col_settings:
            if st.button("⚙️", help="Settings"):
                st.session_state.profile_subview = "Settings"
                st.rerun()
            
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("#### Dashboard")
        
        # Las 4 Boxes / Tarjetas en cuadrícula 2x2
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

    # 2. SUBVISTA: SETTINGS (Aquí se movió la edición de usuario)
    elif st.session_state.profile_subview == "Settings":
        if st.button("⬅️ Volver al Perfil"):
            st.session_state.profile_subview = "Main"
            st.rerun()
        st.title("⚙️ Settings")
        
        st.markdown("### Editar Perfil")
        with st.form("settings_form"):
            new_name = st.text_input("Nombre de usuario", value=st.session_state.user_profile["username"])
            if st.form_submit_button("Guardar Cambios", use_container_width=True):
                st.session_state.user_profile["username"] = new_name
                save_data()
                st.success("¡Nombre de usuario actualizado con éxito!")

    # 3. SUBVISTA: STATISTICS
    elif st.session_state.profile_subview == "Statistics":
        if st.button("⬅️ Volver al Perfil"):
            st.session_state.profile_subview = "Main"
            st.rerun()
        st.title("📈 Statistics")
        st.info("Aquí verás tus gráficos de rendimiento y estadísticas de progreso.")

    # 4. SUBVISTA: MEASURES
    elif st.session_state.profile_subview == "Measures":
        if st.button("⬅️ Volver al Perfil"):
            st.session_state.profile_subview = "Main"
            st.rerun()
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

    # 5. SUBVISTA: CALENDAR
    elif st.session_state.profile_subview == "Calendar":
        if st.button("⬅️ Volver al Perfil"):
            st.session_state.profile_subview = "Main"
            st.rerun()
        st.title("📅 Calendar & Schedule")
        schedule_data = {
            "Time Window": ["07:30 – 08:00", "08:00 – 09:30", "09:30 – 10:30"],
            "Activity": ["🌅 Wake Up", "🏋️ Gym", "🍳 Breakfast"],
            "Strategy": ["No scrolling", "Consistency", "Refuel"]
        }
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

    # 6. SUBVISTA: GOALS
    elif st.session_state.profile_subview == "Goals":
        if st.button("⬅️ Volver al Perfil"):
            st.session_state.profile_subview = "Main"
            st.rerun()
        st.title("🎯 Targets & Goals")
        st.write("• Target Weight: 74 kg")
        st.write("• Target BMI: 24")
        st.write("• Target Body Fat: 13%")

elif st.session_state.seccion_activa == "Workout":
    st.title("🏋️ Workout Session")
    st.write("Sección de entrenamientos...")

elif st.session_state.seccion_activa == "Wellness":
    st.title("✨ Wellness Hub")
    st.write("Sección de bienestar...")

# --- BARRA DE NAVEGACIÓN FLOTANTE INFERIOR ---
st.markdown('<div class="fixed-dock">', unsafe_allow_html=True)
dcol1, dcol2, dcol3 = st.columns(3)
with dcol1:
    if st.button("👤 Profile", use_container_width=True): 
        st.session_state.seccion_activa = "Profile"
        st.session_state.profile_subview = "Main"
        st.rerun()
with dcol2:
    if st.button("🏋️ Workout", use_container_width=True): 
        st.session_state.seccion_activa = "Workout"
        st.rerun()
with dcol3:
    if st.button("🌿 Wellness", use_container_width=True): 
        st.session_state.seccion_activa = "Wellness"
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
