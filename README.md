NuclearGuard AI

A simulated AI-powered monitoring dashboard for a nuclear plant's sensor and equipment health — built to explore how anomaly detection, predictive maintenance, and time-series forecasting could work together in a real-time safety monitoring system.

This is a simulation. All sensor data is synthetically generated with NumPy — there is no connection to any real reactor, plant, or hardware. This project is for learning, demoing, and experimenting with ML pipelines, not for actual nuclear safety operations.

What it does

NuclearGuard AI spins up a fake nuclear plant, streams "sensor readings" (temperature, pressure, neutron flux, coolant flow, vibration, radiation), and runs four different models over that data to figure out if something's wrong:

🔍 Anomaly Detection — an Isolation Forest flags sensor readings that look statistically off
🛠️ Predictive Maintenance — a Random Forest estimates failure probability for five key components (Coolant Pump, Steam Generator, Turbine, Reactor Valve, Heat Exchanger)
📈 Temperature Forecasting — an LSTM predicts the next 10 temperature readings and flags whether a critical threshold is coming up
📋 AI Incident Reports — a local LLM (via Ollama, using mistral) writes a short, readable incident report summarizing current plant status

There's also a rolling alert log, an overall risk score (0–100) that blends all of the above, and a "Simulate Anomaly" toggle so you can watch the system react to a spike in bad readings.


Tech stack
Layer	Tools
Backend / API	FastAPI
ML	- scikit-learn (Isolation Forest, Random Forest), TensorFlow/Keras (LSTM)
LLM  - reports	Ollama (mistral)
Dashboard - 	Streamlit + Plotly
Voice alerts - (optional)	Windows Speech Synthesis via PowerShell


API reference
Endpoint	Description
GET /sensor-data-Latest simulated sensor reading
GET /anomaly-status-Isolation Forest anomaly count + status
GET /maintenance-prediction	Failure probability per component
GET /lstm-forecast-Next 10 predicted temperature values + trend
GET /risk-score-Combined 0–100 risk score with severity level
GET /incident-report-LLM-generated incident summary
GET /alert-log-Rolling log of the last 20 alerts
All endpoints accept an optional ?anomaly=true query param to inject a simulated fault into the generated data, useful for testing how the models and dashboard react.


How the risk score works

The overall risk score blends four signals:

Number of anomalies detected (capped contribution)
Number of components flagged "Critical" (heavily weighted)
Number of components flagged "Warning" (lightly weighted)
How far average temperature has drifted above the normal baseline

The result is a single 0–100 number mapped to LOW → MODERATE → HIGH → CRITICAL.

Notes & limitations
Sensor data is randomly generated on every request — there's no persistence or real historical dataset behind it.
The LSTM is trained from scratch on every forecast request (3 epochs), so it's meant to demonstrate the pipeline rather than produce production-grade forecasts.
The incident report quality depends entirely on your local mistral model — swap in a different Ollama model if you'd like.
voiceassist.py is Windows-only as written; it'd need to be adapted (e.g., pyttsx3 or gTTS) to run cross-platform.
Ideas for extending this
Swap synthetic data for a real historical sensor dataset
Persist alerts/readings to a database instead of an in-memory list
Add authentication before exposing this beyond localhost
Containerize the backend + dashboard with Docker Compose
Cross-platform voice alerts

Built as a demo/learning project exploring applied ML for safety-critical-style monitoring systems.
