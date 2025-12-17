import React, { useState } from 'react'; // <--- This was likely missing
import axios from 'axios';
import { motion } from 'framer-motion';
import { Play, Cpu, Zap, Activity } from 'lucide-react';
import AgentTerminal from './components/AgentTerminal';
import CodeDisplay from './components/CodeDisplay';

function App() {
  const [task, setTask] = useState("");
  const [status, setStatus] = useState("IDLE"); // IDLE, WORKING, COMPLETED, FAILED
  const [logs, setLogs] = useState([]);
  const [code, setCode] = useState("");
  const [attempts, setAttempts] = useState(0);

  const runAgent = async () => {
    if (!task.trim()) return;
    
    setStatus("WORKING");
    setLogs(["Initializing CodeOPS ULTRA Protocol...", "Connecting to Secure Docker Sandbox..."]);
    setCode("");
    setAttempts(0);

    try {
      // Hit the FastAPI backend
      const response = await axios.post("http://127.0.0.1:8000/api/solve", {
        task: task
      });

      const data = response.data;
      setLogs(prev => [...prev, ...data.logs]);
      setCode(data.code);
      setAttempts(data.attempts);
      setStatus("COMPLETED");
    } catch (error) {
      console.error(error);
      setLogs(prev => [...prev, "CRITICAL ERROR: Connection to Agent Brain Failed."]);
      setStatus("FAILED");
    }
  };

  return (
    <div className="min-h-screen bg-ultra-bg text-gray-100 p-4 md:p-8 flex flex-col gap-6 selection:bg-ultra-primary/30">
      
      {/* 1. Header / Navbar */}
      <header className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 bg-ultra-primary blur-lg opacity-50 rounded-full"></div>
            <div className="relative bg-gradient-to-br from-ultra-primary to-purple-600 p-2 rounded-lg">
              <Cpu size={28} className="text-white" />
            </div>
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
              CodeOps <span className="text-ultra-primary">ULTRA</span>
            </h1>
            <p className="text-xs text-gray-500 font-mono tracking-widest">AUTONOMOUS ENGINEERING AGENT v1.0</p>
          </div>
        </div>

        {/* Status Badge */}
        <div className={`px-4 py-1.5 rounded-full border flex items-center gap-2 font-mono text-xs font-bold transition-all duration-500 ${
          status === "WORKING" ? "bg-blue-500/10 border-blue-500/50 text-blue-400 animate-pulse" :
          status === "COMPLETED" ? "bg-green-500/10 border-green-500/50 text-green-400" :
          "bg-gray-800 border-gray-700 text-gray-400"
        }`}>
          <Activity size={14} />
          {status === "WORKING" ? "SYSTEM ACTIVE: PROCESSING" : 
           status === "COMPLETED" ? "MISSION SUCCESS" : "SYSTEM STANDBY"}
        </div>
      </header>

      {/* 2. Input Section */}
      <motion.div 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="glass-panel p-1 rounded-2xl flex items-center gap-2"
      >
        <input
          type="text"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && runAgent()}
          placeholder="Enter engineering task (e.g., 'Write a Python script to scan ports 80-100 on localhost')"
          className="w-full bg-transparent border-none outline-none text-white px-4 py-3 font-medium placeholder-gray-600"
          disabled={status === "WORKING"}
        />
        <button
          onClick={runAgent}
          disabled={status === "WORKING"}
          className={`px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all ${
            status === "WORKING" 
              ? "bg-gray-700 text-gray-500 cursor-not-allowed"
              : "bg-gradient-to-r from-ultra-primary to-purple-600 hover:scale-105 shadow-lg shadow-ultra-primary/25"
          }`}
        >
          {status === "WORKING" ? (
            <Zap size={18} className="animate-spin" />
          ) : (
            <Play size={18} fill="currentColor" />
          )}
          DEPLOY
        </button>
      </motion.div>

      {/* 3. Main Workspace (Split View) */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-[500px]">
        {/* Left: Terminal */}
        <motion.div 
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="h-full"
        >
          <AgentTerminal logs={logs} />
        </motion.div>

        {/* Right: Code Editor */}
        <motion.div 
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="h-full"
        >
          <CodeDisplay code={code} />
        </motion.div>
      </div>

      {/* 4. Footer / Stats */}
      {attempts > 0 && (
        <div className="flex justify-center">
          <div className="bg-white/5 border border-white/10 rounded-full px-6 py-2 flex items-center gap-4 text-xs font-mono text-gray-400">
            <span>SELF_CORRECTION_CYCLES: <span className="text-white font-bold">{attempts - 1}</span></span>
            <span>|</span>
            <span>SANDBOX_INTEGRITY: <span className="text-green-400">VERIFIED</span></span>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;