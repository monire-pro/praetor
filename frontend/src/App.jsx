import { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { Terminal, ShieldAlert, Zap, Activity, Lock, Play, Ban, Cpu } from 'lucide-react';
import './App.css';
// Automatically detect if we are running on localhost
const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const API_URL = isLocal 
  ? 'http://127.0.0.1:8000'                  // Local Development
  : 'https://praetor-415d.onrender.com';     // Live Production
export default function App() {
  const [status, setStatus] = useState(null);
  const [goal, setGoal] = useState("");
  const [limit, setLimit] = useState(100);
  
  // Create a ref for the Terminal container itself
  const terminalRef = useRef(null); 

  // Poll Backend every 1s
  useEffect(() => {
    const interval = setInterval(fetchStatus, 1000);
    fetchStatus();
    return () => clearInterval(interval);
  }, []);

  // AUTO-SCROLL LOGIC: This only scrolls the terminal box, not the whole page
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [status?.logs]);

  const fetchStatus = async () => {
    try {
      const res = await fetch(`${API_URL}/status`);
      if (!res.ok) throw new Error("Offline");
      const data = await res.json();
      setStatus(data);
    } catch (e) { 
      // Fallback/Mock data for UI testing if backend is offline
      console.log("Connecting to core...");
    }
  };

  const runAgent = async () => {
    if (!goal) return;
    try {
      await fetch(`${API_URL}/run-agent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal })
      });
      setGoal("");
    } catch(e) { console.error(e) }
  };

  const updateLimit = async (val) => {
    setLimit(val);
    try {
      await fetch(`${API_URL}/set-limit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ limit: parseFloat(val) })
      });
    } catch(e) { console.error(e) }
  };

  const abortAgent = async () => {
    try { await fetch(`${API_URL}/abort`, { method: 'POST' }); } catch(e) {}
  };

  if (!status) return (
    <div className="dashboard" style={{display:'flex', height:'100vh', justifyContent:'center', alignItems:'center'}}>
      <div className="loading" style={{color: '#00ff41', fontFamily: 'monospace'}}>INITIALIZING NEURAL LINK...</div>
    </div>
  );

  return (
    <>
      <div className="scanlines"></div>
      <div className="dashboard">
        
        {/* HEADER - Now stays at the top */}
        <header>
          <div className="brand">
            <Zap size={28} className="icon-neon" />
            <div>
              <h1>PRAETOR_AGI</h1>
              <span className="version">SYS.VER.1.0.4</span>
            </div>
          </div>
          <div className="stats">
            <div className="stat-box">
              <span className="label">Treasury</span>
              <span className="value mnee">{status.balance?.toFixed(2) || "0.00"} MNEE</span>
            </div>
            <div className="stat-box">
              <span className="label">System State</span>
              <span className={`value status ${status.status === "WORKING" ? "blink" : ""}`}>
                {status.status || "OFFLINE"}
              </span>
            </div>
          </div>
        </header>

        {/* TOP ROW */}
        <div className="main-grid">
          
          {/* CONTROLS */}
          <div className="panel controls">
            <h2><Activity size={18} color="var(--neon-blue)" /> COMMAND OVERRIDE</h2>
            
            <div className="input-group">
              <label>MISSION PARAMETERS</label>
              <textarea 
                value={goal} 
                onChange={(e) => setGoal(e.target.value)} 
                placeholder="> Input directive protocol..."
              />
              <div className="btn-row">
                <button className="btn-primary" onClick={runAgent} disabled={status.status === "WORKING"}>
                  <Play size={16} /> EXECUTE
                </button>
                <button className="btn-danger" onClick={abortAgent}>
                  <Ban size={16} /> KILL SWITCH
                </button>
              </div>
            </div>

            <div className="input-group">
              <label><Lock size={14} /> RESOURCE ALLOCATION LIMIT</label>
              <input 
                type="range" min="10" max="500" value={limit} 
                onChange={(e) => updateLimit(e.target.value)} 
              />
              <div className="range-val">{limit} MNEE</div>
            </div>
          </div>

          {/* TERMINAL - Container now handles its own scrolling */}
          <div className="panel terminal-panel">
            <h2><Terminal size={18} color="var(--neon-green)"/> NEURAL LOGS</h2>
            <div className="terminal-window" ref={terminalRef} style={{ overflowY: 'auto' }}>
              {status.logs && status.logs.length > 0 ? (
                status.logs.map((log, i) => (
                  <div key={i} className="log-line">
                    <span className="log-caret">{'>'}</span> {log}
                  </div>
                ))
              ) : (
                <div className="log-line" style={{color:'#555'}}>System quiet...</div>
              )}
            </div>
          </div>
        </div>

        {/* BOTTOM ROW */}
        <div className="main-grid">
          
          {/* CHART */}
          <div className="panel chart-panel">
            <h2><Cpu size={18} color="var(--neon-red)" /> COST ANALYSIS VECTOR</h2>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={status.history ? [...status.history].reverse() : []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                  <XAxis dataKey="time" stroke="#555" tick={{fontSize: 10}} interval="preserveStartEnd" />
                  <YAxis stroke="#555" tick={{fontSize: 10}} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#050505', border: '1px solid #333', color: '#fff' }} 
                    itemStyle={{ fontSize: '0.8rem' }}
                  />
                  <Line type="stepAfter" dataKey="cost" stroke="#00ff41" strokeWidth={2} dot={false} name="Cost" />
                  <Line type="monotone" dataKey="urgency" stroke="#ff0055" strokeWidth={1} dot={false} name="Risk" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* AUDIT LOG */}
          <div className="panel audit-panel">
            <h2><ShieldAlert size={18} color="#e0e0e0" /> IMMUTABLE LEDGER</h2>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>TIME</th>
                    <th>REASONING</th>
                    <th>RISK</th>
                    <th>COST</th>
                    <th>HASH</th>
                  </tr>
                </thead>
                <tbody>
                  {status.history && status.history.map((tx) => (
                    <tr key={tx.id}>
                      <td style={{color: '#666'}}>{tx.time}</td>
                      <td>{tx.reason}</td>
                      <td>
                        <span className={`tag ${tx.urgency > 80 ? "high" : ""}`}>
                          {tx.urgency > 80 ? "CRITICAL" : "NORMAL"}
                        </span>
                      </td>
                      <td style={{ color: tx.cost > 0 ? '#00ff41' : '#ff0055', fontWeight: 'bold' }}>
                        {tx.cost > 0 ? '+' : ''}{tx.cost}
                      </td>
                      <td className="hash">{tx.tx ? tx.tx.substring(0, 8) : '0x00'}...</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}