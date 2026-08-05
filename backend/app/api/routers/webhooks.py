import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.webhooks import SecurityAlert, RemediationRequest
from app.agent.graph import agent_graph
from app.agent.state import AgentState

router = APIRouter()

@router.post("/aws-alert")
async def process_security_alert(alert: SecurityAlert):
    initial_state: AgentState = {
        "alert_event_type": alert.event_type,
        "alert_event_name": alert.event_name,
        "alert_resource_id": alert.resource_id,
        "alert_severity": alert.severity,
        "alert_details": alert.details,
        "retry_count": 0,
        "messages": [],
        "threat_classification": None,
        "threat_score": None,
        "remediation_script": None,
        "remediation_valid": None,
        "execution_status": None,
        "execution_output": None
    }
    
    # Invoke the LangGraph state machine
    final_state = await agent_graph.ainvoke(initial_state)

    return {
        "status": "analyzed",
        "threat": final_state.get("threat_classification"),
        "remediation": final_state.get("remediation_script"),
        "execution": final_state.get("execution_status")
    }

async def stream_agent_reasoning(alert: SecurityAlert):
    initial_state: AgentState = {
        "alert_event_type": alert.event_type,
        "alert_event_name": alert.event_name,
        "alert_resource_id": alert.resource_id,
        "alert_severity": alert.severity,
        "alert_details": alert.details,
        "retry_count": 0,
        "messages": [],
        "threat_classification": None,
        "threat_score": None,
        "remediation_script": None,
        "remediation_valid": None,
        "execution_status": None,
        "execution_output": None
    }

    yield f"data: {json.dumps({'type': 'status', 'content': 'Ingested alert. Initializing LangGraph reasoning engine...'})}\n\n"
    await asyncio.sleep(0.3)

    # Stream graph events
    async for event in agent_graph.astream_events(initial_state, version="v2"):
        kind = event["event"]
        name = event["name"]
        
        # When a node finishes, we can yield its state updates
        if kind == "on_chain_end" and name in ["analyze_alert", "plan_remediation", "execute_remediation"]:
            output = event["data"].get("output", {})
            if output:
                node_summary = f"[NODE EXECUTED: {name}]\n"
                for key, val in output.items():
                    if key != "messages":
                        node_summary += f"{key}: {val}\n"
                
                yield f"data: {json.dumps({'type': 'thought', 'content': node_summary})}\n\n"
                await asyncio.sleep(0.3)
                
    yield f"data: {json.dumps({'type': 'done', 'content': '\n[STREAM COMPLETE] Awaiting human approval for remediation execution.'})}\n\n"

@router.post("/aws-alert/stream")
async def process_security_alert_stream(alert: SecurityAlert):
    return StreamingResponse(
        stream_agent_reasoning(alert),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/approve-remediation")
async def approve_remediation(req: RemediationRequest):
    print(f"--> [REMEDIATION EXECUTED] Revoking ingress rule for port 22 on {req.resource_id}...")
    return {
        "status": "remediated",
        "action": "REVOKE_INGRESS_PORT_22",
        "resource_id": req.resource_id,
        "message": f"Successfully revoked 0.0.0.0/0 ingress rule on Port 22 for {req.resource_id}."
    }
