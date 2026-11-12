import streamlit as st
from datetime import datetime
import pandas as pd

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Alcohol Detector | Smart Safety",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #14243b);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
[data-testid="stMetric"] {
    background: #1c2d45;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #314764;
}
div.stButton > button {
    background: #00a6d6;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    width: 100%;
}
div.stButton > button:hover {
    background: #008bb5;
    color: white;
}
.card {
    background: #1c2d45;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #314764;
    margin-bottom: 15px;
}
.safe {
    background: #14532d;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.danger {
    background: #7f1d1d;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.small {
    color: #aabbd0 !important;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DATA ----------------
if "history" not in st.session_state:
    st.session_state.history = []
if "reading" not in st.session_state:
    st.session_state.reading = 100
if "motor_status" not in st.session_state:
    st.session_state.motor_status = "ON"
if "detected" not in st.session_state:
    st.session_state.detected = False

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🚗 Alcohol Detector")
    st.caption("SMART VEHICLE SAFETY SYSTEM")
    st.divider()
    
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Detection History", "About Project"]
    )
    
    st.divider()
    st.subheader("⚙️ System Settings")
    threshold = st.slider(
        "Alcohol Detection Threshold",
        min_value=50,
        max_value=1000,
        value=300
    )
    st.caption("Demo mode: sensor readings are entered manually.")
    st.divider()
    st.caption("ATL School Project | 2026")

# ---------------- DETECTION FUNCTION ----------------
def check_alcohol(value):
    detected = value >= threshold
    st.session_state.reading = value
    st.session_state.detected = detected
    
    if detected:
        st.session_state.motor_status = "LOCKED"
        result = "ALCOHOL DETECTED"
        motor = "MOTOR LOCKED"
    else:
        st.session_state.motor_status = "ON"
        result = "NO ALCOHOL DETECTED"
        motor = "MOTOR ON"
        
    record = {
        "Date": datetime.now().strftime("%d-%m-%Y"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Sensor Reading": value,
        "Detection": result,
        "Motor Status": motor
    }
    st.session_state.history.insert(0, record)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("🚗 Alcohol Detector Dashboard")
    st.markdown("### Alcohol Detection & Dual-Shaft Motor Engine Lock System")
    st.caption(
        "A smart safety model designed to demonstrate "
        "alcohol detection and automatic motor locking."
    )
    st.divider()

    # Sensor input
    st.subheader("🧪 Alcohol Sensor Monitoring")
    col1, col2 = st.columns([2, 1])
    with col1:
        sensor_value = st.number_input(
            "Enter Alcohol Sensor Reading",
            min_value=0,
            max_value=1023,
            value=st.session_state.reading,
            step=10
        )
    with col2:
        st.write("")
        st.write("")
        check = st.button("🔍 CHECK ALCOHOL")
        if check:
            check_alcohol(sensor_value)

    st.divider()

    # Dashboard metrics
    st.subheader("📊 Live System Status")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Sensor Reading", st.session_state.reading)
    with c2:
        detection_status = "Detected" if st.session_state.detected else "Not detected"
        st.metric("Alcohol Status", detection_status)
    with c3:
        st.metric("Motor Status", st.session_state.motor_status)

    st.divider()

    # Safety status
    st.subheader("🛡️ Safety Result")
    if st.session_state.detected:
        st.markdown("""
        <div class="danger">
            <h2>⚠️ ALCOHOL DETECTED</h2>
            <h3>🔒 MOTOR LOCKED</h3>
            <p>Safety threshold exceeded.</p>
            <p>The model motor must remain disabled.</p>
        </div>
        """, unsafe_allow_html=True)
        st.error("Warning: Motor operation is blocked in this model.")
    else:
        st.markdown("""
        <div class="safe">
            <h2>✅ NO ALCOHOL DETECTED</h2>
            <h3>🟢 MOTOR ENABLED</h3>
            <p>Reading is below the project threshold.</p>
        </div>
        """, unsafe_allow_html=True)
        st.success("The model is in its motor-enabled state.")

    st.divider()
    st.subheader("⚙️ Working Principle")
    st.markdown("""
    1. The alcohol sensor checks the sample.
    2. The sensor reading is compared with the threshold.
    3. If the reading reaches the threshold, the motor is locked.
    4. Otherwise, the motor is allowed to operate.
    5. The app displays the detection result.
    """)
    st.caption(
        "Note: This is a demonstration interface. "
        "The motor status displayed here does not directly "
        "control the physical motor."
    )

# ---------------- HISTORY PAGE ----------------
elif page == "Detection History":
    st.title("📋 Detection History")
    st.write("Previous alcohol detection records.")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.subheader("📈 Sensor Reading Chart")
        chart_data = df[["Sensor Reading"]].iloc[::-1]
        st.line_chart(chart_data)
        
        if st.button("🗑️ CLEAR HISTORY"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No detection records available yet.")

# ---------------- ABOUT PAGE ----------------
elif page == "About Project":
    st.title("ℹ️ About Alcohol Detector")
    st.markdown("""
    <div class="card">
        <h2>🚗 Alcohol Detector</h2>
        <h3>Alcohol Detection and Engine Lock System</h3>
        <p>
            Alcohol Detector is a school project designed to demonstrate how alcohol detection 
            can help prevent unsafe vehicle operation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 Aim")
    st.write("""
    To develop a smart alcohol detection system that prevents a model vehicle from 
    operating when alcohol is detected above a predefined threshold.
    """)

    st.subheader("🔧 Main Components")
    components = [
        "Alcohol Detection Sensor",
        "Microcontroller",
        "Dual-Shaft DC Motor",
        "Motor Driver",
        "Power Supply",
        "Connecting Wires"
    ]
    for item in components:
        st.write("• " + item)

    st.subheader("💡 Applications")
    st.write("""
    - Vehicle safety demonstrations
    - Alcohol detection awareness
    - Smart transportation concepts
    - Educational electronics projects
    """)

    st.subheader("⚠️ Disclaimer")
    st.write("""
    This is an educational prototype. Sensor readings are not a certified measurement 
    of blood alcohol level and must not be used to determine whether someone is fit to drive.
    """)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<center><p class='small'>"
    "ALCOHOL DETECTOR | SMART SAFETY PROJECT | 2026"
    "</p></center>",
    unsafe_allow_html=True
)
