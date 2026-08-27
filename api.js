const API_URL = 'http://127.0.0.1:8000'


export async function getSensorData() {

  const response = await fetch(
    `${API_URL}/sensor-data`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch sensor data')
  }

  return response.json()
}


export async function getRiskScore() {

  const response = await fetch(
    `${API_URL}/risk-score`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch risk score')
  }

  return response.json()
}


export async function getAnomalyStatus() {

  const response = await fetch(
    `${API_URL}/anomaly-status`
  )

  if (!response.ok) {
    throw new Error('Failed to run anomaly detection')
  }

  return response.json()
}


export async function getMaintenancePrediction() {

  const response = await fetch(
    `${API_URL}/maintenance-prediction`
  )

  if (!response.ok) {
    throw new Error('Failed to run maintenance prediction')
  }

  return response.json()
}


export async function getLstmForecast() {

  const response = await fetch(
    `${API_URL}/lstm-forecast`
  )

  if (!response.ok) {
    throw new Error('Failed to run LSTM forecast')
  }

  return response.json()
}


export async function getIncidentReport() {

  const response = await fetch(
    `${API_URL}/incident-report`
  )

  if (!response.ok) {
    throw new Error('Failed to generate incident report')
  }

  return response.json()
}