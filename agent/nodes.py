import ast
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.state import AgentState
from agent.tools import check_security_group_port

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
llm_with_tools = llm.bind_tools([check_security_group_port])

def validate_python_syntax(code: str) -> bool:
    """Returns True if the code is valid Python syntax."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

async def analyze_alert(state: AgentState) -> dict:
    """Node 1: Classify the incoming security alert."""
    prompt = f"""
    You are an autonomous DevSecOps AI agent. 
    An alert was triggered: '{state['alert_event_name']}' on resource '{state['alert_resource_id']}'.
    Analyze this alert and use your tools to investigate the security configuration.
    Details: {state['alert_details']}
    """
    response = await llm_with_tools.ainvoke(prompt)
    
    # In a real scenario, we might parse this structured output or route it to tools
    # We simulate populating state fields here.
    return {
        "threat_classification": "UNAUTHORIZED_PORT_EXPOSURE",
        "threat_score": 9,
        "messages": [response]
    }

async def plan_remediation(state: AgentState) -> dict:
    """Node 2: Generate a Boto3 remediation script."""
    # Simulating LLM code generation
    script = f"""
import boto3

def remediate():
    print("Revoking port 22 on {state['alert_resource_id']}")
    return True
"""
    # Simulate an error on the first pass just to test the retry loop
    if state.get("retry_count", 0) == 0:
        script = "import boto3\ndef remediate(:"
    
    is_valid = validate_python_syntax(script)
    
    return {
        "remediation_script": script,
        "remediation_valid": is_valid,
        "retry_count": state.get("retry_count", 0) + 1,
        "messages": [AIMessage(content=f"Generated script (valid={is_valid}):\n{script}")]
    }

async def execute_remediation(state: AgentState) -> dict:
    """Node 3: Validate and mock-execute the script."""
    return {
        "execution_status": "SUCCESS",
        "execution_output": f"Executed remediation for {state['alert_resource_id']}.",
        "messages": [AIMessage(content="Remediation executed successfully.")]
    }
