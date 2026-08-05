from typing import TypedDict, Optional, Annotated
from operator import add
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # Input: the raw incoming alert
    alert_event_type: str
    alert_event_name: str
    alert_resource_id: str
    alert_severity: str
    alert_details: str

    # Analysis results (written by analyze_alert node)
    threat_classification: Optional[str]
    threat_score: Optional[int]

    # Remediation plan (written by plan_remediation node)
    remediation_script: Optional[str]
    remediation_valid: Optional[bool]

    # Execution results (written by execute_remediation node)
    execution_status: Optional[str]
    execution_output: Optional[str]

    # Loop control
    retry_count: int
    messages: Annotated[list[BaseMessage], add]
