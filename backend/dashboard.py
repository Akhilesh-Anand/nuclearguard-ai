import streamlit as st
import requests
import plotly.graph_objects as go

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NuclearGuard AI Test", layout="wide")
st.title("🔬 NuclearGuard AI — Test Dashboard")

anomaly = st.toggle("🚨 Simulate Anomaly", value=False)
params = {"anomaly": anomaly}

col1, col2, col3 = st.columns(3)

# ─── Risk Score ───
with col1:
    try:
        r = requests.get(f"{BASE_URL}/risk-score", params=params).json()
        st.metric("Risk Score", f"{r['risk_score']}/100")
        st.markdown(f"**Level:** :{r['risk_level']}:")
    except:
        st.error("Backend not running")

# ─── Anomaly Status ───
with col2:
    try:
        r = requests.get(f"{BASE_URL}/anomaly-status", params=params).json()
        if r["alert"]:
            st.error(f"🚨 {r['status']} — {r['anomaly_count']} anomalies")
        else:
            st.success(f"✅ {r['status']}")
    except:
        st.error("Backend not running")

# ─── Sensor Data ───
with col3:
    try:
        r = requests.get(f"{BASE_URL}/sensor-data", params=params).json()
        st.metric("Temperature", f"{r['temperature']} °C")
        st.metric("Pressure", f"{r['pressure']} Bar")
        st.metric("Coolant Flow", f"{r['coolant_flow']} kg/s")
    except:
        st.error("Backend not running")

st.divider()

# ─── LSTM Forecast ───
st.subheader("📈 LSTM Temperature Forecast")
try:
    r = requests.get(f"{BASE_URL}/lstm-forecast", params=params).json()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=r["next_10_temps"],
        mode='lines+markers',
        line=dict(color='orange'),
        name='Predicted Temp'
    ))
    fig.add_hline(y=330, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"Trend: **{r['trend']}** | Critical Predicted: **{r['predicted_critical']}**")
except:
    st.error("LSTM endpoint not responding")

st.divider()

# ─── Maintenance Prediction ───
st.subheader("🔧 Predictive Maintenance")
try:
    r = requests.get(f"{BASE_URL}/maintenance-prediction", params=params).json()
    for comp in r["components"]:
        color = "🔴" if comp["status"] == "Critical" else "🟡" if comp["status"] == "Warning" else "🟢"
        st.write(f"{color} **{comp['component']}** — {comp['failure_probability']}% failure probability — {comp['status']}")
except:
    st.error("Maintenance endpoint not responding")

st.divider()

# ─── Incident Report ───
st.subheader("📋 AI Incident Report")
if st.button("Generate Incident Report"):
    with st.spinner("AI generating report..."):
        try:
            r = requests.get(f"{BASE_URL}/incident-report", params=params).json()
            st.text_area("Generated Report", r["report"], height=250)
            st.caption(f"Generated at: {r['generated_at']}")
        except:
            st.error("Incident report endpoint not responding")

st.divider()

# ─── Alert Log ───
st.subheader("🔔 Alert Log")
try:
    r = requests.get(f"{BASE_URL}/alert-log").json()
    if r["alerts"]:
        for alert in r["alerts"]:
            icon = "🔴" if alert["level"] == "CRITICAL" else "🟡" if alert["level"] == "WARNING" else "🔵"
            st.write(f"{icon} `{alert['time']}` — {alert['message']}")
    else:
        st.info("No alerts yet")
except:
    st.error("Alert log not responding")
