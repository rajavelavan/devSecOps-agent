from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import analyze_alert, plan_remediation, execute_remediation

def should_retry(state: AgentState) -> str:
    """Conditional edge: decide whether to loop back or proceed."""
    if not state.get("remediation_valid") and state.get("retry_count", 0) < 3:
        return "retry"   # loops back to plan_remediation
    return "execute"     # proceeds to execute_remediation

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze_alert", analyze_alert)
workflow.add_node("plan_remediation", plan_remediation)
workflow.add_node("execute_remediation", execute_remediation)

# Define edges
workflow.set_entry_point("analyze_alert")
workflow.add_edge("analyze_alert", "plan_remediation")
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
