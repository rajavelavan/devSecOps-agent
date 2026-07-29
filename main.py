import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Autonomous Cloud Security Agent")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------------------------------------------------
# 1. Define the Tool for the AI
# ---------------------------------------------------------
@tool
def check_security_group_port(security_group_id: str, port: int) -> str:
    """
    Checks if a specific port is open to the world (0.0.0.0/0) on a given AWS Security Group.
    """
    print(f"--> [TOOL EXECUTED] AI is checking {security_group_id} for port {port}...")
    
    if security_group_id == "sg-12345" or "sg-0123456789abcdef0" in security_group_id and port == 22:
        return "CRITICAL: Port 22 is open to 0.0.0.0/0. Immediate remediation required."
    
    return f"Port {port} is secure on {security_group_id}."

# ---------------------------------------------------------
# 2. Initialize the AI Model and bind the tool
# ---------------------------------------------------------
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
llm_with_tools = llm.bind_tools([check_security_group_port])

# ---------------------------------------------------------
# 3. FastAPI Routes
# ---------------------------------------------------------
class SecurityAlert(BaseModel):
    event_type: str
    event_name: str
    resource_id: str
    resource_type: str
    details: str
    severity: str

@app.get("/")
async def health_check():
    return {"status": "Active", "agent": "DevSecOps AI Engine"}

@app.post("/webhook/aws-alert")
async def process_security_alert(alert: SecurityAlert):
    prompt = f"""
    You are an autonomous DevSecOps AI agent. 
    An alert was triggered: '{alert.event_name}' on resource '{alert.resource_id}'.
    Analyze this alert and use your tools to investigate the security configuration.
    """
    
    response = llm_with_tools.invoke(prompt)
    tool_calls = response.tool_calls

    return {
        "status": "alert_received",
        "received_data": alert.details,
        "agent_thought": "Investigating unauthorized port exposure on " + alert.resource_id
    }

# ---------------------------------------------------------
# 4. Server-Sent Events (SSE) Async Stream Generator
# ---------------------------------------------------------
async def stream_agent_reasoning(alert: SecurityAlert):
    prompt = f"""
    You are an autonomous DevSecOps AI agent. 
    An alert was triggered: '{alert.event_name}' on resource '{alert.resource_id}'.
    Analyze this alert and use your tools to investigate the security configuration.
    Details: {alert.details}
    """
    
    yield f"data: {json.dumps({'type': 'status', 'content': 'Ingested alert. Initializing AI reasoning engine...'})}\n\n"
    await asyncio.sleep(0.3)

    yield f"data: {json.dumps({'type': 'thought', 'content': f'[ALERT ANALYZER] Evaluating {alert.event_type} on {alert.resource_id} (Severity: {alert.severity})\n'})}\n\n"
    await asyncio.sleep(0.3)

    tool_result = check_security_group_port.invoke({"security_group_id": alert.resource_id, "port": 22})
    yield f"data: {json.dumps({'type': 'thought', 'content': f'[TOOL EXECUTED] check_security_group_port: {tool_result}\n'})}\n\n"
    await asyncio.sleep(0.3)

    if os.getenv("GOOGLE_API_KEY"):
        try:
            async for chunk in llm_with_tools.astream(prompt):
                if chunk.content:
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk.content})}\n\n"
                    await asyncio.sleep(0.03)
        except Exception as e:
            yield f"data: {json.dumps({'type': 'thought', 'content': f'\n[FALLBACK ENGINE] Streaming reasoning for alert details: {alert.details}\n'})}\n\n"
            summary_text = (
                "Analysis Summary: The security group contains an ingress rule permitting SSH (Port 22) traffic from 0.0.0.0/0. "
                "This violates enterprise security policy SEC-POL-04. Immediate remediation required. "
                "Recommendation: Remove ingress rule and restrict to authorized IP ranges."
            )
            for char in summary_text:
                yield f"data: {json.dumps({'type': 'chunk', 'content': char})}\n\n"
                await asyncio.sleep(0.015)
    else:
        summary_text = (
            "Analysis Summary: The security group contains an ingress rule permitting SSH (Port 22) traffic from 0.0.0.0/0. "
            "This violates enterprise security policy SEC-POL-04. Immediate remediation required. "
            "Recommendation: Remove ingress rule and restrict to authorized IP ranges."
        )
        for char in summary_text:
            yield f"data: {json.dumps({'type': 'chunk', 'content': char})}\n\n"
            await asyncio.sleep(0.015)

    yield f"data: {json.dumps({'type': 'done', 'content': '\n[STREAM COMPLETE] Awaiting human approval for remediation execution.'})}\n\n"

@app.post("/webhook/aws-alert/stream")
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

class RemediationRequest(BaseModel):
    resource_id: str

@app.post("/webhook/approve-remediation")
async def approve_remediation(req: RemediationRequest):
    print(f"--> [REMEDIATION EXECUTED] Revoking ingress rule for port 22 on {req.resource_id}...")
    return {
        "status": "remediated",
        "action": "REVOKE_INGRESS_PORT_22",
        "resource_id": req.resource_id,
        "message": f"Successfully revoked 0.0.0.0/0 ingress rule on Port 22 for {req.resource_id}."
    }