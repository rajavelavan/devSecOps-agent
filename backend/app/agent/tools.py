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

@tool
def revoke_security_group_ingress(security_group_id: str, port: int) -> str:
    """
    Simulates revoking an inbound rule that allows all traffic (0.0.0.0/0) on a specific port
    for a given AWS Security Group. This is a mock of the boto3 EC2 revoke_security_group_ingress call.
    """
    print(f"--> [TOOL EXECUTED] AI is revoking port {port} on {security_group_id}...")
    
    # Simulate the boto3 mutation without a real AWS call
    return (
        f"SUCCESS: Inbound rule for port {port} (0.0.0.0/0) has been revoked "
        f"from Security Group '{security_group_id}'. "
        f"[SIMULATED boto3: ec2.revoke_security_group_ingress()]"
    )

@tool
def block_public_s3_access(bucket_name: str) -> str:
    """
    Simulates attaching an S3 Block Public Access configuration to the specified S3 bucket,
    preventing any public access policies or ACLs from taking effect.
    This is a mock of the boto3 S3 put_public_access_block call.
    """
    print(f"--> [TOOL EXECUTED] AI is blocking public access on S3 bucket '{bucket_name}'...")
    
    # Simulate the boto3 mutation without a real AWS call
    return (
        f"SUCCESS: Block Public Access has been enabled on S3 bucket '{bucket_name}'. "
        f"All public ACLs and bucket policies granting public access are now blocked. "
        f"[SIMULATED boto3: s3.put_public_access_block()]"
    )
