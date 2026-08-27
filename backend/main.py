from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest, RandomForestClassifier

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

import ollama

from datetime import datetime
import random


# ============================================================
# APP
# ============================================================

app = FastAPI(title="NuclearGuard AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GLOBAL REACTOR STATE
# ============================================================

reactor_state = {
    "data": None,
    "anomaly_mode": False,
    "last_refresh": None
}


alert_log = []


# ============================================================
# DATA GENERATION
# ============================================================

def generate_data(n=200, inject_anomaly=False):

    seed = random.randint(0, 999999)
    np.random.seed(seed)

    data = {
        "temperature": np.random.normal(300, 5, n),
        "pressure": np.random.normal(150, 3, n),
        "neutron_flux": np.random.normal(1e13, 1e11, n),
        "coolant_flow": np.random.normal(500, 10, n),
        "vibration": np.random.normal(0.5, 0.05, n),
        "radiation_level": np.random.normal(2.5, 0.2, n),
    }

    # --------------------------------------------------------
    # Inject abnormal reactor conditions
    # --------------------------------------------------------

    if inject_anomaly:

        data["temperature"][-10:] += np.random.uniform(
            40, 80, 10
        )

        data["pressure"][-10:] += np.random.uniform(
            30, 60, 10
        )

        data["vibration"][-10:] += np.random.uniform(
            0.5, 1.5, 10
        )

        data["radiation_level"][-10:] += np.random.uniform(
            1.0, 3.0, 10
        )

    return pd.DataFrame(data)


# ============================================================
# REFRESH REACTOR
# ============================================================

def refresh_reactor(anomaly=False):

    df = generate_data(
        n=200,
        inject_anomaly=anomaly
    )

    reactor_state["data"] = df
    reactor_state["anomaly_mode"] = anomaly
    reactor_state["last_refresh"] = datetime.now()

    return df


# Create initial normal reactor state
refresh_reactor(False)


# ============================================================
# GET CURRENT DATA
# ============================================================

def get_current_data():

    if reactor_state["data"] is None:
        return refresh_reactor(False)

    return reactor_state["data"]


# ============================================================
# ALERT SYSTEM
# ============================================================

def add_alert(message, level="WARNING"):

    alert_log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "level": level,
        "message": message
    })

    if len(alert_log) > 20:
        alert_log.pop(0)


# ============================================================
# MODEL 1
# ANOMALY DETECTION
# ============================================================

def run_anomaly_detection(df):

    # --------------------------------------------------------
    # Normal reactor data should NOT automatically produce
    # 5% anomalies just because of contamination.
    #
    # We use contamination="auto" and then apply a safety
    # threshold to the sensor values.
    # --------------------------------------------------------

    model = IsolationForest(
        contamination="auto",
        random_state=42,
        n_estimators=150
    )

    model.fit(df)

    predictions = model.predict(df)

    # --------------------------------------------------------
    # Convert Isolation Forest results
    # --------------------------------------------------------

    anomaly_mask = predictions == -1

    # --------------------------------------------------------
    # Safety thresholds
    # --------------------------------------------------------

    threshold_mask = (
        (df["temperature"] > 330) |
        (df["pressure"] > 180) |
        (df["vibration"] > 1.0) |
        (df["radiation_level"] > 5.0)
    )

    # --------------------------------------------------------
    # Only treat Isolation Forest anomalies as real anomalies
    # when the reactor values are meaningfully abnormal.
    # --------------------------------------------------------

    final_mask = anomaly_mask & threshold_mask

    return final_mask.astype(int)


# ============================================================
# MODEL 2
# PREDICTIVE MAINTENANCE
# ============================================================

def create_maintenance_training_data(n=3000):

    np.random.seed(42)

    temperature = np.random.normal(300, 15, n)
    pressure = np.random.normal(150, 10, n)
    neutron_flux = np.random.normal(1e13, 5e11, n)
    coolant_flow = np.random.normal(500, 30, n)
    vibration = np.random.normal(0.5, 0.2, n)
    radiation = np.random.normal(2.5, 0.8, n)

    X = pd.DataFrame({
        "temperature": temperature,
        "pressure": pressure,
        "neutron_flux": neutron_flux,
        "coolant_flow": coolant_flow,
        "vibration": vibration,
        "radiation_level": radiation
    })

    # --------------------------------------------------------
    # Generate training labels
    # --------------------------------------------------------

    risk_score = (
        ((temperature - 300) / 15) +
        ((pressure - 150) / 10) +
        ((vibration - 0.5) / 0.2) +
        ((radiation - 2.5) / 0.8)
    )

    probability = 1 / (1 + np.exp(-risk_score))

    y = (
        np.random.random(n) < probability
    ).astype(int)

    return X, y


# Train maintenance model ONCE
maintenance_X, maintenance_y = create_maintenance_training_data()


maintenance_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    min_samples_leaf=10,
    random_state=42
)

maintenance_model.fit(
    maintenance_X,
    maintenance_y
)


# ============================================================
# COMPONENT MAINTENANCE PREDICTION
# ============================================================

def run_maintenance_prediction(df):

    latest = df.tail(1).copy()

    components = [
        {
            "name": "Coolant Pump",
            "vibration_factor": 1.25,
            "temperature_factor": 0.90,
            "pressure_factor": 0.80
        },
        {
            "name": "Steam Generator",
            "vibration_factor": 0.90,
            "temperature_factor": 1.20,
            "pressure_factor": 1.15
        },
        {
            "name": "Turbine",
            "vibration_factor": 1.30,
            "temperature_factor": 1.00,
            "pressure_factor": 1.10
        },
        {
            "name": "Reactor Valve",
            "vibration_factor": 0.80,
            "temperature_factor": 1.15,
            "pressure_factor": 1.30
        },
        {
            "name": "Heat Exchanger",
            "vibration_factor": 0.85,
            "temperature_factor": 1.25,
            "pressure_factor": 1.05
        }
    ]

    results = []

    for component in components:

        component_data = latest.copy()

        # Component-specific sensitivity
        component_data["vibration"] *= component["vibration_factor"]

        component_data["temperature"] = (
            300
            + (component_data["temperature"] - 300)
            * component["temperature_factor"]
        )

        component_data["pressure"] = (
            150
            + (component_data["pressure"] - 150)
            * component["pressure_factor"]
        )

        probability = maintenance_model.predict_proba(
            component_data[
                [
                    "temperature",
                    "pressure",
                    "neutron_flux",
                    "coolant_flow",
                    "vibration",
                    "radiation_level"
                ]
            ]
        )[0][1]

        probability = float(probability * 100)

        probability = round(
            min(max(probability, 0), 100),
            2
        )

        if probability >= 70:
            status = "Critical"

        elif probability >= 40:
            status = "Warning"

        else:
            status = "Healthy"

        results.append({
            "component": component["name"],
            "failure_probability": probability,
            "status": status
        })

    return results


# ============================================================
# MODEL 3
# LSTM FORECAST
# ============================================================

def run_lstm_forecast(df):

    data = df["temperature"].values.astype(float)

    mean = data.mean()
    std = data.std()

    if std == 0:
        std = 1

    normalized = (data - mean) / std

    seq_len = 20

    X = []
    y = []

    for i in range(len(normalized) - seq_len):

        X.append(
            normalized[i:i + seq_len]
        )

        y.append(
            normalized[i + seq_len]
        )

    X = np.array(X).reshape(
        -1,
        seq_len,
        1
    )

    y = np.array(y)

    model = Sequential([
        LSTM(
            32,
            input_shape=(seq_len, 1)
        ),
        Dense(1)
    ])

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    model.fit(
        X,
        y,
        epochs=3,
        batch_size=16,
        verbose=0
    )

    last_seq = normalized[-seq_len:].reshape(
        1,
        seq_len,
        1
    )

    predictions = []

    for _ in range(10):

        prediction = model.predict(
            last_seq,
            verbose=0
        )[0][0]

        temperature = (
            prediction * std
        ) + mean

        predictions.append(
            float(temperature)
        )

        last_seq = np.append(
            last_seq[:, 1:, :],
            [[[prediction]]],
            axis=1
        )

    difference = (
        predictions[-1]
        - predictions[0]
    )

    if difference > 2:
        trend = "RISING"

    elif difference < -2:
        trend = "FALLING"

    else:
        trend = "STABLE"

    return {
        "next_10_temps": [
            round(p, 2)
            for p in predictions
        ],

        "trend": trend,

        "predicted_critical": any(
            p > 330
            for p in predictions
        )
    }


# ============================================================
# RISK SCORE
# ============================================================

def calculate_risk(
    df,
    anomaly_count,
    maintenance
):

    # --------------------------------------------------------
    # Anomaly contribution
    # --------------------------------------------------------

    anomaly_risk = min(
        anomaly_count * 5,
        50
    )

    # --------------------------------------------------------
    # Maintenance contribution
    # --------------------------------------------------------

    critical = sum(
        1
        for m in maintenance
        if m["status"] == "Critical"
    )

    warning = sum(
        1
        for m in maintenance
        if m["status"] == "Warning"
    )

    maintenance_risk = (
        critical * 10
        + warning * 5
    )

    # --------------------------------------------------------
    # Sensor risk
    # --------------------------------------------------------

    latest = df.tail(1).iloc[0]

    sensor_risk = 0

    if latest["temperature"] > 315:
        sensor_risk += 10

    if latest["pressure"] > 165:
        sensor_risk += 10

    if latest["vibration"] > 0.8:
        sensor_risk += 10

    if latest["radiation_level"] > 4:
        sensor_risk += 10

    total = (
        anomaly_risk
        + maintenance_risk
        + sensor_risk
    )

    return round(
        min(total, 100),
        1
    )


# ============================================================
# SENSOR DATA
# ============================================================

@app.get("/sensor-data")
def sensor_data():

    df = get_current_data()

    latest = df.tail(1).iloc[0]

    return {
        "temperature": round(
            float(latest["temperature"]),
            2
        ),

        "pressure": round(
            float(latest["pressure"]),
            2
        ),

        "neutron_flux": float(
            f"{latest['neutron_flux']:.2e}"
        ),

        "coolant_flow": round(
            float(latest["coolant_flow"]),
            2
        ),

        "vibration": round(
            float(latest["vibration"]),
            3
        ),

        "radiation_level": round(
            float(latest["radiation_level"]),
            2
        )
    }


# ============================================================
# ANOMALY STATUS
# ============================================================

@app.get("/anomaly-status")
def anomaly_status():

    df = get_current_data()

    predictions = run_anomaly_detection(df)

    anomaly_count = int(
        np.sum(predictions == 1)
    )

    if anomaly_count > 0:

        add_alert(
            f"{anomaly_count} anomalies detected in sensor readings",
            "CRITICAL"
        )

    return {
        "anomaly_count": anomaly_count,

        "total_readings": len(
            predictions
        ),

        "status": (
            "ANOMALY DETECTED"
            if anomaly_count > 0
            else "Normal"
        ),

        "alert": anomaly_count > 0
    }


# ============================================================
# MAINTENANCE PREDICTION
# ============================================================

@app.get("/maintenance-prediction")
def maintenance_prediction():

    df = get_current_data()

    results = run_maintenance_prediction(df)

    for result in results:

        if result["status"] == "Critical":

            add_alert(
                f"{result['component']} failure probability: "
                f"{result['failure_probability']}%",
                "CRITICAL"
            )

        elif result["status"] == "Warning":

            add_alert(
                f"{result['component']} showing warning signs",
                "WARNING"
            )

    return {
        "components": results
    }


# ============================================================
# LSTM FORECAST
# ============================================================

@app.get("/lstm-forecast")
def lstm_forecast():

    df = get_current_data()

    result = run_lstm_forecast(df)

    if result["predicted_critical"]:

        add_alert(
            "LSTM predicts temperature will reach critical levels!",
            "CRITICAL"
        )

    return result


# ============================================================
# RISK SCORE
# ============================================================

@app.get("/risk-score")
def risk_score():

    df = get_current_data()

    predictions = run_anomaly_detection(df)

    anomaly_count = int(
        np.sum(predictions == 1)
    )

    maintenance = run_maintenance_prediction(df)

    score = calculate_risk(
        df,
        anomaly_count,
        maintenance
    )

    if score > 70:
        level = "CRITICAL"
        color = "#ff0000"

    elif score > 50:
        level = "HIGH"
        color = "#ff8800"

    elif score > 25:
        level = "MODERATE"
        color = "#ffff00"

    else:
        level = "LOW"
        color = "#00ff00"

    return {
        "risk_score": score,
        "risk_level": level,
        "color": color
    }


# ============================================================
# INCIDENT REPORT
# ============================================================

def generate_incident_report(
    sensor_data,
    anomaly_count,
    risk_score,
    maintenance
):

    critical_components = [
        m
        for m in maintenance
        if m["status"] == "Critical"
    ]

    prompt = f"""
You are NuclearGuard AI, an industrial nuclear plant
monitoring assistant.

Generate a concise professional monitoring incident report.

Sensor Readings:

Temperature:
{sensor_data['temperature']} °C

Pressure:
{sensor_data['pressure']} Bar

Neutron Flux:
{sensor_data['neutron_flux']} n/cm2/s

Coolant Flow:
{sensor_data['coolant_flow']} kg/s

Vibration:
{sensor_data['vibration']}

Radiation:
{sensor_data['radiation_level']} mSv/h

Anomalies Detected:
{anomaly_count}

Risk Score:
{risk_score}/100

Critical Components:
{[c['component'] for c in critical_components]}

Format:

Summary:
Severity:
Affected Systems:
Recommended Actions:

Keep the report under 150 words.
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


@app.get("/incident-report")
def incident_report():

    df = get_current_data()

    predictions = run_anomaly_detection(df)

    anomaly_count = int(
        np.sum(predictions == 1)
    )

    maintenance = run_maintenance_prediction(df)

    sensor = {
        "temperature": round(
            float(df["temperature"].mean()),
            2
        ),

        "pressure": round(
            float(df["pressure"].mean()),
            2
        ),

        "neutron_flux": (
            f"{df['neutron_flux'].mean():.2e}"
        ),

        "coolant_flow": round(
            float(df["coolant_flow"].mean()),
            2
        ),

        "vibration": round(
            float(df["vibration"].mean()),
            3
        ),

        "radiation_level": round(
            float(df["radiation_level"].mean()),
            2
        )
    }

    score = calculate_risk(
        df,
        anomaly_count,
        maintenance
    )

    report = generate_incident_report(
        sensor,
        anomaly_count,
        score,
        maintenance
    )

    add_alert(
        "Incident report generated",
        "INFO"
    )

    return {
        "report": report,

        "generated_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }


# ============================================================
# ALERT LOG
# ============================================================

@app.get("/alert-log")
def get_alert_log():

    return {
        "alerts": list(
            reversed(alert_log)
        )
    }


# ============================================================
# REFRESH
# ============================================================

@app.post("/refresh")
def refresh_endpoint(
    anomaly: bool = False
):

    refresh_reactor(anomaly)

    add_alert(
        (
            "Reactor state refreshed in "
            "ANOMALY MODE"
            if anomaly
            else
            "Reactor state refreshed normally"
        ),
        "WARNING" if anomaly else "INFO"
    )

    return {
        "message": "Reactor state refreshed",
        "anomaly_mode": anomaly
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message":
            "NuclearGuard AI is running!"
    }
