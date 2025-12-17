import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, CheckCircle2, XCircle, Loader2, ArrowRight } from 'lucide-react';

const AgentTerminal = ({ logs }) => {
  const scrollRef = useRef(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="glass-panel rounded-xl h-full flex flex-col overflow-hidden border-l-4 border-l-ultra-primary/50">
      {/* Terminal Header */}
      <div className="bg-ultra-card/50 p-3 border-b border-ultra-border flex items-center justify-between">
        <div className="flex items-center gap-2 text-ultra-accent">
          <Terminal size={18} />
          <span className="font-mono text-sm font-bold tracking-wider">AGENT_LIVE_EXECUTION_LOGS</span>
        </div>
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
          <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
        </div>
      </div>

      {/* Logs Area */}
      <div 
        ref={scrollRef}
        className="flex-1 p-4 overflow-y-auto font-mono text-sm space-y-3"
      >
        <AnimatePresence>
          {logs.length === 0 && (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 0.5 }}
              className="text-gray-500 italic text-center mt-10"
            >
              Waiting for mission parameters...
            </motion.div>
          )}
          
          {logs.map((log, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className={`flex items-start gap-3 p-2 rounded-lg ${
                log.includes("Error") ? "bg-red-900/10 text-red-300 border border-red-900/30" : 
                log.includes("Success") ? "bg-green-900/10 text-green-300 border border-green-900/30" :
                "text-gray-300"
              }`}
            >
              <div className="mt-1 shrink-0">
                {log.includes("Error") ? <XCircle size={16} className="text-red-500" /> :
                 log.includes("Success") ? <CheckCircle2 size={16} className="text-green-500" /> :
                 log.includes("Generating") ? <Loader2 size={16} className="animate-spin text-ultra-accent" /> :
                 <ArrowRight size={16} className="text-gray-500" />}
              </div>
              <span className="break-words leading-relaxed">{log}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default AgentTerminal;