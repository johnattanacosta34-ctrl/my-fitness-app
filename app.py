import streamlit as st
import pandas as pd
import json
import os

# --- DATA PERSISTENCE ---
DATA_FILE = "reading_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # Default data if file doesn't exist
    return {
        "active_books": {
            "Straight Jacket by Matthew Todd": {"read": 135, "total": 300},
            "Murder in the Dressing Room": {"read": 30, "total": 300},
            "Heated Rivalry by Rachel Reid": {"read": 255, "total": 300},
            "Game Changer by Rachel Reid": {"read": 0, "total": 300},
            "Long Game by Rachel Reid": {"read": 0, "total": 300}
        },
        "completed_books": []
    }

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "active_books": st.session_state.active_books,
            "completed_books": st.session_state.completed_books
        }, f)

# Initialize Session State
if "data_loaded" not in st.session_state:
    data = load_data()
    st.session_state.active_books = data["active_books"]
    st.session_state.completed_books = data["completed_books"]
    st.session_state.data_loaded = True
    

# --- CUSTOM THEME ---
# --- CUSTOM THEME ---
st.markdown("""
    <style>
    /* Main App Background & Text */
    .stApp { background-color: #FFF5E5; color: #2D3748; }
    
    /* Main Titles (Deep Teal) */
    h1 { color: #006D77 !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Subheadings (Deep Violet) */
    h2, h3 { color: #5B21B6 !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #FAFAFA !important; border-right: 2px solid #FF8C42 !important; }
    
    /* Custom Metric Cards */
    .custom-card { background: linear-gradient(145deg, #FFFFFF, #F7F3E9); border-left: 5px solid #FF8C42; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .card-title { color: #5B21B6; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px; }
    .card-body { color: #2D3748; font-size: 28px; font-weight: 800; margin-bottom: 4px; }
    .card-sub { color: #006D77; font-size: 13px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
st.sidebar.markdown("<h2 style='color: #ff007f !important; text-align: center;'>⚡ MY SPACE</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("GO TO:", ["📅 MY DAY", "🏋️ WORKOUTS", "🍳 NUTRITION PLAN", "📚 READING LIST", "📏 MY GOALS"])

# --- PAGE 1: MY DAY ---
if page == "📅 MY DAY":
    st.title("📅 My Day")
    schedule_data = {
        "Time Window": ["07:30 AM – 08:00 AM", "08:00 AM – 09:30 AM", "09:30 AM – 10:30 AM", "10:30 AM – 12:00 PM", "12:00 PM – 01:00 PM", "01:00 PM – 02:30 PM", "02:30 PM – 03:00 PM", "03:00 PM – 04:30 PM", "04:30 PM – 06:00 PM", "06:00 PM – 06:45 PM", "06:45 PM onwards"],
        "Activity": ["🌅 Wake Up & Prep", "🏋️ Gym Session", "🍳 Shower & Breakfast", "💼 Block 1: Job Applications", "🍽️ Lunch Break / Cooking", "🐍 Block 2: SQL & Python", "☕ Mandatory Break", "🛠️ Block 3: The Difficult Project", "📚 Guilt-Free Reading", "👟 Walk to Pick Up mi marido", "📺 Dinner & Free Time"],
        "Strategy": ["No phone scrolling!", "Keep up the consistency.", "Refuel & transition.", "Apply 2-3 targeted roles.", "Mon/Wed/Fri: Cook. Tue/Thu/Sat: Leftovers.", "Learn new concepts.", "Step away from the screen.", "Work on ONE micro-task.", "Hit that 12-book goal!", "Fresh air and steps.", "Total guilt-free zone!"]
    }
    st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)


# --- PAGE 2: WORKOUTS ---
elif page == "🏋️ WORKOUTS":
    st.title("🏋️ Workouts")
    day = st.selectbox("CHOOSE DAY:", ["DAY 1 – UPPER (STRENGTH)", "DAY 2 – LOWER (STRENGTH)", "DAY 3 – CARDIO + CORE", "DAY 4 – PUSH (CHEST + SHOULDERS)", "DAY 5 – PULL (V-TAPER)", "DAY 6 – LEGS + CONDITIONING"])
    st.markdown("---")
    if day == "DAY 1 – UPPER (STRENGTH)":
        st.subheader("💪 Upper Body Strength Focus")
        w_bench = st.number_input("Barbell Bench Press — 4x5–8 (kg):", value=22.5, step=0.5)
        w_row = st.number_input("Barbell Row — 4x6–8 (kg):", value=17.5, step=0.5)
        st.markdown("---")
        w_inc = st.number_input("Incline Dumbbell Press — 3x8–10 (kg):", value=26.0, step=0.5)
        w_lat = st.number_input("Lat Pulldown / Pull-ups — 3x8–10 (kg):", value=57.0, step=0.5)
        w_curl = st.number_input("🔥 Biceps Curl — 3x10-12 (kg):", value=18.0, step=0.5)
        w_tri = st.number_input("🔥 Triceps Pushdown — 3x10-12 (kg):", value=28.0, step=0.5)
        w_crunch = st.number_input("🔥 Cable Crunch — 3x12-15", value=28.0, step=0.5)
        st.checkbox("Cardio: 20 min Stairmaster or Treadmill")
    elif day == "DAY 2 – LOWER (STRENGTH)":
        st.subheader("🦵 Lower Body Strength Focus")
        w_squat = st.number_input("Barbell Squat — 4x5–8 (kg):", value=25.0, step=0.5)
        w_rdl = st.number_input("Romanian Deadlift — 4x6–10 (kg):", value=25.0, step=0.5)
        st.markdown("---")
        w_press = st.number_input("Leg Press — 3x10–12 (kg):", value=35.0, step=0.5)
        w_lcurl = st.number_input("Leg Curl — 3x10–12 (kg):", value=52.0, step=0.5)
        w_calf = st.number_input("Calf Raises — 3x12–15 (kg):", value=79.0, step=0.5)
        st.checkbox("Core: Hanging Leg Raise")
        st.checkbox("Core: Plank")
        st.checkbox("Cardio: 10 min Stairmaster or Treadmill")
    elif day == "DAY 3 – CARDIO + CORE":
        st.subheader("🟨 Cardio & Definition Core Day")
        st.checkbox("Cardio: 30–40 min Incline Walk (Zone 2)")
        st.checkbox("Abs: Cable Crunch — 3x12–15")
        st.checkbox("Abs: Hanging Leg Raise — 3x10–12")
        st.checkbox("Abs: Plank — 3×60 s")
    elif day == "DAY 4 – PUSH (CHEST + SHOULDERS)":
        st.subheader("🟩 Push Day Hypertrophy")
        w_inc_b = st.number_input("Incline Barbell Press — 4x6–10 (kg):", value=20.0, step=0.5)
        w_sh_p = st.number_input("Dumbbell Shoulder Press — 3x8-10 (kg):", value=36.0, step=0.5)
        st.markdown("---")
        w_db_b = st.number_input("Dumbbell Bench Press — 3x8–10 (kg):", value=26.0, step=0.5)
        w_tri_p = st.number_input("Triceps Dips or Pushdown — 3x10–12 (kg):", value=28.0, step=0.5)
        w_db_c = st.number_input("Dumbbell Curl — 3x10–12 (kg):", value=18.0, step=0.5)
        w_cb_f = st.number_input("Cable Flyes — 3x12–15 (kg):", value=18.0, step=0.5)
        w_l_r = st.number_input("Lateral Raises — 4x12–20 (kg):", value=18.0, step=0.5)
        w_d_t = st.number_input("Dumbbell Triceps Extension (kg):", value=18.0, step=0.5)
        st.checkbox("Cardio: 20 min Stairmaster or Treadmill")
    elif day == "DAY 5 – PULL (V-TAPER)":
        st.subheader("🟧 Pull & V-Taper Aesthetics")
        w_lat_p = st.number_input("Lat Pulldown — 4x8–12 (kg):", value=52.0, step=0.5)
        w_s_row = st.number_input("Seated Cable Row — 3x8–12 (kg):", value=52.0, step=0.5)
        st.markdown("---")
        w_b_row = st.number_input("Barbell Row — 3x6–10 (kg):", value=15.0, step=0.5)
        w_face = st.number_input("Face Pulls — 3x12–15 (kg):", value=19.0, step=0.5)
        w_rdelt = st.number_input("Rear Delt Flyes — 3x12–15 (kg):", value=45.0, step=0.5)
        w_lat_r = st.number_input("Lateral Raises — 3×15-20 (kg):", value=32.0, step=0.5)
        w_h_curl = st.number_input("Hammer Curl — 3x10–12 (kg):", value=16.0, step=0.5)
        w_ez_curl = st.number_input("EZ Bar Curl — 3x8–10 (kg):", value=25.0, step=0.5)
        st.checkbox("Cardio: 20 min Stairmaster or Treadmill")
    elif day == "DAY 6 – LEGS + CONDITIONING":
        st.subheader("🟪 Lower Body & Conditioning")
        w_d = st.number_input("Deadlift or RDL — 3x5–8 (kg):", value=12.5, step=0.5)
        w_lunge = st.number_input("Lunges — 3x10 per leg (kg):", value=12.5, step=0.5)
        w_ext = st.number_input("Leg Extension — 3x10–12 (kg):", value=59.0, step=0.5)
        w_lcurl6 = st.number_input("Leg Curl — 3x10–12 (kg):", value=41.0, step=0.5)
        w_scalf = st.number_input("Seated Calf Raise — 4×12-15 (kg):", value=73.0, step=0.5)
        w_calves = st.number_input("Calves — 3x12–15 (kg):", value=41.0, step=0.5)
        st.checkbox("Cardio: 12 - 18 min")
        st.checkbox("Abs: Cable Crunch 3x 12-15")
    if st.button("Lock In Session Lifts"): st.success("Weights locked in!")


# --- PAGE 3: NUTRITION PLAN ---
elif page == "🍳 NUTRITION PLAN":
    st.title("🍳 Nutrition Plan")
    chosen_day = st.radio("SELECT DAY TO VIEW MEALS:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], horizontal=True)
    meals_database = {
        "Monday": {"B": "2 Weetabix + 1 banana + 1 scoop Whey + Black coffee", "L": "250g Chicken + 110g Rice + Vegetables", "D": "250g Chicken + Vegetables"},
        "Tuesday": {"B": "40g oats + 1 banana + 1 scoop Whey OR 200g Greek yogurt + Coffee", "L": "200g Beef + 250g Potato + Vegetables", "D": "200g White Fish + Vegetables"},
        "Wednesday": {"B": "2 Weetabix + 1 banana + 1 scoop Whey + Black coffee", "L": "250g Turkey + 110g Rice + Vegetables", "D": "200g Salmon + Salad"},
        "Thursday": {"B": "40g oats + 1 banana + 1 scoop Whey OR 200g Greek yogurt + Coffee", "L": "250g Chicken + 110g Pasta + Vegetables", "D": "200g Hake Fish + Vegetables"},
        "Friday": {"B": "2 Weetabix + 1 banana + 1 scoop Whey + Black coffee", "L": "200g Beef + 110g Rice + Salad", "D": "250g Chicken + Vegetables"},
        "Saturday": {"B": "250g Chicken + 110g Rice + Vegetables", "L": "250g Chicken + 110g Rice + Vegetables", "D": "200g Salmon + Salad"},
        "Sunday": {"B": "250g Chicken/Turkey + 110g Rice + Vegetables", "L": "250g Chicken/Turkey + 110g Rice + Vegetables", "D": "200g White Fish + Vegetables"}
    }
    day_meals = meals_database[chosen_day]
    st.markdown(f"<div class='custom-card'><div class='card-title'>🍳 Breakfast</div><div class='card-body' style='font-size:16px; font-weight:normal;'>{day_meals['B']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-card'><div class='card-title'>🍽️ Lunch</div><div class='card-body' style='font-size:16px; font-weight:normal;'>{day_meals['L']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-card'><div class='card-title'>🥩 Dinner</div><div class='card-body' style='font-size:16px; font-weight:normal;'>{day_meals['D']}</div></div>", unsafe_allow_html=True)
    st.subheader("🧮 Custom Recipe Calculator")
    kcal_lookup = {"chicken breast": {"cal": 165, "pro": 31}, "rice": {"cal": 130, "pro": 2.7}, "oats": {"cal": 389, "pro": 16.9}, "whey protein": {"cal": 400, "pro": 80}, "beef": {"cal": 250, "pro": 26}, "turkey": {"cal": 135, "pro": 30}, "greek yogurt": {"cal": 59, "pro": 10}, "pasta": {"cal": 131, "pro": 5}, "potato": {"cal": 77, "pro": 2}, "salmon": {"cal": 208, "pro": 20}, "weetabix": {"cal": 362, "pro": 12}, "banana": {"cal": 89, "pro": 1.1}, "vegetables": {"cal": 35, "pro": 2}}
    ing_choice = st.selectbox("Pick Ingredient:", list(kcal_lookup.keys()))
    ing_weight = st.number_input("Grams (g):", value=100, step=10)
    calc_c = (kcal_lookup[ing_choice]["cal"] / 100) * ing_weight
    calc_p = (kcal_lookup[ing_choice]["pro"] / 100) * ing_weight
    st.info(f"✨ **Current Estimate for {ing_weight}g of {ing_choice.title()}:** ~{round(calc_c)} Calories | ~{round(calc_p, 1)}g Protein")


# --- PAGE 4: READING LIST ---
elif page == "📚 READING LIST":
    st.title("📚 Reading Rotation Tracker")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown(f"<div class='custom-card'><div class='card-title'>Active Queue</div><div class='card-body'>{len(st.session_state.active_books)}</div></div>", unsafe_allow_html=True)
    with col_b2:
        st.markdown(f"<div class='custom-card' style='border-left: 5px solid #ff007f;'><div class='card-title'>Completed</div><div class='card-body'>{len(st.session_state.completed_books)}</div></div>", unsafe_allow_html=True)
    
    st.subheader("➕ Add a New Book")
    with st.form("book_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1: title = st.text_input("Book Title")
        with c2: total = st.number_input("Total Pages", min_value=1, value=300)
        with c3: read = st.number_input("Pages Read", min_value=0, value=0)
        if st.form_submit_button("Add to Rotation"):
            if title:
                st.session_state.active_books[title] = {"read": read, "total": total}
                save_data()
                st.rerun()

    st.subheader("📖 Books Currently in Rotation")
    for book in list(st.session_state.active_books.keys()):
        data = st.session_state.active_books[book]
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1: st.markdown(f"**{book}**")
        with col2: new_read = st.number_input("Pages Read", value=data['read'], key=f"read_{book}", label_visibility="collapsed")
        with col3:
            pct = int((new_read / data['total']) * 100)
            st.write(f"{pct}% complete")
        if new_read != data['read']:
            if new_read >= data['total']:
                del st.session_state.active_books[book]
                st.session_state.completed_books.append(book)
                save_data()
                st.balloons()
            else:
                st.session_state.active_books[book]['read'] = new_read
                save_data()
            st.rerun()
            
    st.subheader("🏆 Completed History")
    for book in st.session_state.completed_books: st.write(f"• {book}")


# --- PAGE 5: MY GOALS ---
elif page == "📏 MY GOALS":
    st.title("📏 My Goals")
    c1, c2, c3, c4 = st.columns(4)
    with c1: cur_w = st.number_input("Weight (kg):", value=82.7, step=0.1)
    with c2: cur_bmi = st.number_input("BMI Value:", value=27.6, step=0.1)
    with c3: cur_bf = st.number_input("Body Fat %:", value=23.4, step=0.1)
    with c4: cur_bfm = st.number_input("Fat Mass (kg):", value=19.3, step=0.1)
    st.markdown("### 🏆 Goals")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='custom-card'><div class='card-title'>Weight Target</div><div class='card-body'>{cur_w} kg</div><div class='card-sub'>GOAL: 74.0 kg</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='custom-card'><div class='card-title'>BMI Target</div><div class='card-body'>{cur_bmi}</div><div class='card-sub'>GOAL: 24.0</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='custom-card'><div class='card-title'>Body Fat Target</div><div class='card-body'>{cur_bf}%</div><div class='card-sub'>GOAL: 13%</div></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='custom-card'><div class='card-title'>Fat Mass Target</div><div class='card-body'>{cur_bfm} kg</div><div class='card-sub'>GOAL: 9.0 kg</div></div>", unsafe_allow_html=True)
    st.subheader("📐 Tape Measurement Timeline (cm)")
    c_w1, c_w2, c_w3, c_w4, c_w5 = st.columns(5)
    with c_w1: in_cint = st.number_input("Waist Input:", value=89, step=1)
    with c_w2: in_pech = st.number_input("Chest Input:", value=109, step=1)
    with c_w3: in_homb = st.number_input("Shoulders Input:", value=125, step=1)
    with c_w4: in_bice = st.number_input("Biceps Input:", value=39, step=1)
    with c_w5: in_pier = st.number_input("Legs Input:", value=59, step=1)
    measures_df = pd.DataFrame({
        "Body Part": ["Waist", "Chest", "Shoulders", "Biceps", "Legs"],
        "4/4/2026": [95, 105, 127, 39, 59],
        "1/6/2026": [92, 105, 125, 38, 59],
        "17/06/2026": [89, 109, 125, 39, 59],
        "Your Current Entry": [in_cint, in_pech, in_homb, in_bice, in_pier],
        "META TARGET": [80, 110, 130, 42, 60]
    })
    st.dataframe(measures_df, use_container_width=True, hide_index=True)
    st.subheader("📅 Projected Progress Timeline")
    timeline_data = {
        "Date Expected": ["July 22, 2026", "August 12, 2026", "September 9, 2026", "October 7, 2026", "November 11, 2026"],
        "Milestone Target": ["Week 2", "Week 5 (Month 1)", "Week 9 (Month 2)", "Week 13 (Month 3)", "Week 18 (META GOAL)"],
        "Estimated Weight Goal": ["81.7 kg", "80.7 kg", "78.7 kg", "76.7 kg", "74.0 kg"],
        "Visual Changes & Milestones": ["Body debloats, fluid retention from June drops away.", "Waist approaching 87 cm. Strength metrics remain stable.", "Drastic change in the mirror. Waist around 84-85 cm; love handles fade.", "Arm vascularity showing up due to supersets. Waist around 81-82 cm.", "13% Body Fat Achieved. Lean athletic condition. Optimal waist at 78-79 cm."]
    }
    st.dataframe(pd.DataFrame(timeline_data), use_container_width=True, hide_index=True)

