from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.agent.state import AgentState
from app.agent.nodes import analyze_alert, plan_remediation, execute_remediation
from app.agent.tools import check_security_group_port, revoke_security_group_ingress, block_public_s3_access

def should_continue(state: AgentState) -> str:
    """Determine what to do after analyze_alert."""
    messages = state.get("messages", [])
    last_message = messages[-1]
    
    # If the LLM makes a tool call, route to tools
    if last_message.tool_calls:
        return "tools"
    
    # If the analysis is complete, decide whether to remediate.
    # We can use a heuristic (e.g. if the word 'CRITICAL' or 'remediate' is in the text)
    # or rely on structured output. For now, if there are no tool calls, it proceeds to plan_remediation.
    # In a real enterprise system, we would parse structured output here.
    content = str(last_message.content).lower()
    if "secure" in content and "critical" not in content:
        return "end"
        
    return "remediate"

def should_retry(state: AgentState) -> str:
    """Conditional edge: decide whether to loop back or proceed."""
    if not state.get("remediation_valid") and state.get("retry_count", 0) < 3:
        return "retry"   # loops back to plan_remediation
    return "execute"     # proceeds to execute_remediation

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze_alert", analyze_alert)
workflow.add_node("tools", ToolNode([check_security_group_port, revoke_security_group_ingress, block_public_s3_access]))
workflow.add_node("plan_remediation", plan_remediation)
workflow.add_node("execute_remediation", execute_remediation)

# Define edges
workflow.set_entry_point("analyze_alert")

workflow.add_conditional_edges(
    "analyze_alert",
    should_continue,
    {
        "tools": "tools",
        "remediate": "plan_remediation",
        "end": END
    }
)

workflow.add_edge("tools", "analyze_alert")

workflow.add_conditional_edges(
    "plan_remediation",
    should_retry,
    {
        "retry": "plan_remediation",   # self-correction loop
        "execute": "execute_remediation"
    }
)
workflow.add_edge("execute_remediation", END)

# Compile the graph into a runnable
agent_graph = workflow.compile()
