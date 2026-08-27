import { useEffect, useState } from 'react'
import {
  getSensorData,
  getRiskScore,
  getAnomalyStatus,
  getMaintenancePrediction,
  getLstmForecast,
  getIncidentReport,
} from './api'

import './App.css'

function App() {
  const [sensorData, setSensorData] = useState(null)
  const [riskScore, setRiskScore] = useState(null)

  const [anomaly, setAnomaly] = useState(null)
  const [maintenance, setMaintenance] = useState(null)
  const [forecast, setForecast] = useState(null)
  const [incident, setIncident] = useState(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [actionLoading, setActionLoading] = useState(false)

  // ============================================================
  // LOAD DASHBOARD
  // ============================================================

  async function loadDashboard() {
    try {
      setError(null)

      const data = await getSensorData()
      const risk = await getRiskScore()

      setSensorData(data)
      setRiskScore(risk)

    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Load when page opens
  useEffect(() => {
    loadDashboard()
  }, [])


  // ============================================================
  // ANOMALY DETECTION
  // ============================================================

  async function handleAnomaly() {
    try {
      setActionLoading(true)

      const result = await getAnomalyStatus()

      setAnomaly(result)

    } catch (err) {
      setError(err.message)
    } finally {
      setActionLoading(false)
    }
  }


  // ============================================================
  // MAINTENANCE
  // ============================================================

  async function handleMaintenance() {
    try {
      setActionLoading(true)

      const result = await getMaintenancePrediction()

      setMaintenance(result)

    } catch (err) {
      setError(err.message)
    } finally {
      setActionLoading(false)
    }
  }


  // ============================================================
  // LSTM FORECAST
  // ============================================================

  async function handleForecast() {
    try {
      setActionLoading(true)

      const result = await getLstmForecast()

      setForecast(result)

    } catch (err) {
      setError(err.message)
    } finally {
      setActionLoading(false)
    }
  }


  // ============================================================
  // INCIDENT REPORT
  // ============================================================

  async function handleIncident() {
    try {
      setActionLoading(true)

      const result = await getIncidentReport()

      setIncident(result)

    } catch (err) {
      setError(err.message)
    } finally {
      setActionLoading(false)
    }
  }


  // ============================================================
  // LOADING
  // ============================================================

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          Loading reactor data...
        </div>
      </div>
    )
  }


  // ============================================================
  // ERROR
  // ============================================================

  if (error && !sensorData) {
    return (
      <div className="app">
        <div className="error">
          <h2>Connection Error</h2>
          <p>{error}</p>

          <button onClick={loadDashboard}>
            Retry Connection
          </button>
        </div>
      </div>
    )
  }


  // ============================================================
  // RISK COLOR
  // ============================================================

  const riskColor =
    riskScore?.risk_level === 'CRITICAL'
      ? '#ff4444'
      : riskScore?.risk_level === 'HIGH'
        ? '#ff8800'
        : riskScore?.risk_level === 'MODERATE'
          ? '#ffff00'
          : '#00ff88'


  // ============================================================
  // UI
  // ============================================================

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div>
          <h1>NuclearGuard AI</h1>

          <p>
            AI-Powered Nuclear Plant Monitoring System
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>

      </header>


      <main>

        {/* REACTOR OVERVIEW */}

        <section className="overview">

          <div>

            <h2>
              Reactor Overview
            </h2>

            <p>
              Real-time monitoring and predictive analysis
            </p>

          </div>


          <div
            className="risk"
            style={{ color: riskColor }}
          >

            <span>
              Risk Score
            </span>

            <strong>
              {riskScore?.risk_score}%
            </strong>

            <small>
              {riskScore?.risk_level}
            </small>

          </div>

        </section>


        {/* SENSOR CARDS */}

        <section className="sensor-grid">

          <div className="card">

            <span className="label">
              TEMPERATURE
            </span>

            <strong>
              {sensorData.temperature} °C
            </strong>

            <span className="normal">
              NORMAL
            </span>

          </div>


          <div className="card">

            <span className="label">
              PRESSURE
            </span>

            <strong>
              {sensorData.pressure}
            </strong>

            <span className="normal">
              NORMAL
            </span>

          </div>


          <div className="card">

            <span className="label">
              NEUTRON FLUX
            </span>

            <strong>
              {sensorData.neutron_flux.toExponential(1)}
            </strong>

            <span className="normal">
              NORMAL
            </span>

          </div>


          <div className="card">

            <span className="label">
              COOLANT FLOW
            </span>

            <strong>
              {sensorData.coolant_flow}
            </strong>

            <span className="normal">
              NORMAL
            </span>

          </div>


          <div className="card">

            <span className="label">
              VIBRATION
            </span>

            <strong>
              {sensorData.vibration}
            </strong>

            <span className="normal">
              NORMAL
            </span>

          </div>


          <div className="card">

            <span className="label">
              RADIATION LEVEL
            </span>

            <strong>
              {sensorData.radiation_level}
            </strong>

            <span className="normal">
              NORMAL
            </span>

          </div>

        </section>


        {/* AI MODULES */}

        <section className="modules">


          {/* ANOMALY */}

          <div className="module">

            <h3>
              🔍 Anomaly Detection
            </h3>

            <p>
              Monitor abnormal reactor conditions
              using machine learning.
            </p>

            <button
              onClick={handleAnomaly}
              disabled={actionLoading}
            >
              {actionLoading
                ? 'Analyzing...'
                : 'View Analysis'}
            </button>


            {anomaly && (

              <div className="result">

                <strong>
                  {anomaly.status}
                </strong>

                <p>
                  Anomalies detected:
                  {' '}
                  {anomaly.anomaly_count}
                </p>

                <p>
                  Total readings:
                  {' '}
                  {anomaly.total_readings}
                </p>

              </div>

            )}

          </div>


          {/* MAINTENANCE */}

          <div className="module">

            <h3>
              🔧 Maintenance Prediction
            </h3>

            <p>
              Predict potential equipment failures
              before they occur.
            </p>

            <button
              onClick={handleMaintenance}
              disabled={actionLoading}
            >
              {actionLoading
                ? 'Analyzing...'
                : 'View Predictions'}
            </button>


            {maintenance && (

              <div className="result">

                {maintenance.components.map(
                  (component) => (

                    <div
                      className="maintenance-item"
                      key={component.component}
                    >

                      <strong>
                        {component.component}
                      </strong>

                      <span>
                        {component.failure_probability}%
                      </span>

                      <small>
                        {component.status}
                      </small>

                    </div>

                  )
                )}

              </div>

            )}

          </div>


          {/* LSTM */}

          <div className="module">

            <h3>
              📈 LSTM Forecast
            </h3>

            <p>
              Forecast future reactor temperature
              and operating conditions.
            </p>

            <button
              onClick={handleForecast}
              disabled={actionLoading}
            >
              {actionLoading
                ? 'Predicting...'
                : 'View Forecast'}
            </button>


            {forecast && (

              <div className="result">

                <p>
                  Trend:
                  {' '}
                  <strong>
                    {forecast.trend}
                  </strong>
                </p>

                <p>
                  Next 10 predicted temperatures:
                </p>

                <div className="forecast-values">

                  {forecast.next_10_temps.map(
                    (temp, index) => (

                      <span key={index}>
                        {temp}°C
                      </span>

                    )
                  )}

                </div>

                {forecast.predicted_critical && (

                  <strong className="critical">
                    ⚠ Critical temperature predicted
                  </strong>

                )}

              </div>

            )}

          </div>


          {/* INCIDENT REPORT */}

          <div className="module">

            <h3>
              🚨 Incident Report
            </h3>

            <p>
              Review detected incidents and
              system alerts.
            </p>

            <button
              onClick={handleIncident}
              disabled={actionLoading}
            >
              {actionLoading
                ? 'Generating...'
                : 'View Reports'}
            </button>


            {incident && (

              <div className="result incident">

                <p>
                  {incident.report}
                </p>

                <small>
                  Generated:
                  {' '}
                  {incident.generated_at}
                </small>

              </div>

            )}

          </div>

        </section>

      </main>

    </div>
  )
}

export default App
