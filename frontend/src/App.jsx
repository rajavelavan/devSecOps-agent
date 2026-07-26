import React, { useState } from 'react';

function App() {
  const [alert, setAlert] = useState(null);
  const [agentThoughts, setAiThoughts] = useState("");
  const [status, setStatus] = useState("Idle");

  // Simulated trigger alert function
  const triggerSimulatedAlert = async () => {
    setStatus("Alert Triggered - Contacting AI...");
    setAiThoughts("Sending alert to backend. Awaiting agent reasoning...");
    
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
      const response = await fetch("http://localhost:8000/webhook/aws-alert", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Dump the raw JSON response into our thought stream window for now
      setAiThoughts(JSON.stringify(data, null, 2));
      setStatus("AI Response Received");
      
    } catch (error) {
      console.error("Connection Error:", error);
      setAiThoughts("Error connecting to Python backend. Is FastAPI running?");
      setStatus("Connection Failed");
    }
  };

  const handleApproveRemediation = () => {
    setStatus("Remediation Approved");
    setAiThoughts((prev) => prev + "\n[Action Approved] Executing AWS Security Group fix...");
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