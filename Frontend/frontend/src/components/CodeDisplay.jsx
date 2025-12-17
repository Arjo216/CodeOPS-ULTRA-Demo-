import React from 'react';
import Editor from '@monaco-editor/react';
import { Code2, Copy, Check } from 'lucide-react';
import { useState } from 'react';

const CodeDisplay = ({ code }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-panel rounded-xl h-full flex flex-col overflow-hidden border-r-4 border-r-ultra-accent/50">
      {/* Editor Header */}
      <div className="bg-ultra-card/50 p-3 border-b border-ultra-border flex items-center justify-between">
        <div className="flex items-center gap-2 text-ultra-primary">
          <Code2 size={18} />
          <span className="font-mono text-sm font-bold tracking-wider">VERIFIED_SOURCE_CODE.py</span>
        </div>
        <button 
          onClick={handleCopy}
          className="flex items-center gap-2 px-3 py-1 rounded bg-white/5 hover:bg-white/10 transition-colors text-xs text-gray-400 hover:text-white"
        >
          {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
          {copied ? "COPIED" : "COPY CODE"}
        </button>
      </div>

      {/* Monaco Editor Instance */}
      <div className="flex-1 bg-[#1e1e1e]">
        <Editor
          height="100%"
          defaultLanguage="python"
          value={code || "# Waiting for agent output..."}
          theme="vs-dark"
          options={{
            readOnly: true,
            minimap: { enabled: false },
            fontSize: 14,
            padding: { top: 16 },
            fontFamily: "Fira Code",
            scrollBeyondLastLine: false,
            renderLineHighlight: "none",
          }}
        />
      </div>
    </div>
  );
};

export default CodeDisplay;