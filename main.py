from fastapi import FastAPI
from pydantic import BaseModel #create a model for the incident data
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel("models/gemini-3.8-flash")

app = FastAPI()

incidents = [
    {
        "id": 1,
        "title": "Database Timeout",
        "description": "Database connection timed out",
        "severity": "Critical",
        "status": "Open"
    },
    {
        "id": 2,
        "title": "High CPU Usage",
        "description": "CPU usage reached 95 percent",
        "severity": "Medium",
        "status": "Investigating"
    }
]


class Incident(BaseModel):
    title: str
    description: str
    severity: str
    status: str


@app.get("/")
def home():
    return incidents


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/incident/{incident_id}")
def get_incident(incident_id: int):
    for incident in incidents:
        if incident["id"] == incident_id:
            return incident

    return {"error": "Incident not found"}


@app.post("/incident")
def create_incident(incident: Incident):

    new_incident = {
        "id": len(incidents) + 1,
        "title": incident.title,
        "description": incident.description,
        "severity": incident.severity,
        "status": incident.status
    }

    incidents.append(new_incident)

    return new_incident


@app.get("/analyze/{incident_id}")
def analyze_incident(incident_id: int):

    for incident in incidents:

        if incident["id"] == incident_id:

            description = incident["description"].lower()

            if "database" in description:
                return {
                    "root_cause": "Possible database connectivity issue",
                    "suggestion": "Check database connections"
                }

            if "cpu" in description:
                return {
                    "root_cause": "High CPU utilization",
                    "suggestion": "Scale application or investigate heavy processes"
                }

            if "memory" in description:
                return {
                    "root_cause": "Possible memory leak",
                    "suggestion": "Inspect memory consumption"
                }

            if "network" in description:
                return {
                    "root_cause": "Possible network connectivity issue",
                    "suggestion": "Check network configuration and server connectivity"
                }

            return {
                "root_cause": "Unknown",
                "suggestion": "Manual investigation required"
            }

    return {"error": "Incident not found"}


@app.get("/ai-analyze/{incident_id}")
def ai_analyze_incident(incident_id: int):

    for incident in incidents:

        if incident["id"] == incident_id:

            response = model.generate_content(
                f"""
                You are a senior DevOps engineer.

                Analyze this incident:

                Title:
                {incident["title"]}

                Description:
                {incident["description"]}

                Severity:
                {incident["severity"]}

                Provide:

                1. Likely Root Cause
                2. Recommended Action
                3. Priority Level
                """
            )

            return {
                "incident_id": incident_id,
                "analysis": response.text
            }

    return {"error": "Incident not found"}

