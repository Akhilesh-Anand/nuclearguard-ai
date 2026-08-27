# import winsound
# import time
# import subprocess
# import requests

# BASE_URL = "http://127.0.0.1:8000"

# def speak(text):
#     print(f"[ALERT] {text}")
#     subprocess.run([
#         'powershell', '-Command',
#         f'Add-Type -AssemblyName System.Speech; '
#         f'$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
#         f'$s.Speak("{text}")'
#     ])

# def beep(times=1):
#     for _ in range(times):
#         winsound.Beep(1000, 400)
#         time.sleep(0.1)

# def critical_beep():
#     for _ in range(3):
#         winsound.Beep(1500, 200)
#         time.sleep(0.1)

# # ─── Check Sensor Data ────────────────────────────────────────
# def check_sensors(anomaly=False):
#     try:
#         r = requests.get(f"{BASE_URL}/sensor-data", params={"anomaly": anomaly}).json()
#         temp = r["temperature"]
#         pressure = r["pressure"]
#         radiation = r["radiation_level"]
#         vibration = r["vibration"]
#         coolant = r["coolant_flow"]

#         print(f"\n[SENSORS] Temp:{temp}°C | Pressure:{pressure}bar | Radiation:{radiation}mSv | Vibration:{vibration} | Coolant:{coolant}kg/s")

#         # Temperature alerts
#         if temp > 330:
#             critical_beep()
#             speak(f"Critical alert! Reactor temperature at {round(temp)} degrees. Immediate action required!")
#         elif temp > 315:
#             beep(2)
#             speak(f"Warning. Temperature rising to {round(temp)} degrees. Monitor closely.")
#         elif temp < 270:
#             beep(2)
#             speak("Warning. Temperature dropping below safe range.")

#         # Pressure alerts
#         if pressure > 170:
#             critical_beep()
#             speak(f"Critical alert! Pressure at {round(pressure)} bar. Dangerously high!")
#         elif pressure < 140:
#             critical_beep()
#             speak(f"Critical alert! Pressure dropped to {round(pressure)} bar!")
#         elif pressure > 162:
#             beep()
#             speak("Caution. Pressure drifting above normal range.")
#         elif pressure < 148:
#             beep()
#             speak("Caution. Pressure drifting below normal range.")

#         # Radiation alerts
#         if radiation > 4.0:
#             critical_beep()
#             speak(f"Critical! Radiation level at {round(radiation, 1)} millisieverts. Evacuate area!")
#         elif radiation > 3.0:
#             beep(2)
#             speak(f"Warning. Radiation elevated at {round(radiation, 1)} millisieverts.")

#         # Vibration alerts
#         if vibration > 1.5:
#             critical_beep()
#             speak("Critical vibration detected in reactor systems!")
#         elif vibration > 0.8:
#             beep()
#             speak("Caution. Abnormal vibration detected.")

#         # Coolant flow alerts
#         if coolant < 450:
#             critical_beep()
#             speak("Critical! Coolant flow rate dangerously low!")
#         elif coolant < 480:
#             beep()
#             speak("Warning. Coolant flow rate below normal.")

#     except Exception as e:
#         print(f"[ERROR] Sensor check failed: {e}")

# # ─── Check Anomaly Status ─────────────────────────────────────
# def check_anomaly(anomaly=False):
#     try:
#         r = requests.get(f"{BASE_URL}/anomaly-status", params={"anomaly": anomaly}).json()
#         count = r["anomaly_count"]
#         status = r["status"]

#         if r["alert"]:
#             critical_beep()
#             speak(f"Anomaly detected! {count} abnormal readings found in sensor data. Risk level elevated.")
#             print(f"[ANOMALY] {status} — {count} anomalies")
#         else:
#             print(f"[ANOMALY] {status}")

#     except Exception as e:
#         print(f"[ERROR] Anomaly check failed: {e}")

# # ─── Check Risk Score ─────────────────────────────────────────
# def check_risk(anomaly=False):
#     try:
#         r = requests.get(f"{BASE_URL}/risk-score", params={"anomaly": anomaly}).json()
#         score = r["risk_score"]
#         level = r["risk_level"]

#         print(f"[RISK] Score: {score}/100 — {level}")

#         if score > 70:
#             critical_beep()
#             speak(f"Critical risk level! Plant risk score is {round(score)} out of 100. Emergency protocols may be required.")
#         elif score > 50:
#             beep(2)
#             speak(f"High risk detected. Risk score is {round(score)} out of 100. Increased monitoring required.")
#         elif score > 25:
#             beep()
#             speak(f"Moderate risk level. Score is {round(score)}. Stay alert.")
#         else:
#             print(f"[OK] Risk score normal: {score}/100")

#     except Exception as e:
#         print(f"[ERROR] Risk check failed: {e}")

# # ─── Check Maintenance Predictions ───────────────────────────
# def check_maintenance(anomaly=False):
#     try:
#         r = requests.get(f"{BASE_URL}/maintenance-prediction", params={"anomaly": anomaly}).json()
#         components = r["components"]

#         for comp in components:
#             name = comp["component"]
#             prob = comp["failure_probability"]
#             status = comp["status"]

#             if status == "Critical":
#                 critical_beep()
#                 speak(f"Critical maintenance alert! {name} has {round(prob)} percent failure probability. Inspect immediately!")
#             elif status == "Warning":
#                 beep()
#                 speak(f"Maintenance warning. {name} showing signs of wear. Failure probability {round(prob)} percent.")

#     except Exception as e:
#         print(f"[ERROR] Maintenance check failed: {e}")

# # ─── Check LSTM Forecast ──────────────────────────────────────
# def check_lstm(anomaly=False):
#     try:
#         r = requests.get(f"{BASE_URL}/lstm-forecast", params={"anomaly": anomaly}).json()
#         trend = r["trend"]
#         critical = r["predicted_critical"]
#         next_temps = r["next_10_temps"]
#         max_temp = max(next_temps)

#         print(f"[LSTM] Trend: {trend} | Max predicted: {round(max_temp)}°C | Critical: {critical}")

#         if critical:
#             critical_beep()
#             speak(f"LSTM forecast warning! Temperature predicted to reach {round(max_temp)} degrees in upcoming readings. Critical threshold will be exceeded!")
#         elif trend == "RISING":
#             beep()
#             speak(f"Temperature trend is rising. Predicted to reach {round(max_temp)} degrees. Monitor closely.")

#     except Exception as e:
#         print(f"[ERROR] LSTM check failed: {e}")

# # ─── Check Alert Log ──────────────────────────────────────────
# def check_alerts():
#     try:
#         r = requests.get(f"{BASE_URL}/alert-log").json()
#         alerts = r["alerts"]
#         critical_count = sum(1 for a in alerts if a["level"] == "CRITICAL")

#         if critical_count > 5:
#             beep(2)
#             speak(f"Alert log warning. {critical_count} critical alerts recorded in the last monitoring cycle.")
#             print(f"[ALERTS] {critical_count} critical alerts in log")

#     except Exception as e:
#         print(f"[ERROR] Alert log check failed: {e}")

# # ─── Main Monitoring Loop ─────────────────────────────────────
# def run_monitor(anomaly_mode=False):
#     speak("Nuclear Guard AI voice monitoring system online. All systems initializing.")
#     time.sleep(2)

#     cycle = 0
#     while True:
#         cycle += 1
#         print(f"\n{'='*50}")
#         print(f"[CYCLE {cycle}] Scanning all systems...")
#         print(f"{'='*50}")

#         # Run all checks
#         check_sensors(anomaly=anomaly_mode)
#         time.sleep(1)
#         check_anomaly(anomaly=anomaly_mode)
#         time.sleep(1)
#         check_risk(anomaly=anomaly_mode)
#         time.sleep(1)
#         check_maintenance(anomaly=anomaly_mode)
#         time.sleep(1)
#         check_lstm(anomaly=anomaly_mode)
#         time.sleep(1)
#         check_alerts()

#         print(f"\n[CYCLE {cycle}] Scan complete. Next scan in 15 seconds...")
#         time.sleep(15)

# if __name__ == "__main__":
#     import sys

#     # Run with anomaly mode: python voiceassist.py anomaly
#     # Run normal mode:       python voiceassist.py
#     anomaly = len(sys.argv) > 1 and sys.argv[1] == "anomaly"

#     if anomaly:
#         print("[MODE] ANOMALY SIMULATION MODE — Emergency alerts active")
#     else:
#         print("[MODE] NORMAL MONITORING MODE")

#     run_monitor(anomaly_mode=anomaly)