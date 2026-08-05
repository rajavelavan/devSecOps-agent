import { useState } from 'react';

interface Alert {
  event_type: string;
  event_name: string;
  resource_id: string;
  resource_type: string;
  details: string;
  severity: string;
}

function App() {
  const [alert, setAlert] = useState<Alert | null>(null);
  const [agentThoughts, setAiThoughts] = useState<string>("");
  const [status, setStatus] = useState<string>("Idle");

  // Simulated trigger alert function with Real-Time SSE Streaming
  const triggerSimulatedAlert = async () => {
    setStatus("Connecting Stream...");
    setAiThoughts("");
    
    const payload = {
      event_type: "UNAUTHORIZED_PORT_OPEN",
      event_name: "Port open",
      resource_id: "sg-0123456789abcdef0",
      resource_type: "Normal",
      details: "Port 22 open to 0.0.0.0/0 on production security group",
      severity: "CRITICAL"
    };
    
    setAlert(payload);

    try {
      const response = await fetch("http://localhost:8000/webhook/aws-alert/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("Response body is null");
      }
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lineGroups = buffer.split("\n\n");
        // Keep the last incomplete block in the buffer
        buffer = lineGroups.pop() || "";

        for (const group of lineGroups) {
          const line = group.trim();
          if (line.startsWith("data: ")) {
            try {
              const eventData = JSON.parse(line.slice(6));
              if (eventData.type === 'status') {
                setStatus(eventData.content);
              } else if (eventData.type === 'thought' || eventData.type === 'chunk') {
                setAiThoughts((prev) => prev + eventData.content);
              } else if (eventData.type === 'done') {
                setStatus("Stream Finished");
                setAiThoughts((prev) => prev + eventData.content);
              }
            } catch (e) {
              console.error("Error parsing SSE line:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Connection Error:", error);
      setAiThoughts("Error connecting to Python backend stream. Is FastAPI running?");
      setStatus("Connection Failed");
    }
  };

  const handleApproveRemediation = async () => {
    setStatus("Executing Remediation...");
    setAiThoughts((prev) => prev + "\n\n[HUMAN APPROVAL GRANTED] Dispatching remediation command to AWS orchestrator...");

    try {
      const response = await fetch("http://localhost:8000/webhook/approve-remediation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ resource_id: alert?.resource_id || "sg-0123456789abcdef0" }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAiThoughts((prev) => prev + `\n[AWS BOTO3 SUCCESS] ${data.message}\n[POSTURE VERIFIED] Security Group ${data.resource_id} is now SECURE & COMPLIANT.`);
      setStatus("Remediation Executed");
    } catch (error) {
      console.error("Remediation Error:", error);
      setAiThoughts((prev) => prev + "\n[ERROR] Failed to execute remediation request on backend.");
      setStatus("Remediation Error");
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      {/* Header */}
      <header className="border-b border-slate-700 pb-4 mb-8">
        <h1 className="text-3xl font-bold text-sky-400">
          🛡️ Cloud Security Remediation Engine
        </h1>
        <p className="text-slate-400 mt-2 text-lg">
          Autonomous AI Agent Handshake & Live Stream Dashboard
        </p>
      </header>

      {/* Control Panel */}
      <div className="flex gap-4 mb-8">
        <button 
          onClick={triggerSimulatedAlert}
          className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold rounded-lg transition-colors shadow-lg"
        >
          Simulate AWS Security Alert
        </button>

        <button 
          onClick={handleApproveRemediation}
          disabled={!alert}
          className={`px-6 py-3 font-bold rounded-lg transition-colors shadow-lg ${
            alert 
              ? 'bg-green-600 hover:bg-green-500 text-white cursor-pointer' 
              : 'bg-slate-700 text-slate-400 cursor-not-allowed'
          }`}
        >
          Approve Remediation
        </button>
      </div>

      {/* Active Alert Details */}
      {alert && (
        <div className="bg-slate-800 p-6 rounded-xl mb-6 border-l-4 border-red-500 shadow-xl">
          <h3 className="text-red-400 text-xl font-bold mb-3">Active Alert: {alert.event_type}</h3>
          <div className="space-y-2 text-slate-300">
            <p><strong className="text-slate-100">Resource ID:</strong> {alert.resource_id}</p>
            <p><strong className="text-slate-100">Severity:</strong> {alert.severity}</p>
            <p><strong className="text-slate-100">Details:</strong> {alert.details}</p>
          </div>
        </div>
      )}

      {/* AI Agent Thought Stream Output Area */}
      <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 min-h-[200px] shadow-inner">
        <h4 className="text-purple-400 font-bold mb-3 text-lg flex items-center gap-2">
          🤖 Agent Reasoning Stream:
          <span className="text-xs px-2 py-1 bg-purple-900/50 text-purple-300 rounded-full">Status: {status}</span>
        </h4>
        <pre className="text-sky-300 font-mono whitespace-pre-wrap break-words mt-4">
          {agentThoughts || "Awaiting alert execution..."}
        </pre>
      </div>
    </div>
  );
}

export default App;