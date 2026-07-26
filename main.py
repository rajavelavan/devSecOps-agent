import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title= "Autonomous Cloud Security Agent")

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
    # Mock logic representing an AWS Boto3 call
    print(f"--> [TOOL EXECUTED] AI is checking {security_group_id} for port {port}...")
    
    if security_group_id == "sg-12345" and port == 22:
        return "CRITICAL: Port 22 is open to 0.0.0.0/0. Immediate remediation required."
    
    return f"Port {port} is secure on {security_group_id}."

# ---------------------------------------------------------
# 2. Initialize the AI Model and bind the tool
# ---------------------------------------------------------
# We use gemini-1.5-flash as it is highly capable and free
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
    # Create a prompt for the AI based on the incoming webhook
    prompt = f"""
    You are an autonomous DevSecOps AI agent. 
    An alert was triggered: '{alert.event_name}' on resource '{alert.resource_id}'.
    Analyze this alert and use your tools to investigate the security configuration.
    """
    
    # Send the prompt to Gemini
    response = llm_with_tools.invoke(prompt)
    
    # Extract the tool calls Gemini wants to make based on its reasoning
    tool_calls = response.tool_calls

    return {
        "status": "alert_received",
        "received_data": alert.details,
        "agent_thought": "Investigating unauthorized port exposure on " + alert.resource_id
    }