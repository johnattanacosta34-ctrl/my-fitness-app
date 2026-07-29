import streamlit as st, pandas as pd, json, os
from datetime import datetime

st.set_page_config(page_title="Daily Dashboard", page_icon="⚡", layout="centered")

# --- GENERAL DESIGN (BLACK BACKGROUND, WHITE TEXT, ORANGE CARDS) ---
st.markdown("""
    <style>
        :root { color-scheme: dark !important; }
        .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        section[data-testid="stSidebar"], #MainMenu, footer { display: none !important; }
        
        /* General texts in white */
        h1, h2, h3, h4, h5, h6, p, span, label, div { color: #FFFFFF !important; }
        
        /* Custom Orange Cards */
        .custom-card { background: linear-gradient(135deg, #FF8C42 0%, #FF701A 100%) !important; padding: 20px !important; border-radius: 16px !important; margin-bottom: 15px !important; box-shadow: 0 10px 25px rgba(255, 140, 66, 0.25) !important; border: none !important; }
        .custom-card * { color: #000000 !important; }
        .card-title { font-size: 12px !important; font-weight: 700 !important; text-transform: uppercase !important; opacity: 0.85; margin-bottom: 6px !important; }
        .card-body { font-size: 32px !important; font-weight: 800 !important; }

        /* Main buttons style */
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

# --- DATA PERSISTENCE & INITIALIZATION ---
DATA_FILE = "reading_data.json"
data = {}
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f: 
            data = json.load(f)
    except:
        data = {}

if "active_books" not in st.session_state:
    st.session_state.active_books = data.get("active_books", [
        {"title": "Straight Jacket by Matthew Todd", "read": 135, "total": 300}
    ])

if "completed_books" not in st.session_state:
    st.session_state.completed_books = data.get("completed_books", [])

default_profile = {
    "username": "Felipe Acosta",
    "weight": 81.6,
    "height": 174,
    "bmi": 27.0,
    "fat": 22.7,
    "fat_mass": 18.5,
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
        "Weight": 81.6, 
        "BMI": 27.0, 
        "Body Fat": 22.7, 
        "Body Fat Mass": 18.5
    }])

if "body_history" not in st.session_state:
    st.session_state.body_history = data.get("body_history", [{
        "Date": "2026-03-01", 
        "Chest": 100.0, 
        "Shoulders": 115.0, 
        "Arms": 35.0, 
        "Waist": 85.0, 
        "Legs": 55.0
    }])

# Plans / Custom Workout Plan state initialization
if "plans_data" not in st.session_state:
    st.session_state.plans_data = data.get("plans_data", {
        "plan_name": "Felipe workout",
        "days": {
            "Monday": {"name": "Upper Body", "type": "Workout", "exercises": [
                {"name": "Barbell Bench Press", "sets": 4, "reps": "12", "wt": "23,5"},
                {"name": "Chest-Supported T-Bar Ro", "sets": 4, "reps": "12", "wt": "50"},
                {"name": "Incline Dumbbell Press", "sets": 4, "reps": "12", "wt": "26"},
                {"name": "Lat Pulldown", "sets": 4, "reps": "12", "wt": "57"},
                {"name": "Biceps Curl", "sets": 4, "reps": "12", "wt": "18"},
                {"name": "Triceps pushdown", "sets": 4, "reps": "12", "wt": "28"},
                {"name": "Decline Bench Crunches", "sets": 3, "reps": "15", "wt": "kg"},
                {"name": "Stair Climber", "sets": 20, "reps": "Reps", "wt": "kg"}
            ]},
            "Tuesday": {"name": "Lower Body", "type": "Workout", "exercises": [
                {"name": "Barbell Squat", "sets": 4, "reps": "10", "wt": "60"},
                {"name": "Romanian Deadlift", "sets": 4, "reps": "10", "wt": "50"}
            ]},
            "Wednesday": {"name": "Cardio and Core", "type": "Workout", "exercises": [
                {"name": "Running / Treadmill", "sets": 1, "reps": "30 min", "wt": "0"}
            ]},
            "Thursday": {"name": "Push Day", "type": "Workout", "exercises": [
                {"name": "Overhead Press", "sets": 3, "reps": "10", "wt": "30"}
            ]},
            "Friday": {"name": "Pull Day", "type": "Workout", "exercises": [
                {"name": "Barbell Row", "sets": 4, "reps": "10", "wt": "40"}
            ]},
            "Saturday": {"name": "Leg Day", "type": "Workout", "exercises": [
                {"name": "Leg Press", "sets": 4, "reps": "12", "wt": "100"}
            ]},
            "Sunday": {"name": "Rest / Not set", "type": "Rest", "exercises": []}
        }
    })

if "daily_log_data" not in st.session_state:
    st.session_state.daily_log_data = data.get("daily_log_data", {
        "weight": 81.6,
        "height": 174,
        "bmi": 27.0,
        "body_fat": 22.7,
        "body_fat_mass": 18.5,
        "chest": 100.0,
        "shoulders": 115.0,
        "arms": 35.0,
        "waist": 85.0,
        "legs": 55.0,
        "water": 8,
        "steps": 10000,
        "sleep_hours": 7.5,
        "sleep_quality": 3,
        "calories": 2000,
        "protein": 150,
        "carbs": 200,
        "fat": 70,
        "reading_mins": 30,
        "notes": ""
    })

if "daily_checkin" not in st.session_state:
    st.session_state.daily_checkin = data.get("daily_checkin", {
        "water": "8 glasses",
        "sleep": "7.5 hrs",
        "steps": "10,000",
        "calories": "2000 kcal",
        "reading": "30 min",
        "mood": "3 / 5"
    })

if 'active_section' not in st.session_state: 
    st.session_state.active_section = "Dashboard"

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "active_books": st.session_state.active_books, 
            "completed_books": st.session_state.completed_books,
            "user_profile": st.session_state.user_profile,
            "weight_history": st.session_state.weight_history,
            "body_history": st.session_state.body_history,
            "plans_data": st.session_state.plans_data,
            "daily_log_data": st.session_state.daily_log_data,
            "daily_checkin": st.session_state.daily_checkin
        }, f)

WEEKDAY_NAMES_MAP = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

DIET_SCHEDULE = {
    0: {
        "Breakfast": "2 Weetabix + 1/2 banana + 200 ml oat milk + Unsweetened coffee",
        "Lunch": "200 g chicken (raw) + 220 g rice (cooked) + 150 g vegetables (cooked)",
        "Dinner": "200 g chicken or hake (raw) + 180 g potato or sweet potato (cooked) + 150 g vegetables (cooked)"
    },
    1: {
        "Breakfast": "40 g oats + 1/2 banana + 200 g light Greek yogurt + Unsweetened coffee",
        "Lunch": "180 g beef (raw) + 250 g potato (cooked) + 150 g vegetables (cooked)",
        "Dinner": "200 g chicken breast (raw) + 110 g pasta (cooked) + 150 g vegetables (cooked)"
    },
    2: {
        "Breakfast": "2 Weetabix + 1/2 banana + 200 ml oat milk + Unsweetened coffee",
        "Lunch": "200 g turkey (raw) + 220 g rice (cooked) + 150 g vegetables (cooked)",
        "Dinner": "200 g white fish (raw) + 110 g rice (cooked) + 150 g vegetables (cooked)"
    },
    3: {
        "Breakfast": "40 g oats + 1/2 banana + 200 g light Greek yogurt + Unsweetened coffee",
        "Lunch": "200 g chicken (raw) + 110 g pasta (cooked) + 150 g vegetables (cooked)",
        "Dinner": "180 g beef or turkey (raw) + 180 g potato (cooked) + 150 g vegetables (cooked)"
    },
    4: {
        "Breakfast": "2 Weetabix + 1/2 banana + 200 ml oat milk + Unsweetened coffee",
        "Lunch": "180 g beef (raw) + 220 g rice (cooked) + 150 g vegetables (cooked)",
        "Dinner": "200 g salmon or white fish (raw) + 110 g rice (cooked) + 150 g vegetables (cooked)"
    },
    5: {
        "Breakfast": "Scrambled eggs (2-3 eggs) + 2 budget sausages + Moderate pancakes with fruit + Coffee",
        "Lunch": "200 g chicken (raw) + 220 g rice (cooked) + 150 g vegetables (cooked)",
        "Dinner": "200 g chicken (raw) + 180 g potato or sweet potato (cooked) + 150 g vegetables (cooked)"
    },
    6: {
        "Breakfast": "Free-style brunch (controlled) + Coffee",
        "Lunch": "200 g white fish or chicken (raw) + 220 g rice (cooked) + 150 g vegetables (cooked)",
        "Dinner": "200 g turkey or chicken (raw) + 110 g pasta or rice (cooked) + 150 g vegetables (cooked)"
    }
}

# --- NAVIGATION BAR ---
st.markdown(f"## **Welcome, {st.session_state.user_profile['username']}**")
st.markdown("<hr style='margin: 10px 0; border-color: #2C2C2E;'>", unsafe_allow_html=True)

nav_cols = st.columns(5)
categories = ["Dashboard", "Workout", "Log", "Progress", "Plans"]

for i, cat in enumerate(categories):
    with nav_cols[i]:
        if st.button(cat, use_container_width=True, key=f"nav_btn_{cat}"):
            st.session_state.active_section = cat
            st.rerun()

st.markdown("<hr style='margin: 10px 0 20px 0; border-color: #2C2C2E;'>", unsafe_allow_html=True)

# --- 1. DASHBOARD ---
if st.session_state.active_section == "Dashboard":
    now = datetime.now()
    date_str = now.strftime("%A, %B %d")
    st.markdown(f"### {date_str}")
    
    current_hour = now.hour
    if current_hour < 12:
        greeting = "Good morning 🌅"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon ☀️"
    else:
        greeting = "Good evening 🌙"
    st.markdown(f"# **{greeting}**")
    
    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("### TODAY'S WORKOUT")
    today_name = WEEKDAY_NAMES_MAP[now.weekday()]
    today_plan_data = st.session_state.plans_data["days"].get(today_name, {"name": "Rest Day", "type": "Rest", "exercises": []})
    
    # Clean clickable button showing ONLY routine name and weekday
    if st.button(f"{today_plan_data['name']} ({today_name})", use_container_width=True, key="jump_to_workout_btn"):
        st.session_state.active_section = "Workout"
        st.rerun()

    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

    st.markdown("### DAILY CHECK-IN")
    chk = st.session_state.daily_checkin
    
    dc1, dc2 = st.columns(2)
    with dc1:
        st.markdown(f"<div class='custom-card'><div class='card-title'>Water</div><div class='card-body' style='font-size:22px !important;'>{chk.get('water', '8 glasses')}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card'><div class='card-title'>Steps</div><div class='card-body' style='font-size:22px !important;'>{chk.get('steps', '10,000')}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card'><div class='card-title'>Reading</div><div class='card-body' style='font-size:22px !important;'>{chk.get('reading', '30 min')}</div></div>", unsafe_allow_html=True)
    with dc2:
        st.markdown(f"<div class='custom-card'><div class='card-title'>Sleep</div><div class='card-body' style='font-size:22px !important;'>{chk.get('sleep', '7.5 hrs')}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card'><div class='card-title'>Calories</div><div class='card-body' style='font-size:22px !important;'>{chk.get('calories', '2000 kcal')}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='custom-card'><div class='card-title'>Mood</div><div class='card-body' style='font-size:22px !important;'>{chk.get('mood', '3 / 5')}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    st.markdown("### BODY")
    b1, b2, b3, b4 = st.columns(4)
    b1.markdown(f"<div class='custom-card'><div class='card-title'>Weight</div><div class='card-body' style='font-size:20px !important;'>{st.session_state.user_profile['weight']} kg</div></div>", unsafe_allow_html=True)
    b2.markdown(f"<div class='custom-card'><div class='card-title'>BMI</div><div class='card-body' style='font-size:20px !important;'>{st.session_state.user_profile['bmi']}</div></div>", unsafe_allow_html=True)
    b3.markdown(f"<div class='custom-card'><div class='card-title'>Body Fat</div><div class='card-body' style='font-size:20px !important;'>{st.session_state.user_profile['fat']}%</div></div>", unsafe_allow_html=True)
    b4.markdown(f"<div class='custom-card'><div class='card-title'>Body Fat Mass</div><div class='card-body' style='font-size:20px !important;'>{st.session_state.user_profile['fat_mass']} kg</div></div>", unsafe_allow_html=True)

# --- 2. WORKOUT ---
elif st.session_state.active_section == "Workout":
    st.title("🏋️ Workout Hub")
    
    now = datetime.now()
    today_name = WEEKDAY_NAMES_MAP[now.weekday()]
    today_plan = st.session_state.plans_data["days"].get(today_name, {"name": "Rest Day", "type": "Rest", "exercises": []})
    
    st.markdown(f"### Today's Routine: {today_name} ({today_plan['name']})")
    
    if today_plan["type"] == "Workout" and today_plan.get("exercises"):
        st.markdown("Complete your exercises for today below:")
        for idx, ex in enumerate(today_plan["exercises"]):
            st.markdown(f"""
                <div style="background-color: #1C1C1E; padding: 16px; border-radius: 12px; border: 1px solid #2C2C2E; margin-bottom: 12px;">
                    <h4 style="color: #FF8C42 !important; margin: 0 0 6px 0;">{idx+1}. {ex.get('name')}</h4>
                    <p style="margin: 0; color: #FFFFFF; opacity: 0.9;"><b>Target:</b> {ex.get('sets')} sets × {ex.get('reps')} reps | <b>Weight:</b> {ex.get('wt')}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"Today ({today_name}) is a Rest Day or has no exercises configured in your Plans section.")

# --- 3. LOG ---
elif st.session_state.active_section == "Log":
    now = datetime.now()
    st.title("Daily Log")

    with st.form("daily_log_styled_form"):
        # 1. Date selector for metrics/log updating
        log_date = st.date_input("Log Date", value=now.date(), key="log_date_input")

        with st.expander("👤 Body Metrics", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                log_weight = st.number_input("Weight (kg)", value=float(st.session_state.daily_log_data.get("weight", 81.6)), step=0.1, key="log_w_input")
            with col2:
                log_height = st.number_input("Height (cm)", value=int(st.session_state.daily_log_data.get("height", 174)), step=1, key="log_h_input")
            
            col3, col4 = st.columns(2)
            with col3:
                calc_bmi = round(log_weight / ((log_height / 100) ** 2), 1) if log_height > 0 else 27.0
                log_bmi = st.number_input("BMI (auto)", value=float(calc_bmi), step=0.1, key="log_bmi_input")
            with col4:
                log_body_fat = st.number_input("Body Fat %", value=float(st.session_state.daily_log_data.get("body_fat", 22.7)), step=0.1, key="log_bf_input")
            
            log_body_fat_mass = st.number_input("Body Fat Mass (kg)", value=float(st.session_state.daily_log_data.get("body_fat_mass", 18.5)), step=0.1, key="log_bfm_input")
            
            st.markdown("---")
            st.markdown("**Body Circumferences (cm)**")
            bc1, bc2, bc3, bc4, bc5 = st.columns(5)
            log_chest = bc1.number_input("Chest", value=float(st.session_state.daily_log_data.get("chest", 100.0)), step=0.5, key="log_chest_input")
            log_shoulders = bc2.number_input("Shoulders", value=float(st.session_state.daily_log_data.get("shoulders", 115.0)), step=0.5, key="log_shoulders_input")
            log_arms = bc3.number_input("Arms", value=float(st.session_state.daily_log_data.get("arms", 35.0)), step=0.5, key="log_arms_input")
            log_waist = bc4.number_input("Waist", value=float(st.session_state.daily_log_data.get("waist", 85.0)), step=0.5, key="log_waist_input")
            log_legs = bc5.number_input("Legs", value=float(st.session_state.daily_log_data.get("legs", 55.0)), step=0.5, key="log_legs_input")

        with st.expander("💧 Hydration & Steps", expanded=True):
            h_col1, h_col2 = st.columns(2)
            with h_col1:
                log_water = st.number_input("Water Intake (glasses)", value=int(st.session_state.daily_log_data.get("water", 8)), step=1, key="log_water_input")
            with h_col2:
                log_steps = st.number_input("Steps", value=int(st.session_state.daily_log_data.get("steps", 10000)), step=100, key="log_steps_input")

        with st.expander("😴 Sleep", expanded=True):
            log_sleep_hours = st.number_input("Sleep Hours", value=float(st.session_state.daily_log_data.get("sleep_hours", 7.5)), step=0.5, key="log_sleep_h_input")
            st.markdown("Sleep Quality")
            log_sleep_quality = st.slider("Sleep Quality scale", min_value=1, max_value=5, value=int(st.session_state.daily_log_data.get("sleep_quality", 3)), label_visibility="collapsed", key="log_sleep_q_input")
            st.markdown("<div style='display: flex; justify-content: space-between; font-size: 12px; opacity: 0.7;'><span>1</span><span>2</span><span>3</span><span>4</span><span>5 😐</span></div>", unsafe_allow_html=True)

        with st.expander("🥗 Nutrition & Today's Diet Plan", expanded=True):
            n_col1, n_col2 = st.columns(2)
            with n_col1:
                log_calories = st.number_input("Calories (kcal)", value=int(st.session_state.daily_log_data.get("calories", 2000)), step=50, key="log_cal_input")
            with n_col2:
                log_protein = st.number_input("Protein (g)", value=int(st.session_state.daily_log_data.get("protein", 150)), step=5, key="log_prot_input")
            
            n_col3, n_col4 = st.columns(2)
            with n_col3:
                log_carbs = st.number_input("Carbs (g)", value=int(st.session_state.daily_log_data.get("carbs", 200)), step=5, key="log_carb_input")
            with n_col4:
                log_fat = st.number_input("Fat (g)", value=int(st.session_state.daily_log_data.get("fat", 70)), step=5, key="log_fat_input")
            
            st.markdown("---")
            st.markdown(f"**Today's Diet Plan ({now.strftime('%A')})**")
            today_weekday_num = now.weekday()
            current_day_diet = DIET_SCHEDULE.get(today_weekday_num, DIET_SCHEDULE[0])
            
            st.markdown(f"• **Breakfast**: {current_day_diet['Breakfast']}")
            st.markdown(f"• **Lunch (Just for you)**: {current_day_diet['Lunch']}")
            st.markdown(f"• **Dinner (For you and your partner - With Carbohydrates)**: {current_day_diet['Dinner']}")

        with st.expander("📚 Reading", expanded=True):
            log_reading_mins = st.number_input("Minutes Read", value=int(st.session_state.daily_log_data.get("reading_mins", 30)), step=5, key="log_read_input")

        with st.expander("📝 Notes", expanded=True):
            log_notes = st.text_area("Daily Notes / Reflection", value=str(st.session_state.daily_log_data.get("notes", "")), key="log_notes_input")

        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        if st.form_submit_button("💾 Save Today's Log", use_container_width=True):
            st.session_state.daily_log_data = {
                "weight": log_weight, "height": log_height, "bmi": log_bmi,
                "body_fat": log_body_fat, "body_fat_mass": log_body_fat_mass,
                "chest": log_chest, "shoulders": log_shoulders, "arms": log_arms,
                "waist": log_waist, "legs": log_legs, "water": log_water,
                "steps": log_steps, "sleep_hours": log_sleep_hours,
                "sleep_quality": log_sleep_quality, "calories": log_calories,
                "protein": log_protein, "carbs": log_carbs, "fat": log_fat,
                "reading_mins": log_reading_mins, "notes": log_notes
            }
            
            st.session_state.user_profile.update({
                "weight": log_weight, "height": log_height, "bmi": log_bmi,
                "fat": log_body_fat, "fat_mass": log_body_fat_mass,
                "chest": log_chest, "shoulders": log_shoulders, "arms": log_arms,
                "waist": log_waist, "legs": log_legs
            })
            
            st.session_state.daily_checkin = {
                "water": f"{log_water} glasses",
                "sleep": f"{log_sleep_hours} hrs",
                "steps": f"{log_steps:,}",
                "calories": f"{log_calories} kcal",
                "reading": f"{log_reading_mins} min",
                "mood": f"{log_sleep_quality} / 5"
            }
            
            date_str_iso = log_date.strftime("%Y-%m-%d")
            
            existing_w = next((item for item in st.session_state.weight_history if item["Date"] == date_str_iso), None)
            if existing_w:
                existing_w.update({"Weight": log_weight, "BMI": log_bmi, "Body Fat": log_body_fat, "Body Fat Mass": log_body_fat_mass})
            else:
                st.session_state.weight_history.append({"Date": date_str_iso, "Weight": log_weight, "BMI": log_bmi, "Body Fat": log_body_fat, "Body Fat Mass": log_body_fat_mass})
                st.session_state.weight_history = sorted(st.session_state.weight_history, key=lambda x: x["Date"], reverse=True)
                
            existing_b = next((item for item in st.session_state.body_history if item["Date"] == date_str_iso), None)
            if existing_b:
                existing_b.update({"Chest": log_chest, "Shoulders": log_shoulders, "Arms": log_arms, "Waist": log_waist, "Legs": log_legs})
            else:
                st.session_state.body_history.append({"Date": date_str_iso, "Chest": log_chest, "Shoulders": log_shoulders, "Arms": log_arms, "Waist": log_waist, "Legs": log_legs})
                st.session_state.body_history = sorted(st.session_state.body_history, key=lambda x: x["Date"], reverse=True)
                
            save_data()
            st.success("Log and history updated successfully for " + date_str_iso + "!")

# --- 4. PROGRESS ---
elif st.session_state.active_section == "Progress":
    st.title("📈 Progress & History")

    # --- TARGETS SECTION (MOVED TO TOP) ---
    st.markdown("### 🎯 Targets")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown("""
            <div style="background-color: #1C1C1E; padding: 18px; border-radius: 16px; border: 1px solid #2C2C2E;">
                <h4 style="color: #FF8C42 !important; margin-bottom: 12px; font-size: 15px;">PHYSICAL TARGETS</h4>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>Weight</span><b>74 kg</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>BMI</span><b>24</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>Body Fat</span><b>13%</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0;"><span>Body Fat Mass</span><b>9 kg</b></div>
            </div>
        """, unsafe_allow_html=True)
        
    with t_col2:
        st.markdown("""
            <div style="background-color: #1C1C1E; padding: 18px; border-radius: 16px; border: 1px solid #2C2C2E;">
                <h4 style="color: #FF8C42 !important; margin-bottom: 12px; font-size: 15px;">BODY MEASUREMENTS TARGETS</h4>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>Cintura (Waist)</span><b>80 cm</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>Pecho (Chest)</span><b>110 cm</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>Hombro (Shoulders)</span><b>130 cm</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2C2C2E;"><span>Biceps (Arms)</span><b>42 cm</b></div>
                <div style="display: flex; justify-content: space-between; padding: 6px 0;"><span>Pierna (Legs)</span><b>60 cm</b></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    total_books_count = len(st.session_state.completed_books)
    st.markdown(f"""
        <div style="background-color: #1C1C1E; padding: 18px; border-radius: 16px; border: 1px solid #2C2C2E; text-align: center;">
            <h4 style="color: #FF8C42 !important; margin-bottom: 6px; font-size: 15px;">BOOKS READ TARGET</h4>
            <div style="font-size: 28px; font-weight: 800; color: #FFFFFF;">{total_books_count} <span style="font-size: 16px; opacity: 0.6; font-weight: 400;">/ 12 Goal</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("### 📊 Measures History")
    if st.session_state.weight_history:
        df_weight = pd.DataFrame(st.session_state.weight_history)
        st.dataframe(df_weight, use_container_width=True, hide_index=True)
    else:
        st.info("No primary metrics history available.")

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("### 📏 Body Metric History")
    if st.session_state.body_history:
        df_body = pd.DataFrame(st.session_state.body_history)
        st.dataframe(df_body, use_container_width=True, hide_index=True)
    else:
        st.info("No body measurements history available.")

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # --- READING SECTION ---
    st.markdown("### 📚 Books Read Tracker")
    st.markdown("Add books you've read or are currently reading. Completing them updates your total count instantly.")

    col_bk1, col_bk2 = st.columns([3, 1])
    with col_bk1:
        new_book_title = st.text_input("New book title", placeholder="e.g., Atomic Habits by James Clear", key="inline_new_book_title", label_visibility="collapsed")
    with col_bk2:
        if st.button("➕ Add Book", use_container_width=True, key="inline_add_book_btn"):
            if new_book_title.strip():
                st.session_state.completed_books.append(new_book_title.strip())
                save_data()
                st.rerun()

    st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

    if st.session_state.completed_books:
        st.markdown("**Completed Books:**")
        for i, cb in enumerate(st.session_state.completed_books):
            b_col1, b_col2 = st.columns([4, 1])
            with b_col1:
                st.markdown(f"<p style='margin: 4px 0; color: #FFFFFF;'>✓ {cb}</p>", unsafe_allow_html=True)
            with b_col2:
                if st.button("🗑️", key=f"del_book_{i}"):
                    st.session_state.completed_books.pop(i)
                    save_data()
                    st.rerun()
    else:
        st.info("No books logged yet. Add your completed books above!")

# --- 5. PLANS ---
elif st.session_state.active_section == "Plans":
    st.title("Plans")
    
    plans = st.session_state.plans_data
    
    c_p1, c_p2, c_p3 = st.columns([3, 1, 1])
    with c_p1:
        st.markdown(f"### **{plans['plan_name']}**")
    with c_p2:
        if st.button("✓ Set Active", key="set_active_plan_main"):
            st.success("Plan set as active!")
    with c_p3:
        if st.button("🗑️", key="delete_plan_main"):
            st.info("Plan active")
            
    st.markdown("<div style='background-color: #1C1C1E; padding: 20px; border-radius: 16px; border: 1px solid #2C2C2E; margin-bottom: 25px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #8E8E93;'>WEEKLY SCHEDULE</p>", unsafe_allow_html=True)
    
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_abbrs = ["M", "T", "W", "T", "F", "S", "S"]
    
    scols = st.columns(7)
    for i, d_name in enumerate(days_list):
        day_info = plans["days"].get(d_name, {"name": "Rest", "type": "Rest"})
        short_label = day_info["name"][:3].upper() if day_info["type"] == "Workout" else "-"
        with scols[i]:
            st.markdown(f"""
                <div style="text-align: center; padding: 10px 4px; background-color: #2C2C2E; border-radius: 12px; margin-bottom: 6px;">
                    <div style="font-weight: 700; font-size: 14px; margin-bottom: 6px;">{day_abbrs[i]}</div>
                    <div style="background-color: {'#34C759' if day_info['type']=='Workout' else '#48484A'}; color: #FFFFFF; font-size: 10px; font-weight: 700; padding: 6px 2px; border-radius: 8px; word-break: break-all;">{short_label}</div>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
        <div style="display: flex; gap: 15px; font-size: 12px; margin-top: 10px; opacity: 0.8;">
            <span>🟢 Workout</span>
            <span>⚪ Rest</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### **Schedule Days & Exercises**")
    
    for d_name in days_list:
        d_data = plans["days"][d_name]
        ex_count = len(d_data.get("exercises", []))
        summary_text = f"{d_data['name']} · {ex_count} exercises" if d_data['type'] == 'Workout' else f"{d_data['name']} / Not set"
        
        with st.expander(f"{d_name.upper()}  —  {summary_text}"):
            if st.button(f"+ Add Exercise ({d_name})", key=f"add_btn_{d_name}"):
                if "exercises" not in d_data:
                    d_data["exercises"] = []
                d_data["exercises"].append({"name": "New Exercise", "sets": 3, "reps": "12", "wt": "kg"})
                save_data()
                st.rerun()

            with st.form(f"form_day_{d_name}_live"):
                new_day_name = st.text_input("Workout Name", value=d_data['name'], key=f"wname_{d_name}")
                new_day_type = st.selectbox("Day Type", ["Workout", "Rest"], index=0 if d_data['type']=="Workout" else 1, key=f"wtype_{d_name}")
                
                updated_exercises = []
                if new_day_type == "Workout":
                    st.markdown("#### Exercises")
                    exercises = d_data.get("exercises", [])
                    
                    for idx, ex in enumerate(exercises):
                        col_e1, col_e2, col_e3, col_e4 = st.columns([3, 1, 1, 1])
                        with col_e1:
                            ex_n = st.text_input(f"Exercise {idx+1}", value=ex.get("name", ""), key=f"{d_name}_ex_n_{idx}")
                        with col_e2:
                            ex_s = st.number_input(f"Sets", value=int(ex.get("sets", 3)), key=f"{d_name}_ex_s_{idx}")
                        with col_e3:
                            ex_r = st.text_input(f"Reps", value=str(ex.get("reps", "12")), key=f"{d_name}_ex_r_{idx}")
                        with col_e4:
                            ex_w = st.text_input(f"Wt", value=str(ex.get("wt", "kg")), key=f"{d_name}_ex_w_{idx}")
                        
                        updated_exercises.append({"name": ex_n, "sets": ex_s, "reps": ex_r, "wt": ex_w})
                        
                if st.form_submit_button(f"Save {d_name} Changes", use_container_width=True):
                    plans["days"][d_name] = {
                        "name": new_day_name,
                        "type": new_day_type,
                        "exercises": updated_exercises if new_day_type == "Workout" else []
                    }
                    save_data()
                    st.success(f"{d_name} saved successfully!")
