import streamlit as st
import numpy as np
import cv2
import pandas as pd
import base64
import sqlite3
import hashlib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# DB connect
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Table create
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    email TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

c.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    name TEXT,
    prediction REAL,
    risk TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Tooth Decay Detection System",
    page_icon="🦷",
    layout="wide"
)

# ---------------- SESSION ----------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False 

if "show_forgot" not in st.session_state:
    st.session_state.show_forgot = False    

if "reset_mode" not in st.session_state:
    st.session_state.reset_mode = False    


# ---------------- BACKGROUND ----------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{data}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- DATABASE ----------------
import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    email TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# register
def register_user(email, password):
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()

# login
def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

# ---------------- AUTH FUNCTIONS ----------------
def register_user(email, password):
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()

def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

def reset_password(email, new_password):
    c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
    conn.commit()    

def save_history(email, name, prediction, risk):
    c.execute(
        "INSERT INTO history (email, name, prediction, risk) VALUES (?, ?, ?, ?)",
        (email, name, prediction, risk)
    )
    conn.commit()    
# ---------------- MODEL ----------------
model = load_model("tooth_decay_model.keras")

# ---------------- HEATMAP FUNCTION ----------------
def show_heatmap(img):
    img = img.resize((128, 128))
    img_array = np.array(img)

    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    blended = cv2.addWeighted(img_array, 0.6, heatmap, 0.4, 0)

    st.image(blended, caption="🔥 Heatmap", use_container_width=True)

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1.5,2,1.5])

    with col2:

        # 🖼️ LOGO
        st.image("logo.jpeg", width=120)

        # 🏷️ PROJECT NAME
        st.markdown(
            "<h2 style='text-align:center;'>🦷 AI Tooth Decay Detection</h2>",
            unsafe_allow_html=True
        )

        st.write("")

        # 🔁 MODE SWITCH
        mode = st.radio("", ["Login", "Create Account"])

        # 📧 INPUTS
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")


        # ---------------- LOGIN ----------------
        if mode == "Login":

            if st.button("Login", use_container_width=True):

                user = login_user(email, password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.success("✅ Login success")
                    st.rerun()

                else:
                    st.error("❌ Wrong email or password")
                    st.session_state.show_forgot = True


            # 🔑 FORGOT PASSWORD (SHOW ONLY AFTER ERROR)
    
            if st.session_state.show_forgot:

                st.markdown("<p style='color:blue;'>Forgot Password?</p>", unsafe_allow_html=True)
                
                if st.button("Reset Password"):
                    st.session_state.reset_mode = True

            # 🔐 RESET PASSWORD INPUT (👉 IDHA INGA PODANUM)
            if st.session_state.reset_mode:

                st.markdown("### 🔐 Set New Password")

                new_pass = st.text_input("Enter New Password", type="password")
      
                if st.button("Update Password"):

                    c.execute(
                        "UPDATE users SET password=? WHERE email=?",
                        (new_pass, email)
                    )
                    conn.commit()

                    st.success("✅ Password updated successfully!")

                    st.session_state.reset_mode = False
                    st.session_state.show_forgot = False

            # 🆕 REGISTER
            if mode == "Create Account":
                if st.button("Create Account", use_container_width=True):
                    try:
                        register_user(email, password)
                        st.success("✅ Account created!")
                    except:
                        st.error("⚠️ Email already exists")        

        # ---------------- REGISTER ----------------
        else:

            if st.button("Create Account", use_container_width=True):

                try:
                    register_user(email, password)
                    st.success("✅ Account created! Now login")

                except:
                    st.error("⚠️ Email already exists")


# ❗ STOP APP UNTIL LOGIN
if not st.session_state.logged_in:
    st.stop()



# ---------------- PAGE 1 ----------------
if st.session_state.step == 1:

    set_bg("background2.jpeg")

    col1, col2, col3 = st.columns([1.5,2,1.5])

    with col2:
        st.image("logo.jpeg", width=180)
        st.markdown("<h1 style='text-align:center; color:#0A1AFF;'>🦷 AI Tooth Detection System</h1>", unsafe_allow_html=True)

        if st.button("🚀 Start",use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# ---------------- PAGE 2 ----------------
elif st.session_state.step == 2:

    set_bg("background2.jpeg")

    col1, col2, col3 = st.columns([1.5,2,1.5])
    
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        st.image("logo.jpeg", width=180)

        st.markdown("<h1 style='text-align:center; color:#0A1AFF;'>🦷 AI Tooth Detection System</h1>", unsafe_allow_html=True)

        name = st.text_input("👤 Enter your name")

        if st.button("➡️ Continue", use_container_width=True):
            if name.strip() == "":
                st.warning("⚠️ Please enter your name")
            else:
                st.session_state.username = name
                st.session_state.step = 3
                st.rerun()
# ---------------- PAGE 3 (SIDEBAR APP) ----------------
elif st.session_state.step == 3:

    st.sidebar.title("🦷 AI Tooth App")
    st.sidebar.image("logo.jpeg", width=200)

    if st.sidebar.button("⬅️ Back"):
        st.session_state.step = 2
        st.rerun()
        
    st.session_state.page = st.sidebar.radio("Navigation", ["Home", "Tooth Detection", "History", "Nearby Hospitals"])
    page = st.session_state.page

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
# ---------------- HOME ----------------
if  st.session_state.step == 3 and page == "Home":

    st.title("🦷 AI Tooth Decay Prediction System")

    st.success(f"Welcome {st.session_state.username} 👋")

    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050525.png", width=200)
    
    st.write("""
This AI-powered system helps in early dental caries screening 
using deep learning and image analysis.

The application allows users to upload or capture tooth images,
analyzes decay risk, generates visual heatmaps, and provides
basic dental care recommendations.
""")
    
    st.write("""
🚀 Features:
- Image Upload 📂  
- Camera Detection 📷  
- AI Prediction 🧠  
- Heatmap 🔥  
- Hospital Suggestion 📍  
""")

    st.success("👉 Go to Tooth Detection")

# ---------------- DETECTION ----------------
elif st.session_state.step == 3 and page == "Tooth Detection":

    st.title("🔍 Tooth Decay Detection")

    st.write("Upload a tooth image or capture using camera.")
    
    # Prediction function
    def predict_tooth(img):

        img = img.resize((128,128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        with st.spinner("Analyzing dental image using AI model..."):
            prediction = model.predict(img_array)[0][0]

        prediction = model.predict(img_array)[0][0]

        st.subheader("🧠 prediction value")
        st.write(prediction)

        col1, col2, col3 = st.columns(3)

        col1.metric("Model Accuracy", "94%")
        col2.metric("Model Type", "CNN")
        col3.metric("Image Size", "128x128")

        if prediction < 0.02:
            risk = "high"
            st.error("🔴 High Risk Tooth Decay")

        elif prediction < 0.05:
            risk = "medium"
            st.warning("🟠 Medium Risk Tooth Decay")

        else:
            risk = "healthy"
            st.success("🟢 Low Risk Tooth Decay")

        save_history(
            st.session_state.email,
            st.session_state.username,
            prediction,
            risk
        )    

        # 📊 STATUS
        st.subheader("📊 Status Overview")
        data = {
           "Healthy": 1 if risk=="healthy" else 0,
           "Medium": 1 if risk=="medium" else 0,
           "High": 1 if risk=="high" else 0
        }
        st.bar_chart(pd.DataFrame.from_dict(data, orient="index"))

        # 🔥 HEATMAP FIRST
        if risk in ["high", "medium"]:
            st.subheader("🔥 Heatmap")
            show_heatmap(img)

        
         
        # -------- SUGGESTIONS (ADDED CORRECTLY) --------
        st.subheader("💡 Suggestions")

        if risk == "high":
            st.error(""" ⚠️Immediate Action Required

👉 🦷Visit dentist immediately  
👉 🍬Avoid sweets & cold drinks  
👉 ⏳Do not delay treatment

👉 📅Book dental appointment immediately  
👉 🚫🦷Avoid chewing on affected side  
👉 ♨️🧊Stay away from very hot/cold foods

🧴 Use pain relief gel if needed  
🧂 Rinse with warm salt water  
⚠️ Advanced treatment may be required 

💊 Take prescribed medicines only  
🪥 Keep area clean after eating  
🚨 Do not ignore pain or swelling  
""")

        elif risk == "medium":
            st.warning("""🟠 Take Care Early

👉 🪥Brush twice daily properly  
👉 🦷🧴Start using fluoride toothpaste  
👉 🍩🍫Reduce sugary snacks frequency

👉 💧Drink water after every meal  
🪥 Floss regularly   
🦷📅 Dental checkup recommended 

🪥 Brush gently but thoroughly  
🪥 Clean between teeth (floss/interdental)  
🔍 Monitor pain or sensitivity  
""")

        else:
            st.success("""🟢 Maintain Good Oral Health

👉 🪥Continue brushing twice daily  
👉 🥗Maintain balanced diet    
👉 💧Stay hydrated  

🍩🍭🍫 Avoid excess sugar     
✨😁 Keep smiling healthy                         
🔄🪥 Replace toothbrush every 3 months

👅🪥 Clean tongue regularly  
👨‍⚕️🦷 Visit dentist for routine checkup  
💙🦷 Care today, smile tomorrow 💯
""")
       
    # -------- MAP --------
        st.subheader("🏥 Hospitals")

        if risk != "healthy":
            st.map(pd.DataFrame({
                "lat": [13.0827, 13.0878, 13.0805],
                "lon": [80.2707, 80.2785, 80.2652]
            }))

            st.markdown("""
            <a href="https://www.google.com/maps/search/dental+hospital+near+me" target="_blank">
                <button style="padding:10px;background:green;color:white;border-radius:8px;">
                    Open Google Maps 🗺️
                </button>
            </a>
            """, unsafe_allow_html=True)

        else:
            st.success("No hospital needed 👍")

        return risk
    # ---------------- IMAGE UPLOAD ----------------
    st.subheader("📂 Upload Tooth Image")

    uploaded_file = st.file_uploader(
        "Choose a tooth image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        img = Image.open(uploaded_file)

        st.image(
            img,
            caption="Uploaded Image",
            use_container_width=True
        )

        risk = predict_tooth(img)

    # ---------------- CAMERA CAPTURE ----------------
    st.subheader("📷 Capture Tooth Image")

    camera_image = st.camera_input("Take a Tooth Photo")

    if camera_image is not None:

        img = Image.open(camera_image)

        st.image(
            img,
            caption="Captured Image",
            use_container_width=True
        )

        risk = predict_tooth(img)


# ---------------- HOSPITAL ----------------
elif st.session_state.step == 3 and page == "Nearby Hospitals":

    st.title("📍 Nearby Dental Hospitals")

    st.write("Click below to open nearby dental hospitals in Google Maps")

    # Map view (optional keep pannalaam)
    st.map(pd.DataFrame({
        "lat": [13.0827, 13.0878, 13.0805],
        "lon": [80.2707, 80.2785, 80.2652]
    }))

    # 🔥 Google Maps Button
    st.markdown("""
    <a href="https://www.google.com/maps/search/dental+hospital+near+me" target="_blank">
        <button style="
            padding:12px;
            background-color:#0A1AFF;
            color:white;
            border:none;
            border-radius:10px;
            font-size:16px;
            width:100%;">
            🗺️ Open in Google Maps
        </button>
    </a>
    """, unsafe_allow_html=True)

elif st.session_state.step == 3 and page == "History":

    st.title("📊 Your History")

    data = pd.read_sql_query(
        "SELECT name, prediction, risk, date FROM history WHERE email=? ORDER BY date ASC",
        conn,
        params=(st.session_state.email,)
    )
    data["date"] = pd.to_datetime(data["date"]) \
        .dt.tz_localize("UTC") \
        .dt.tz_convert("Asia/Kolkata") \
        .dt.strftime("%d-%m-%Y %I:%M %p")

    if not data.empty:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No history found")