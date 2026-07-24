import streamlit as st, pandas as pd, json, os
from datetime import datetime

st.set_page_config(page_title="Daily Dashboard", page_icon="⚡", layout="centered")

# --- DISEÑO GENERAL (FONDO NEGRO, LETRAS BLANCAS, CAJAS NARANJAS) ---
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

        /* Estilo para los botones principales (compactos en 3 columnas) */
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

# --- PERSISTENCIA DE DATOS Y CORRECCIÓN DE ESTADOS FALTANTES ---
DATA_FILE = "reading_data.json"
data = {}
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f: 
            data = json.load(f)
    except:
        data = {}

if "active_books" not in st.session_state:
    st.session_state.active_books = data.get("active_books", {
        "Straight Jacket by Matthew Todd": {"read": 135, "total": 300},
        "Heated Rivalry by Rachel Reid": {"read": 255, "total": 300}
    })

if "completed_books" not in st.session_state:
    st.session_state.completed_books = data.get("completed_books", [])

default_profile = {
    "username": "Felipe Acosta",
    "weight": 82.7,
    "bmi": 27.6,
    "fat": 23.4,
    "fat_mass": 19.3,
    "waist": 85.0,
    "chest": 100.0,
    "shoulders": 115.0,
    "arms": 35.0,
    "legs": 55.0
}

if "user_profile" not in st.session_state:
    loaded_profile = data.get("user_profile", {})
    st.session_state.user_profile = {**default_profile, **loaded_profile}
else:
    for k, v in default_profile.items():
        if k not in st.session_state.user_profile:
            st.session_state.user_profile[k] = v

if "weight_history" not in st.session_state:
    st.session_state.weight_history = data.get("weight_history", [{
        "Date": "2026-03-01", 
        "Weight": 82.7, 
        "BMI": 27.6, 
        "Body Fat": 23.4, 
        "Body Fat Mass": 19.3
    }])
else:
    for entry in st.session_state.weight_history:
        if "fat%" in entry:
            entry["Body Fat"] = entry.pop("fat%")
        if "fat_mass" in entry and "Body Fat Mass" not in entry:
            entry["Body Fat Mass"] = entry.pop("fat_mass")

if "body_history" not in st.session_state:
    st.session_state.body_history = data.get("body_history", [{
        "Date": "2026-03-01", 
        "Chest": 100.0, 
        "Shoulders": 115.0, 
        "Arms": 35.0, 
        "Waist": 85.0, 
        "Legs": 55.0
    }])
else:
    # Limpiar columnas adicionales indeseadas en historiales cargados previamente
    desired_body_cols = ["Date", "Chest", "Shoulders", "Arms", "Waist", "Legs"]
    for entry in st.session_state.body_history:
        keys_to_remove = [k for k in entry.keys() if k not in desired_body_cols]
        for k in keys_to_remove:
            del entry[k]

if "physical_goals" not in st.session_state:
    st.session_state.physical_goals = data.get("physical_goals", "• Bajar a 74 kg\n• Reducir porcentaje de grasa a 13%\n• Aumentar masa muscular en hombros")

if "mental_goals" not in st.session_state:
    st.session_state.mental_goals = data.get("mental_goals", "• Meditar 10 minutos diarios\n• Leer 20 páginas al día\n• Mantener consistencia sin distracciones")

if 'seccion_activa' not in st.session_state: st.session_state.seccion_activa = "Home"
if 'profile_subview' not in st.session_state: st.session_state.profile_subview = "Main"
if 'workout_subview' not in st.session_state: st.session_state.workout_subview = "Main"
if 'wellness_subview' not in st.session_state: st.session_state.wellness_subview = "Main"

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "active_books": st.session_state.active_books, 
            "completed_books": st.session_state.completed_books,
            "user_profile": st.session_state.user_profile,
            "weight_history": st.session_state.weight_history,
            "body_history": st.session_state.body_history,
            "physical_goals": st.session_state.physical_goals,
            "mental_goals": st.session_state.mental_goals
        }, f)

# --- BASES DE DATOS ---
WORKOUTS = {
    "DÍA 1: PUSH (Pecho, Hombro, Tríceps)": [
        ("Press de Banca con Barra", "4 series x 8-10 reps"),
        ("Press Militar con Mancuernas", "3 series x 10 reps"),
        ("Aperturas en Polea", "3 series x 12 reps"),
        ("Extensiones de Tríceps en Polea", "3 series x 12 reps")
    ],
    "DÍA 2: PULL (Espalda, Bíceps)": [
        ("Dominadas / Jalón al Pecho", "4 series x 8-10 reps"),
        ("Remo con Barra", "3 series x 8-10 reps"),
        ("Remo en Polea Baja", "3 series x 12 reps"),
        ("Curl de Bíceps con Mancuerna", "3 series x 12 reps")
    ],
    "DÍA 3: LEGS (Pierna Completa)": [
        ("Sentadilla Libre", "4 series x 6-8 reps"),
        ("Peso Muerto Rumano", "3 series x 8-10 reps"),
        ("Prensa de Piernas", "3 series x 10-12 reps"),
        ("Curl de Isquios / Extensiones", "3 series x 15 reps")
    ],
    "DÍA 4: UPPER (Torso Completo)": [
        ("Press Inclinado con Mancuernas", "4 series x 8-10 reps"),
        ("Remo Pendlay o en T", "3 series x 8 reps"),
        ("Elevaciones Laterales", "4 series x 15 reps"),
        ("Curl de Bíceps Martillo", "3 series x 12 reps")
    ]
}

DIET_PLAN = {
    "Comida 1 (Desayuno)": "Omelette de 3 claras y 1 huevo entero, 50g de avena con frutos rojos y café negro.",
    "Comida 2 (Almuerzo)": "200g de pechuga de pollo o carne magra, 150g de arroz blanco o integral, vegetales al vapor.",
    "Comida 3 (Pre-entreno)": "Yogur griego natural con una porción de fruta y un puñado de almendras.",
    "Comida 4 (Cena)": "200g de pescado blanco o salmón, ensalada verde grande con aceite de oliva y aguacate."
}

# --- NAVEGACIÓN PRINCIPAL ---

if st.session_state.seccion_activa == "Home":
    
    col_name, col_settings = st.columns([4, 1])
    with col_name:
        st.markdown(f"## **{st.session_state.user_profile['username']}**")
    with col_settings:
        if st.button("⚙️", help="Settings"):
            st.session_state.seccion_activa = "Settings"
            st.rerun()
        
    st.markdown("<hr style='margin: 15px 0; border-color: #2C2C2E;'>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.seccion_activa = "Profile"
            st.session_state.profile_subview = "Main"
            st.rerun()
    with c2:
        if st.button("🏋️ Workout", use_container_width=True):
            st.session_state.seccion_activa = "Workout"
            st.session_state.workout_subview = "Main"
            st.rerun()
    with c3:
        if st.button("✨ Wellness", use_container_width=True):
            st.session_state.seccion_activa = "Wellness"
            st.session_state.wellness_subview = "Main"
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

# SECCIÓN PROFILE
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
            if st.button("📏 Measures", use_container_width=True):
                st.session_state.profile_subview = "Measures"
                st.rerun()
            if st.button("🎯 Goals", use_container_width=True):
                st.session_state.profile_subview = "Goals"
                st.rerun()
        with b_col2:
            if st.button("📈 Statistics", use_container_width=True):
                st.session_state.profile_subview = "Statistics"
                st.rerun()
            if st.button("📅 Calendar", use_container_width=True):
                st.session_state.profile_subview = "Calendar"
                st.rerun()

    elif st.session_state.profile_subview == "Measures":
        st.title("📏 Measures & Body Metrics")
        
        # 1. BLOQUE DE MÉTRICAS PRINCIPALES
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='custom-card'><div class='card-title'>Weight</div><div class='card-body'>{st.session_state.user_profile['weight']}</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='custom-card'><div class='card-title'>BMI</div><div class='card-body'>{st.session_state.user_profile['bmi']}</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='custom-card'><div class='card-title'>Body Fat</div><div class='card-body'>{st.session_state.user_profile['fat']}%</div></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='custom-card'><div class='card-title'>Body Fat Mass</div><div class='card-body'>{st.session_state.user_profile['fat_mass']}</div></div>", unsafe_allow_html=True)

        with st.form("measures_form"):
            st.subheader("Actualizar Métricas Principales")
            meas_date = st.date_input("Fecha de registro", value=datetime.now())
            
            c1, c2, c3, c4 = st.columns(4)
            w = c1.number_input("Weight", value=float(st.session_state.user_profile["weight"]), step=0.1)
            bmi = c2.number_input("BMI", value=float(st.session_state.user_profile["bmi"]), step=0.1)
            bf = c3.number_input("Body Fat", value=float(st.session_state.user_profile["fat"]), step=0.1)
            fm = c4.number_input("Body Fat Mass", value=float(st.session_state.user_profile["fat_mass"]), step=0.1)
            
            if st.form_submit_button("Guardar Métricas Principales", use_container_width=True):
                st.session_state.user_profile.update({
                    "weight": w, "bmi": bmi, "fat": bf, "fat_mass": fm
                })
                date_str = meas_date.strftime("%Y-%m-%d")
                
                existing_entry = next((item for item in st.session_state.weight_history if item["Date"] == date_str), None)
                if existing_entry:
                    existing_entry.update({"Weight": w, "BMI": bmi, "Body Fat": bf, "Body Fat Mass": fm})
                else:
                    st.session_state.weight_history.append({
                        "Date": date_str, "Weight": w, "BMI": bmi, "Body Fat": bf, "Body Fat Mass": fm
                    })
                save_data()
                st.success("¡Métricas principales guardadas con éxito!")

        st.markdown("<hr style='margin: 30px 0; border-color: #2C2C2E;'>", unsafe_allow_html=True)

        # 2. BLOQUE DE MEDIDAS CORPORALES
        b1, b2, b3, b4, b5 = st.columns(5)
        b1.markdown(f"<div class='custom-card'><div class='card-title'>Chest</div><div class='card-body' style='font-size:22px !important;'>{st.session_state.user_profile['chest']}</div></div>", unsafe_allow_html=True)
        b2.markdown(f"<div class='custom-card'><div class='card-title'>Shoulders</div><div class='card-body' style='font-size:22px !important;'>{st.session_state.user_profile['shoulders']}</div></div>", unsafe_allow_html=True)
        b3.markdown(f"<div class='custom-card'><div class='card-title'>Arms</div><div class='card-body' style='font-size:22px !important;'>{st.session_state.user_profile['arms']}</div></div>", unsafe_allow_html=True)
        b4.markdown(f"<div class='custom-card'><div class='card-title'>Waist</div><div class='card-body' style='font-size:22px !important;'>{st.session_state.user_profile['waist']}</div></div>", unsafe_allow_html=True)
        b5.markdown(f"<div class='custom-card'><div class='card-title'>Legs</div><div class='card-body' style='font-size:22px !important;'>{st.session_state.user_profile['legs']}</div></div>", unsafe_allow_html=True)

        with st.form("body_measures_form"):
            st.subheader("Actualizar Medidas del Cuerpo")
            body_date = st.date_input("Fecha de registro (Medidas)", value=datetime.now())
            
            bc1, bc2, bc3, bc4, bc5 = st.columns(5)
            chest = bc1.number_input("Chest", value=float(st.session_state.user_profile["chest"]), step=0.5)
            shoulders = bc2.number_input("Shoulders", value=float(st.session_state.user_profile["shoulders"]), step=0.5)
            arms = bc3.number_input("Arms", value=float(st.session_state.user_profile["arms"]), step=0.5)
            waist = bc4.number_input("Waist", value=float(st.session_state.user_profile["waist"]), step=0.5)
            legs = bc5.number_input("Legs", value=float(st.session_state.user_profile["legs"]), step=0.5)
            
            if st.form_submit_button("Guardar Medidas Corporales", use_container_width=True):
                st.session_state.user_profile.update({
                    "chest": chest, "shoulders": shoulders, "arms": arms, "waist": waist, "legs": legs
                })
                date_str = body_date.strftime("%Y-%m-%d")
                
                existing_body = next((item for item in st.session_state.body_history if item["Date"] == date_str), None)
                if existing_body:
                    existing_body.update({
                        "Chest": chest, "Shoulders": shoulders, "Arms": arms, "Waist": waist, "Legs": legs
                    })
                else:
                    st.session_state.body_history.append({
                        "Date": date_str, "Chest": chest, "Shoulders": shoulders, "Arms": arms, "Waist": waist, "Legs": legs
                    })
                save_data()
                st.success("¡Medidas corporales guardadas con éxito!")

    elif st.session_state.profile_subview == "Goals":
        st.title("🎯 Targets & Goals")
        
        with st.form("goals_form"):
            st.subheader("💪 Objetivos Físicos")
            p_goals = st.text_area("Edita tus objetivos físicos:", value=st.session_state.physical_goals, height=120)
            
            st.markdown("<hr style='border-color: #2C2C2E;'>", unsafe_allow_html=True)
            st.subheader("🧠 Objetivos Personales y Mentales")
            m_goals = st.text_area("Edita tus objetivos mentales/personales:", value=st.session_state.mental_goals, height=120)
            
            if st.form_submit_button("Guardar Todos los Objetivos", use_container_width=True):
                st.session_state.physical_goals = p_goals
                st.session_state.mental_goals = m_goals
                save_data()
                st.success("¡Objetivos guardados correctamente!")

    elif st.session_state.profile_subview == "Statistics":
        st.title("📈 Statistics & History")
        
        # --- TABLA 1: MEASURES HISTORY ---
        st.subheader("📊 Measures History")
        if st.session_state.weight_history:
            df_weight = pd.DataFrame(st.session_state.weight_history)
            desired_columns = ["Date", "Weight", "BMI", "Body Fat", "Body Fat Mass"]
            for col in desired_columns:
                if col not in df_weight.columns:
                    df_weight[col] = 0.0
            df_weight = df_weight[desired_columns]
            
            df_weight["Date"] = pd.to_datetime(df_weight["Date"])
            df_weight = df_weight.sort_values(by="Date", ascending=True).reset_index(drop=True)
            df_weight["Date"] = df_weight["Date"].dt.strftime("%Y-%m-%d")
            
            st.dataframe(df_weight, use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros de métricas principales aún.")

        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # --- TABLA 2: BODY METRICS HISTORY (Estrictamente con las columnas requeridas) ---
        st.subheader("📏 Body Metrics History")
        if st.session_state.body_history:
            df_body = pd.DataFrame(st.session_state.body_history)
            
            desired_body_columns = ["Date", "Chest", "Shoulders", "Arms", "Waist", "Legs"]
            for col in desired_body_columns:
                if col not in df_body.columns:
                    df_body[col] = 0.0
            df_body = df_body[desired_body_columns]
            
            df_body["Date"] = pd.to_datetime(df_body["Date"])
            df_body = df_body.sort_values(by="Date", ascending=True).reset_index(drop=True)
            df_body["Date"] = df_body["Date"].dt.strftime("%Y-%m-%d")
            
            st.dataframe(df_body, use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros de medidas corporales aún.")

        st.markdown("<hr style='margin: 30px 0; border-color: #2C2C2E;'>", unsafe_allow_html=True)

        # --- SECCIÓN DE EDICIÓN Y ELIMINACIÓN DE REGISTROS (FUERA DE FORMULARIOS ANIDADOS) ---
        st.subheader("🛠️ Gestión de Registros (Eliminar o Actualizar)")
        
        gestion_tab = st.radio("Selecciona acción:", ["🗑️ Eliminar Registro", "✏️ Actualizar / Corregir Registro"], horizontal=True)
        
        if gestion_tab == "🗑️ Eliminar Registro":
            st.markdown("### 🗑️ Eliminar Fila")
            del_table = st.selectbox("Selecciona la tabla", ["Measures History", "Body Metrics History"], key="del_tbl_choice")
            
            if del_table == "Measures History":
                if st.session_state.weight_history:
                    dates_list = [x["Date"] for x in st.session_state.weight_history]
                    selected_del_date = st.selectbox("Fecha exacta a eliminar", dates_list, key="del_w_date")
                    if st.button("Confirmar Eliminación (Measures)", use_container_width=True):
                        st.session_state.weight_history = [x for x in st.session_state.weight_history if x["Date"] != selected_del_date]
                        save_data()
                        st.success(f"¡Registro del {selected_del_date} eliminado correctamente!")
                        st.rerun()
                else:
                    st.info("No hay registros disponibles en Measures History.")
            else:
                if st.session_state.body_history:
                    dates_list_b = [x["Date"] for x in st.session_state.body_history]
                    selected_del_b_date = st.selectbox("Fecha exacta a eliminar", dates_list_b, key="del_b_date")
                    if st.button("Confirmar Eliminación (Body Metrics)", use_container_width=True):
                        st.session_state.body_history = [x for x in st.session_state.body_history if x["Date"] != selected_del_b_date]
                        save_data()
                        st.success(f"¡Registro del {selected_del_b_date} eliminado correctamente!")
                        st.rerun()
                else:
                    st.info("No hay registros disponibles en Body Metrics History.")

        else:
            st.markdown("### ✏️ Actualizar / Corregir Fila")
            edit_table = st.selectbox("Selecciona la tabla a editar", ["Measures History", "Body Metrics History"], key="edit_tbl_choice")
            
            if edit_table == "Measures History":
                if st.session_state.weight_history:
                    edit_dates_w = [x["Date"] for x in st.session_state.weight_history]
                    chosen_w_date = st.selectbox("Selecciona Fecha", edit_dates_w, key="edit_w_sel")
                    
                    curr_w_record = next(x for x in st.session_state.weight_history if x["Date"] == chosen_w_date)
                    
                    with st.form("edit_w_form"):
                        ew = st.number_input("Weight", value=float(curr_w_record["Weight"]), step=0.1)
                        ebmi = st.number_input("BMI", value=float(curr_w_record["BMI"]), step=0.1)
                        ebf = st.number_input("Body Fat", value=float(curr_w_record["Body Fat"]), step=0.1)
                        efm = st.number_input("Body Fat Mass", value=float(curr_w_record["Body Fat Mass"]), step=0.1)
                        
                        if st.form_submit_button("Guardar Cambios Measures", use_container_width=True):
                            curr_w_record.update({
                                "Weight": ew, "BMI": ebmi, "Body Fat": ebf, "Body Fat Mass": efm
                            })
                            save_data()
                            st.success(f"¡Registro del {chosen_w_date} actualizado con éxito!")
                            st.rerun()
                else:
                    st.info("No hay registros disponibles para editar.")
            else:
                if st.session_state.body_history:
                    edit_dates_b = [x["Date"] for x in st.session_state.body_history]
                    chosen_b_date = st.selectbox("Selecciona Fecha", edit_dates_b, key="edit_b_sel")
                    
                    curr_b_record = next(x for x in st.session_state.body_history if x["Date"] == chosen_b_date)
                    
                    with st.form("edit_b_form"):
                        e_chest = st.number_input("Chest", value=float(curr_b_record["Chest"]), step=0.5)
                        e_shoulders = st.number_input("Shoulders", value=float(curr_b_record["Shoulders"]), step=0.5)
                        e_arms = st.number_input("Arms", value=float(curr_b_record["Arms"]), step=0.5)
                        e_waist = st.number_input("Waist", value=float(curr_b_record["Waist"]), step=0.5)
                        e_legs = st.number_input("Legs", value=float(curr_b_record["Legs"]), step=0.5)
                        
                        if st.form_submit_button("Guardar Cambios Body Metrics", use_container_width=True):
                            curr_b_record.update({
                                "Chest": e_chest, "Shoulders": e_shoulders, "Arms": e_arms, "Waist": e_waist, "Legs": e_legs
                            })
                            save_data()
                            st.success(f"¡Registro del {chosen_b_date} actualizado con éxito!")
                            st.rerun()
                else:
                    st.info("No hay registros disponibles para editar.")

    elif st.session_state.profile_subview == "Calendar":
        st.title("📅 Calendar & Schedule")
        schedule_data = {
            "Time Window": [
                "07:00 – 07:30", "07:30 – 08:00", "08:00 – 09:30", 
                "09:30 – 10:30", "10:30 – 13:30", "13:30 – 14:30", 
                "14:30 – 18:30", "18:30 – 19:30", "19:30 – 21:00", "21:00 – 22:30"
            ],
            "Activity": [
                "🌅 Wake Up & Hydration", "🧘 Mobility / Stretching", "🏋️ Workout Session", 
                "🍳 Breakfast & Shower", "💻 Deep Work / Focus Block", "🥗 Lunch & Rest", 
                "💻 Afternoon Tasks / Meetings", "🚶 Light Walk / Cardio", "🍽️ Dinner & Family Time", "📚 Reading & Wind Down"
            ],
            "Strategy": [
                "No screens", "Consistency", "Push limits", 
                "Refuel", "Zero distractions", "Digest", 
                "Productivity", "Step count", "Disconnect", "Sleep prep"
            ]
        }
        st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

# SECCIÓN WORKOUT
elif st.session_state.seccion_activa == "Workout":
    if st.button("⬅️ Back"):
        if st.session_state.workout_subview == "Main":
            st.session_state.seccion_activa = "Home"
        else:
            st.session_state.workout_subview = "Main"
        st.rerun()

    if st.session_state.workout_subview == "Main":
        st.title("🏋️ Workout Hub")
        
        w_col1, w_col2 = st.columns(2)
        with w_col1:
            if st.button("📋 Rutinas Completas", use_container_width=True):
                st.session_state.workout_subview = "Rutinas"
                st.rerun()
            if st.button("📊 Historial", use_container_width=True):
                st.session_state.workout_subview = "Historial"
                st.rerun()
        with w_col2:
            if st.button("⏱️ Cronómetro", use_container_width=True):
                st.session_state.workout_subview = "Cronometro"
                st.rerun()
            if st.button("🔥 Ejercicios", use_container_width=True):
                st.session_state.workout_subview = "Ejercicios"
                st.rerun()

    elif st.session_state.workout_subview == "Rutinas":
        st.title("📋 Tus Rutinas de Entrenamiento")
        for day_name, exercises in WORKOUTS.items():
            with st.expander(day_name):
                for ex_name, details in exercises:
                    st.write(f"• **{ex_name}**: {details}")

    elif st.session_state.workout_subview == "Historial":
        st.title("📊 Historial de Entrenamientos")
        st.info("Aquí puedes consultar tus registros de entrenamientos anteriores.")

    elif st.session_state.workout_subview == "Cronometro":
        st.title("⏱️ Cronómetro de Descanso")
        st.write("Controla tus tiempos de descanso entre series.")

    elif st.session_state.workout_subview == "Ejercicios":
        st.title("🔥 Biblioteca de Ejercicios")
        st.write("Guía detallada de ejecución para cada movimiento.")

# SECCIÓN WELLNESS
elif st.session_state.seccion_activa == "Wellness":
    if st.button("⬅️ Back"):
        if st.session_state.wellness_subview == "Main":
            st.session_state.seccion_activa = "Home"
        else:
            st.session_state.wellness_subview = "Main"
        st.rerun()

    if st.session_state.wellness_subview == "Main":
        st.title("✨ Wellness Hub")
        
        we_col1, we_col2 = st.columns(2)
        with we_col1:
            if st.button("🥗 Dieta / Nutrición", use_container_width=True):
                st.session_state.wellness_subview = "Dieta"
                st.rerun()
        with we_col2:
            if st.button("📚 Reading / Lectura", use_container_width=True):
                st.session_state.wellness_subview = "Reading"
                st.rerun()

    elif st.session_state.wellness_subview == "Dieta":
        st.title("🥗 Plan de Dieta y Nutrición")
        for meal_time, meal_desc in DIET_PLAN.items():
            st.markdown(f"**{meal_time}**")
            st.info(meal_desc)

    elif st.session_state.wellness_subview == "Reading":
        st.title("📚 Reading Tracker")
        
        st.subheader("📖 Libros Activos")
        for book, info in st.session_state.active_books.items():
            progress = int((info["read"] / info["total"]) * 100)
            st.write(f"**{book}** ({info['read']}/{info['total']} págs - {progress}%)")
            st.progress(progress)
            
            col_b1, col_b2 = st.columns(2)
            if col_b1.button(f"+10 Págs ({book[:10]}...)", key=f"p_{book}"):
                st.session_state.active_books[book]["read"] = min(info["total"], info["read"] + 10)
                save_data()
                st.rerun()
                
        st.markdown("---")
        st.subheader("✅ Libros Completados")
        if st.session_state.completed_books:
            for b in st.session_state.completed_books:
                st.write(f"• {b}")
        else:
            st.write("Aún no hay libros completados en la lista.")
