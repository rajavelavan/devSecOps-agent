from langchain_core.tools import tool

@tool
def check_security_group_port(security_group_id: str, port: int) -> str:
    """
    Checks if a specific port is open to the world (0.0.0.0/0) on a given AWS Security Group.
    """
    print(f"--> [TOOL EXECUTED] AI is checking {security_group_id} for port {port}...")
    
    if (security_group_id == "sg-12345" or "sg-0123456789abcdef0" in security_group_id) and port == 22:
        return "CRITICAL: Port 22 is open to 0.0.0.0/0. Immediate remediation required."
    
    return f"Port {port} is secure on {security_group_id}."
