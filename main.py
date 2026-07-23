from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title= "Autonomous Cloud Security Agent")

class SecurityAlert(BaseModel):
    event_name: str
    resource_id: str
    resource_type: str
    details: dict

@app.get("/")
async def health_check():
    return {"status": "Active", "agent": "DevSecOps AI Engine"}

@app.post("/webhook/aws-alert")
async def receive_alert(alert: SecurityAlert):
    print(f"[ALERT RECEIVED] {alert.event_name} on {alert.resource_id}")
    return {"message": "Alert ingested successfully", "data": alert}