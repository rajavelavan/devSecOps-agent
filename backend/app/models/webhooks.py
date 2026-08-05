from pydantic import BaseModel

class SecurityAlert(BaseModel):
    event_type: str
    event_name: str
    resource_id: str
    resource_type: str
    details: str
    severity: str

class RemediationRequest(BaseModel):
    resource_id: str
