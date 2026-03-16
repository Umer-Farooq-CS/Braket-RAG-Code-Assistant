import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Check, Copy, Terminal } from 'lucide-react';
import type { CodeBlock as CodeBlockType } from '@/types/chat';

interface CodeBlockProps {
  block: CodeBlockType;
  isPulsing?: boolean;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({ block, isPulsing }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(block.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`relative rounded-xl overflow-hidden border border-border/50 ${isPulsing ? 'agent-pulse-border' : ''}`}
      style={{ position: 'relative', boxShadow: 'none' }}
    >
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[hsl(222,47%,6%)] border-b border-white/5">
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-muted-foreground" />
          <span className="text-xs font-mono text-muted-foreground">
            {block.filename || `circuit.py`}
          </span>
          <span className="px-1.5 py-0.5 rounded-md bg-primary/10 text-primary text-[10px] font-mono uppercase">
            {block.language}
          </span>
        </div>
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={handleCopy}
          className="flex items-center gap-1.5 text-[11px] font-mono text-muted-foreground hover:text-foreground transition-colors px-2 py-1 rounded-md hover:bg-white/5"
        >
          <motion.div key={copied ? 'check' : 'copy'} initial={{ scale: 0.8 }} animate={{ scale: 1 }}>
            {copied ? <Check className="w-3 h-3 text-success" /> : <Copy className="w-3 h-3" />}
          </motion.div>
          {copied ? 'Copied!' : 'Copy'}
        </motion.button>
      </div>

      {/* Code */}
      <div className="overflow-x-auto text-[13px] scrollbar-thin bg-background">
        <pre className="m-0 p-4 text-xs leading-relaxed font-mono whitespace-pre">
          <code>{block.code}</code>
        </pre>
      </div>
    </motion.div>
  );
};
