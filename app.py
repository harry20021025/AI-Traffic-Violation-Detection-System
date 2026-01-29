import streamlit as st
import requests
from PIL import Image
import io
import mysql.connector

# ======================
# CONFIG
# ======================
BACKEND_URL = "http://127.0.0.1:8000/process-image"
ADMIN_PASSWORD = "admin123"

VIOLATION_TYPES = [
    "No Helmet",
    "Signal Jump",
    "Over Speeding",
    "Wrong Parking",
    "No Seat Belt"
]

# ======================
# DB CONNECTION (ADMIN)
# ======================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="traffic_db"
)
cursor = conn.cursor()

# ======================
# PAGE SETUP
# ======================
st.set_page_config(page_title="Traffic Violation System", layout="centered")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ======================
# SIDEBAR NAVIGATION
# ======================
st.sidebar.title("🚦 Navigation")
page = st.sidebar.radio("Go to", ["Public - Violation Detection", "Admin Panel"])

# =====================================================
# 1️⃣ PUBLIC PAGE
# =====================================================
if page == "Public - Violation Detection":

    st.title("🚦 AI Traffic Violation Detection System")

    uploaded_file = st.file_uploader(
        "Upload Vehicle Image",
        type=["jpg", "jpeg", "png"]
    )

    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    violation_type = st.selectbox("🚨 Select Violation Type", VIOLATION_TYPES)

    if image and st.button("🚨 Process Image"):
        with st.spinner("Processing..."):

            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            files = {"file": ("image.png", img_bytes, "image/png")}
            data = {"violation_type": violation_type}

            try:
                response = requests.post(BACKEND_URL, files=files, data=data)
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("✅ Fine Generated Successfully")
                    st.write(f"**Vehicle Number:** {result['vehicle_number']}")
                    st.write(f"**Violation:** {result['violation_type']}")
                    st.write(f"**Fine:** ₹{result['fine']}")
                    st.write(f"**Status:** {result['status']}")

            except Exception as e:
                st.error(f"Backend not reachable: {e}")

# =====================================================
# 2️⃣ ADMIN PAGE (PASSWORD PROTECTED)
# =====================================================
elif page == "Admin Panel":

    st.title("🔐 Admin Panel")

    # -------- LOGIN --------
    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter Admin Password", type="password")

        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Incorrect password")

    # -------- ADMIN DASHBOARD --------
    else:
        st.success("🛠️ Admin Access Granted")

        st.subheader("➕ Add New Vehicle & Owner")

        owner_name = st.text_input("Owner Name")
        email = st.text_input("Email")
        vehicle_number = st.text_input("Vehicle Number (e.g. MH04FA1234)")

        if st.button("Save Vehicle"):
            if owner_name and email and vehicle_number:
                try:
                    cursor.execute(
                        """
                        INSERT INTO vehicle_owners
                        (vehicle_number, owner_name, email)
                        VALUES (%s, %s, %s)
                        """,
                        (vehicle_number.upper(), owner_name, email)
                    )
                    conn.commit()
                    st.success("✅ Vehicle added successfully")
                except Exception as e:
                    st.error(f"Database error: {e}")
            else:
                st.warning("⚠️ Please fill all fields")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
