import { useState, useEffect, useRef } from 'react';
import { Terminal, Wallet, ArrowDownLeft, ArrowUpRight, DollarSign, Play, Activity, Cpu, Search } from 'lucide-react';
import './App.css';

function App() {
  const [logs, setLogs] = useState([]);
  const [goal, setGoal] = useState("");
  const [stats, setStats] = useState({
    balance: 0,
    spent: 0,
    revenue: 0,
    net_profit: 0,
    status: "IDLE",
    history: []
  });
  const [loading, setLoading] = useState(false);
  const logsEndRef = useRef(null);

  // 1. POLL LOGS
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/logs');
        const data = await res.json();
        if (Array.isArray(data)) setLogs(data);
      } catch (e) {
        console.error("Log Poll Error:", e);
      }
    };
    const interval = setInterval(fetchLogs, 1000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll logs
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  // 2. POLL STATS
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/status');
        const data = await res.json();
        setStats(data);
      } catch (e) {
        console.error("Stats Poll Error:", e);
      }
    };
    const interval = setInterval(fetchStats, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleRunAgent = async () => {
    if (!goal) return;
    setLoading(true);
    try {
      await fetch('http://127.0.0.1:8000/run-agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal })
      });
      setGoal("");
    } catch (e) {
      alert("Backend Offline");
    }
    setLoading(false);
  };

  const formatTime = (ts) => {
    if (!ts) return new Date().toLocaleTimeString();
    const date = new Date(ts < 10000000000 ? ts * 1000 : ts);
    return date.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' });
  };

  // --- UI COMPONENTS ---

  return (
    <div className="min-h-screen bg-black text-zinc-100 font-sans selection:bg-blue-500/30 overflow-hidden relative">
      
      {/* === BACKGROUND IMAGE LAYER === */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        {/* Placeholder Tech Image - Replace 'src' with your own URL if desired */}
        <img 
            src="/bg.jpg"
            alt="Background" 
            className="w-full h-full object-cover opacity-55"
        />
        {/* Dark Gradient Overlay to ensure text readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-zinc-950/90 via-zinc-950/80 to-black/90"></div>
      </div>

      <div className="max-w-[1600px] mx-auto p-4 lg:p-6 relative z-10 h-screen flex flex-col">
        
        {/* === HEADER === */}
        <header className="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-900 rounded-lg flex items-center justify-center shadow-lg shadow-blue-900/20 border border-blue-500/30">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                PRAETOR <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">PRIME</span>
              </h1>
              <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-500 font-medium">Autonomous Asset Neural Net</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
             <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border backdrop-blur-sm transition-all duration-500 ${
                stats.status === "WORKING" 
                ? "bg-amber-500/10 border-amber-500/20 text-amber-400" 
                : "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
              }`}>
                <Activity className={`w-3.5 h-3.5 ${stats.status === "WORKING" ? "animate-spin" : ""}`} />
                <span className="text-xs font-bold tracking-wide">{stats.status}</span>
             </div>
          </div>
        </header>

        {/* === MAIN LAYOUT === */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 min-h-0">

          {/* === LEFT: CONSOLE & INPUT === */}
          <div className="lg:col-span-8 flex flex-col gap-6 min-h-0">
            
            {/* INPUT SECTION */}
            <div className="bg-zinc-900/50 border border-white/5 rounded-2xl p-1 shadow-xl backdrop-blur-md">
              <div className="relative flex items-center">
                <div className="absolute left-4 text-blue-500">
                  <Terminal className="w-5 h-5" />
                </div>
                <input
                  type="text"
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleRunAgent()}
                  placeholder="Input strategic directive..."
                  className="w-full bg-transparent border-none text-white placeholder-zinc-600 pl-12 pr-32 py-4 focus:ring-0 font-mono text-sm"
                />
                <button
                  onClick={handleRunAgent}
                  disabled={stats.status === "WORKING" || !goal}
                  className="absolute right-2 bg-blue-600 hover:bg-blue-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all shadow-lg shadow-blue-900/20"
                >
                  {loading ? <Activity className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3 fill-current" />}
                  EXECUTE
                </button>
              </div>
            </div>

            {/* LOGS & TABLE SPLIT */}
            <div className="flex-1 grid grid-rows-2 gap-6 min-h-0">
              
              {/* TERMINAL LOGS */}
              <div className="bg-black/40 border border-white/10 rounded-2xl overflow-hidden flex flex-col shadow-inner relative group backdrop-blur-sm">
                <div className="px-4 py-2 bg-white/5 border-b border-white/5 flex justify-between items-center backdrop-blur-sm">
                  <span className="text-[10px] font-mono text-zinc-400 uppercase flex items-center gap-2">
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
                    System Stream
                  </span>
                </div>
                
                <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-xs custom-scrollbar">
                  {logs.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-zinc-700 space-y-2">
                      <Terminal className="w-8 h-8 opacity-20" />
                      <p>Awaiting Neural Input...</p>
                    </div>
                  )}
                  {logs.map((log, i) => (
                    <div key={i} className="flex gap-3 group/log animate-in fade-in slide-in-from-left-2 duration-300">
                      <span className="text-zinc-600 shrink-0 select-none">{formatTime(log.timestamp)}</span>
                      <div className="flex gap-2">
                        <span className={`shrink-0 px-1.5 py-0.5 rounded-[4px] text-[9px] font-bold border ${
                          log.tag === "ERROR" || log.tag === "ABORT" ? "bg-red-500/10 text-red-400 border-red-500/20" :
                          log.tag === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                          log.tag === "COMMAND" ? "bg-purple-500/10 text-purple-400 border-purple-500/20" :
                          "bg-blue-500/10 text-blue-400 border-blue-500/20"
                        }`}>
                          {log.tag}
                        </span>
                        <span className={`text-zinc-300 ${log.tag === "ERROR" ? "text-red-300" : ""}`}>
                          {log.description}
                        </span>
                      </div>
                    </div>
                  ))}
                  <div ref={logsEndRef} />
                </div>
              </div>

              {/* LEDGER */}
              <div className="bg-black/40 border border-white/10 rounded-2xl overflow-hidden flex flex-col backdrop-blur-sm">
                <div className="px-5 py-3 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
                  <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-wider">Transaction Ledger</h3>
                  <div className="p-1 bg-zinc-800 rounded text-zinc-500"><Search className="w-3 h-3" /></div>
                </div>
                <div className="flex-1 overflow-auto custom-scrollbar">
                  <table className="w-full text-left text-xs">
                    <thead className="text-zinc-500 font-medium bg-white/[0.02] sticky top-0 backdrop-blur-sm z-10">
                      <tr>
                        <th className="px-5 py-3 font-normal">Timestamp</th>
                        <th className="px-5 py-3 font-normal">Operation</th>
                        <th className="px-5 py-3 font-normal text-right">Cost</th>
                        <th className="px-5 py-3 font-normal text-right">Rev</th>
                        <th className="px-5 py-3 font-normal text-right">Net</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      {stats.history.length === 0 ? (
                         <tr><td colSpan="5" className="text-center py-10 text-zinc-700 italic">No ledger activity recorded.</td></tr>
                      ) : (
                        stats.history.map((tx) => (
                          <tr key={tx.id} className="hover:bg-white/[0.03] transition-colors group">
                            <td className="px-5 py-2.5 font-mono text-zinc-500">{tx.time}</td>
                            <td className="px-5 py-2.5 text-zinc-300 font-medium group-hover:text-white">{tx.type}</td>
                            <td className="px-5 py-2.5 text-right font-mono text-red-400/80">{tx.cost > 0 ? '-' : ''}{tx.cost.toFixed(2)}</td>
                            <td className="px-5 py-2.5 text-right font-mono text-blue-400/80">{tx.revenue > 0 ? '+' : ''}{tx.revenue.toFixed(2)}</td>
                            <td className={`px-5 py-2.5 text-right font-mono font-bold ${tx.profit >= 0 ? "text-emerald-400" : "text-red-500"}`}>
                              {tx.profit > 0 ? '+' : ''}{tx.profit.toFixed(2)}
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          </div>

          {/* === RIGHT: FINANCIALS === */}
          <div className="lg:col-span-4 flex flex-col gap-4">
            
            {/* BALANCE CARD */}
            <div className="bg-gradient-to-br from-zinc-900/80 to-black/80 border border-white/10 p-6 rounded-2xl relative overflow-hidden group backdrop-blur-md">
              <div className="absolute -right-10 -top-10 w-40 h-40 bg-blue-600/10 rounded-full blur-3xl group-hover:bg-blue-600/20 transition-all"></div>
              
              <div className="flex justify-between items-start mb-6 relative z-10">
                <div className="p-2 bg-zinc-800/50 rounded-lg border border-white/5">
                  <Wallet className="w-5 h-5 text-zinc-400" />
                </div>
                <span className="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Treasury</span>
              </div>
              
              <div className="relative z-10">
                <div className="text-4xl font-mono font-bold text-white tracking-tighter">
                  {stats.balance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
                <div className="text-xs text-zinc-500 mt-1 flex items-center gap-1">
                  Available Liquidity <span className="text-zinc-600">|</span> USD
                </div>
              </div>
            </div>

            {/* METRICS GRID */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-zinc-900/40 border border-white/5 p-4 rounded-xl backdrop-blur-sm hover:border-red-500/30 transition-colors">
                <div className="flex items-center gap-2 mb-3">
                  <div className="p-1.5 bg-red-500/10 rounded text-red-500">
                    <ArrowDownLeft className="w-3.5 h-3.5" />
                  </div>
                  <span className="text-[10px] uppercase text-zinc-500 font-bold">Spent</span>
                </div>
                <p className="text-xl font-mono text-zinc-200">{stats.spent.toLocaleString()}</p>
              </div>

              <div className="bg-zinc-900/40 border border-white/5 p-4 rounded-xl backdrop-blur-sm hover:border-blue-500/30 transition-colors">
                 <div className="flex items-center gap-2 mb-3">
                  <div className="p-1.5 bg-blue-500/10 rounded text-blue-500">
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </div>
                  <span className="text-[10px] uppercase text-zinc-500 font-bold">Revenue</span>
                </div>
                <p className="text-xl font-mono text-zinc-200">{stats.revenue.toLocaleString()}</p>
              </div>
            </div>

            {/* NET PROFIT HERO */}
            <div className="flex-1 min-h-[180px] bg-gradient-to-b from-zinc-900/80 to-black/80 border border-white/10 rounded-2xl p-6 relative flex flex-col justify-end overflow-hidden backdrop-blur-md">
               {/* Background Chart Effect (Abstract) */}
               <div className="absolute inset-0 opacity-20">
                  <svg className="w-full h-full" preserveAspectRatio="none">
                    <path d="M0,100 Q50,50 100,80 T200,40 T300,90" fill="none" stroke={stats.net_profit >= 0 ? "#10b981" : "#ef4444"} strokeWidth="2" vectorEffect="non-scaling-stroke" />
                  </svg>
               </div>
               
               <div className="relative z-10">
                 <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-zinc-500 font-bold uppercase tracking-widest">Total Yield</span>
                    <DollarSign className={`w-5 h-5 ${stats.net_profit >= 0 ? "text-emerald-500" : "text-red-500"}`} />
                 </div>
                 <div className={`text-4xl font-mono font-bold tracking-tight ${stats.net_profit >= 0 ? "text-emerald-400 drop-shadow-[0_0_10px_rgba(52,211,153,0.3)]" : "text-red-400 drop-shadow-[0_0_10px_rgba(248,113,113,0.3)]"}`}>
                    {stats.net_profit >= 0 ? "+" : ""}{stats.net_profit.toLocaleString()}
                 </div>
                 <div className="mt-3 flex items-center gap-2">
                    <div className={`h-1 flex-1 rounded-full ${stats.net_profit >= 0 ? "bg-emerald-900/50" : "bg-red-900/50"}`}>
                       <div className={`h-full rounded-full w-[70%] ${stats.net_profit >= 0 ? "bg-emerald-500" : "bg-red-500"}`}></div>
                    </div>
                    <span className="text-[10px] text-zinc-500">ROI IMPRESSION</span>
                 </div>
               </div>
            </div>

          </div>
        </div>
      </div>

      {/* Custom Scrollbar Styles embedded for this component */}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 2px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }
      `}</style>
    </div>
  );
}

export default App;