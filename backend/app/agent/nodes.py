import ast
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from app.agent.state import AgentState
from app.agent.tools import check_security_group_port, revoke_security_group_ingress, block_public_s3_access

load_dotenv()

llm = ChatOllama(model="llama3.2:3b", temperature=0.1)
llm_with_tools = llm.bind_tools([check_security_group_port, revoke_security_group_ingress, block_public_s3_access])

# 2. The Heavy Reasoning Model specifically for Code Generation
llm_coder = ChatOllama(model="llama3.2:3b", temperature=0.1)

def validate_python_syntax(code: str) -> bool:
    """Returns True if the code is valid Python syntax."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

async def analyze_alert(state: AgentState) -> dict:
    """Node 1: Classify the incoming security alert."""
    messages = state.get("messages", [])
    if not messages:
        # Initial prompt
        prompt = f"""
        You are an autonomous DevSecOps AI agent. 
        An alert was triggered: '{state['alert_event_name']}' on resource '{state['alert_resource_id']}'.
        Analyze this alert and use your tools to investigate the security configuration.
        Details: {state['alert_details']}
        """
        messages = [HumanMessage(content=prompt)]
        
    response = await llm_with_tools.ainvoke(messages)
    
    return {
        "messages": [response]
    }

async def plan_remediation(state: AgentState) -> dict:
    """Node 2: Generate a Boto3 remediation script."""
    
    # 1. Prompt engineering specifically for code generation
    prompt = f"""
    You are a Senior Cloud Security Engineer. Write a Python script using the Boto3 library to remediate the following AWS security alert:
    
    Alert Type: {state['alert_event_name']}
    Resource ID: {state['alert_resource_id']}
    Details: {state['alert_details']}
    
    STRICT REQUIREMENTS:
    1. The script MUST define a main function called `remediate()`.
    2. Since we do not have live AWS credentials yet, mock the boto3 client calls but write the exact syntax that would be used in production.
    3. Output ONLY the raw Python code. Do NOT wrap it in markdown code blocks (like ```python). Do not include any text explanations.
    
    Is this a retry attempt due to previous syntax failure? {'Yes, fix your syntax errors.' if state.get('retry_count', 0) > 0 else 'No'}
    """
    
    # 2. Invoke the LLM (Notice we use 'llm' here, not 'llm_with_tools', because we just want code output)
    response = await llm_coder.ainvoke(prompt)
    script = response.content.strip()
    
    # 3. Clean up the output (LLMs love to add markdown backticks even when told not to)
    if script.startswith("```python"):
        script = script[9:]
    elif script.startswith("```"):
        script = script[3:]
    if script.endswith("```"):
        script = script[:-3]
        
    script = script.strip()
    
    # 4. Guardrail validation
    is_valid = validate_python_syntax(script)
    
    return {
        "remediation_script": script,
        "remediation_valid": is_valid,
        "retry_count": state.get("retry_count", 0) + 1,
        "messages": [AIMessage(content=f"Generated script (valid={is_valid}):\n\n{script}")]
    }

async def execute_remediation(state: AgentState) -> dict:
    """Node 3: Validate and mock-execute the script."""
    return {
        "execution_status": "SUCCESS",
        "execution_output": f"Executed remediation for {state['alert_resource_id']}.",
        "messages": [AIMessage(content="Remediation executed successfully.")]
    }
