import streamlit as st
import requests
from PIL import Image
import io

# ==============================
# CONFIG
# ==============================

# For now this is local backend.
# After deploying backend, replace with public URL.
BACKEND_URL = "http://127.0.0.1:8000/process-image"

ADMIN_PASSWORD = "admin123"

VIOLATION_TYPES = [
    "No Helmet",
    "Signal Jump",
    "Over Speeding",
    "Wrong Parking",
    "No Seat Belt"
]

# ==============================
# STREAMLIT PAGE SETUP
# ==============================

st.set_page_config(
    page_title="AI Traffic Violation Detection",
    layout="centered"
)

# Session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("🚦 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Public - Violation Detection", "Admin Panel"]
)

# ==============================
# PUBLIC PAGE
# ==============================

if page == "Public - Violation Detection":

    st.title("🚦 AI Traffic Violation Detection System")

    st.write(
        "Upload a vehicle image to detect number plate and generate fine."
    )

    uploaded_file = st.file_uploader(
        "Upload Vehicle Image",
        type=["jpg", "jpeg", "png"]
    )

    image = None

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="Uploaded Image",
            use_column_width=True
        )

    violation_type = st.selectbox(
        "Select Violation Type",
        VIOLATION_TYPES
    )

    if image and st.button("Process Image"):

        with st.spinner("Processing image..."):

            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            files = {
                "file": ("image.png", img_bytes, "image/png")
            }

            data = {
                "violation_type": violation_type
            }

            try:
                response = requests.post(
                    BACKEND_URL,
                    files=files,
                    data=data,
                    timeout=60
                )

                result = response.json()

                if response.status_code != 200:
                    st.error("Backend error occurred")
                    st.write(result)
                    st.stop()

                if "error" in result:
                    st.error(result["error"])

                else:
                    st.success("✅ Violation processed successfully")

                    st.write(
                        f"**Vehicle Number:** {result.get('vehicle_number', 'N/A')}"
                    )

                    st.write(
                        f"**Violation:** {result.get('violation_type', 'N/A')}"
                    )

                    st.write(
                        f"**Fine Amount:** ₹{result.get('fine', 'N/A')}"
                    )

                    st.write(
                        f"**Status:** {result.get('status', 'Pending')}"
                    )

            except requests.exceptions.RequestException:
                st.error(
                    "⚠ Backend server not reachable. "
                    "Make sure FastAPI backend is running."
                )

# ==============================
# ADMIN PANEL (DEMO MODE)
# ==============================

elif page == "Admin Panel":

    st.title("🔐 Admin Panel")

    if not st.session_state.admin_logged_in:

        password = st.text_input(
            "Enter Admin Password",
            type="password"
        )

        if st.button("Login"):

            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Incorrect password")

    else:

        st.success("Admin access granted")

        st.subheader("Add Vehicle & Owner (Demo Mode)")

        owner_name = st.text_input("Owner Name")
        email = st.text_input("Email")
        vehicle_number = st.text_input(
            "Vehicle Number (Example: MH04FA1234)"
        )

        if st.button("Save Vehicle"):
            st.warning(
                "Database is disabled for free cloud deployment.\n"
                "This feature works in local setup with MySQL."
            )

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

# ==============================
# FOOTER
# ==============================

st.markdown("---")
st.markdown(
    "Built by **Hariom Dixit** | AI Traffic Violation Detection System"
)
