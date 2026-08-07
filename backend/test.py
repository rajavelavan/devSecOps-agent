import asyncio

from app.agent.graph import agent_graph

async def main():
    initial_state = {
        "alert_event_type": "SecurityGroupModification",
        "alert_event_name": "AuthorizeSecurityGroupIngress",
        "alert_resource_id": "sg-12345",
        "alert_severity": "High",
        "alert_details": "Port 22 opened to 0.0.0.0/0",
        "retry_count": 0,
        "messages": [],
        "threat_classification": None,
        "threat_score": None,
        "remediation_script": None,
        "remediation_valid": None,
        "execution_status": None,
        "execution_output": None
    }
    print("Invoking agent graph...")
    final_state = await agent_graph.ainvoke(initial_state)
    print("Done!")
    print("Threat:", final_state.get("threat_classification"))
    print("Remediation Script:\n", final_state.get("remediation_script"))

if __name__ == "__main__":
    asyncio.run(main())
