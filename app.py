import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Aura EWS | Clinical Review", layout="wide")

st.markdown("""
    <style>
    .panel {background-color: #1e1e1e; padding: 15px; border-radius: 5px; margin-bottom: 10px;}
    .critical-text {color: #ff4b4b; font-weight: bold;}
    .stable-text {color: #00cc96; font-weight: bold;}
    .warning-text {color: #faca2b;}
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_system():
    df_features = pd.read_csv("time_series_features.csv")
    df_raw = pd.read_csv("final_ml_dataset.csv")
    target = "In-hospital_death"
    X = df_features.drop(columns=['RecordID', target])
    y = df_features[target]
    weight_ratio = len(y[y == 0]) / len(y[y == 1])
    model = xgb.XGBClassifier(
        n_estimators=200, learning_rate=0.05,
        scale_pos_weight=weight_ratio, missing=np.nan, random_state=42
    )
    model.fit(X, y)
    return model, df_raw, list(X.columns)

model, df_raw, expected_cols = load_system()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Aura EWS Analytics")
    valid_patients = df_raw['RecordID'].unique()
    patient_id = st.selectbox("Select Patient ID:", valid_patients)
    start_btn = st.button("▶ Run Clinical Analysis", use_container_width=True)

# --- MAIN DASHBOARD LAYOUT ---
st.title(f"Patient {patient_id} | Live Clinical Review")

col_chart, col_diagnostics = st.columns([3, 2])

with col_chart:
    st.subheader("Risk Trajectory")
    chart_spot = st.empty()

with col_diagnostics:
    st.subheader("Diagnostic Rationale")
    outcome_spot = st.empty()
    missing_data_spot = st.empty()
    rationale_spot = st.empty()

# Clinical thresholds for basic rationale generation
normal_ranges = {
    'HR': (60, 100, "bpm"),
    'SpO2': (95, 100, "%"),
    'SysABP': (90, 120, "mmHg"),
    'Temp': (36.1, 37.2, "°C")
}

# --- SIMULATION LOOP ---
if start_btn:
    patient_data = df_raw[df_raw['RecordID'] == patient_id]
    clinical_cols = [c for c in df_raw.columns if c not in ['RecordID', 'TimeMinutes', 'File', 'SAPS-I', 'SOFA', 'Length_of_stay', 'Survival', 'In-hospital_death']]
    agg_dict = {col: ['min', 'max', 'mean', 'std'] for col in clinical_cols}
    
    risk_history = []
    time_history = []
    
    for hour in range(4, 52, 4):
        current_time_mins = hour * 60
        snapshot = patient_data[patient_data['TimeMinutes'] <= current_time_mins]
        
        if snapshot.empty:
            continue
            
        # Model Prediction
        snapshot_features = snapshot.groupby('RecordID').agg(agg_dict)
        snapshot_features.columns = [f"{col[0]}_{col[1]}" for col in snapshot_features.columns]
        snapshot_features = snapshot_features.reindex(columns=expected_cols)
        
        risk_prob = model.predict_proba(snapshot_features)[0][1]
        risk_history.append(risk_prob * 100)
        time_history.append(f"Hr {hour}")
        
        # 1. Update Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_history, y=risk_history, fill='tozeroy', 
                                 line=dict(color='#ff4b4b' if risk_prob >= 0.2 else '#00b4d8', width=3)))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=350, yaxis=dict(range=[0, 100]), template="plotly_dark")
        chart_spot.plotly_chart(fig, use_container_width=True)
        
        # 2. Extract Latest Actual Values & Missing Data
        latest_vitals = snapshot[clinical_cols].iloc[-1]
        
        # Find missing sensors (NaN values in the current snapshot)
        missing_sensors = latest_vitals[latest_vitals.isna()].index.tolist()
        if missing_sensors:
            missing_text = f"<span class='warning-text'>Offline Sensors ({len(missing_sensors)}):</span> {', '.join(missing_sensors)}"
        else:
            missing_text = "<span class='stable-text'>All primary sensors active.</span>"
            
        missing_data_spot.markdown(f"<div class='panel'>{missing_text}</div>", unsafe_allow_html=True)
        
        # 3. Formulate Clinical Rationale based on dataset values
        rationale_html = "<div class='panel'><strong>Driving Factors (Latest Available):</strong><br>"
        abnormal_flags = 0
        
        for vital, (low, high, unit) in normal_ranges.items():
            if vital in latest_vitals and not pd.isna(latest_vitals[vital]):
                val = latest_vitals[vital]
                if val < low or val > high:
                    abnormal_flags += 1
                    rationale_html += f"• {vital}: <span class='critical-text'>{val:.1f} {unit}</span> (Normal: {low}-{high})<br>"
                else:
                    rationale_html += f"• {vital}: {val:.1f} {unit} (Normal)<br>"
        
        if abnormal_flags == 0 and risk_prob < 0.20:
            rationale_html += "<br><em>System logic: Vitals within normal limits. Trajectory stable.</em>"
        elif risk_prob >= 0.20:
            rationale_html += "<br><em>System logic: High physiological volatility detected across current active sensors. 20% risk threshold breached.</em>"
            
        rationale_html += "</div>"
        rationale_spot.markdown(rationale_html, unsafe_allow_html=True)

        # 4. Final Review Decision Update
        if risk_prob >= 0.20:
            outcome_spot.markdown(f"<div class='panel'><h3 class='critical-text'>FINAL REVIEW: CRITICAL RISK ({risk_prob*100:.1f}%)</h3>Action Required: Immediate clinical intervention recommended.</div>", unsafe_allow_html=True)
        else:
            outcome_spot.markdown(f"<div class='panel'><h3 class='stable-text'>FINAL REVIEW: NORMAL ({risk_prob*100:.1f}%)</h3>Action Required: Continue standard monitoring.</div>", unsafe_allow_html=True)
            
        time.sleep(0.5)
