import React, { useRef, useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Square, Paperclip, AtSign, Atom } from 'lucide-react';
import type { ChatMessage, AgentConfig } from '@/types/chat';
import { MessageBubble } from './MessageBubble';

interface ChatWindowProps {
  messages: ChatMessage[];
  isGenerating: boolean;
  onSendMessage: (content: string) => void;
  onStopGeneration: () => void;
  config: AgentConfig;
}

const WELCOME_PROMPTS = [
  'Create a Bell state on Amazon Braket',
  'Implement a 3-qubit QFT circuit',
  'Build a QAOA circuit for MaxCut',
  'Generate a VQE ansatz with CNOT layers',
];

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isGenerating,
  onSendMessage,
  onStopGeneration,
  config,
}) => {
  const [input, setInput] = useState('');
  const [focused, setFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  const adjustHeight = useCallback(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
  }, []);

  useEffect(() => {
    adjustHeight();
  }, [input, adjustHeight]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || isGenerating) return;
    onSendMessage(trimmed);
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6 scrollbar-thin">
        {isEmpty ? (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center h-full text-center gap-8 py-16"
          >
            <div className="space-y-3">
              <div className="w-14 h-14 mx-auto rounded-2xl gradient-primary flex items-center justify-center shadow-lg">
                <Atom className="w-7 h-7 text-white" />
              </div>
              <h1 className="text-2xl font-bold gradient-text">
                Synthesize Braket Circuit
              </h1>
              <p className="text-sm text-muted-foreground max-w-md mx-auto leading-relaxed">
                Describe a quantum algorithm or circuit in natural language. The multi-agent pipeline
                will design, optimize, and validate your code using the Amazon Braket SDK.
              </p>
            </div>

            {/* Quick prompts */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full max-w-2xl">
              {WELCOME_PROMPTS.map((prompt) => (
                <motion.button
                  key={prompt}
                  whileHover={{ y: -1 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => onSendMessage(prompt)}
                  className="px-4 py-3 text-left rounded-xl border border-border bg-surface hover:border-primary/40 hover:bg-primary/5 transition-all card-shadow text-sm text-muted-foreground hover:text-foreground group"
                >
                  <div className="flex items-center gap-2">
                    <AtSign className="w-3.5 h-3.5 text-primary opacity-60 group-hover:opacity-100 shrink-0" />
                    <span className="font-mono text-xs">{prompt}</span>
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>
        ) : (
          <div className="max-w-3xl mx-auto w-full space-y-6">
            <AnimatePresence initial={false}>
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
            </AnimatePresence>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="shrink-0 px-4 pb-4">
        <div className="max-w-3xl mx-auto w-full">
          {/* Agent pills */}
          <div className="flex items-center gap-2 mb-2 px-1">
            {config.designerEnabled && (
              <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary/10 text-primary text-[10px] font-mono border border-primary/20">
                <span className="w-1 h-1 rounded-full bg-primary" />
                Designer
              </span>
            )}
            {config.optimizerEnabled && (
              <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-accent/10 text-accent text-[10px] font-mono border border-accent/20">
                <span className="w-1 h-1 rounded-full bg-accent" />
                Optimizer
              </span>
            )}
            {config.validatorEnabled && (
              <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-success/10 text-success text-[10px] font-mono border border-success/20">
                <span className="w-1 h-1 rounded-full bg-success" />
                Validator
              </span>
            )}
            <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary/10 text-primary text-[10px] font-mono border border-primary/20">
              <span className="w-1 h-1 rounded-full bg-primary" />
              {`Educational (${config.educationalDepth})`}
            </span>
            <span className="ml-auto text-[10px] text-muted-foreground font-mono">
              ⇧ Enter for newline
            </span>
          </div>

          {/* Input box */}
          <div
            className={`relative flex items-end gap-3 rounded-2xl border bg-surface transition-all px-4 py-3 ${
              focused || isGenerating
                ? 'border-primary/50 input-glow'
                : 'border-border hover:border-border/80'
            } ${config.validatorEnabled && isGenerating ? 'shadow-[0_0_15px_rgba(147,51,234,0.2)]' : ''}`}
          >
            <button className="text-muted-foreground hover:text-foreground transition-colors pb-0.5">
              <Paperclip className="w-4 h-4" />
            </button>

            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              placeholder="Describe a quantum circuit or algorithm..."
              rows={1}
              className="flex-1 bg-transparent resize-none outline-none text-sm text-foreground placeholder:text-muted-foreground leading-relaxed min-h-[24px] max-h-[200px] scrollbar-thin"
              disabled={isGenerating}
            />

            {/* Send / Stop button */}
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={isGenerating ? onStopGeneration : handleSend}
              disabled={!isGenerating && !input.trim()}
              className={`shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all ${
                isGenerating
                  ? 'bg-destructive/80 hover:bg-destructive text-white'
                  : input.trim()
                  ? 'gradient-primary text-white shadow-sm hover:opacity-90'
                  : 'bg-muted text-muted-foreground cursor-not-allowed'
              }`}
            >
              <motion.div
                key={isGenerating ? 'stop' : 'send'}
                initial={{ scale: 0.7, rotate: -15 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 400, damping: 20 }}
              >
                {isGenerating ? <Square className="w-3.5 h-3.5 fill-current" /> : <Send className="w-3.5 h-3.5" />}
              </motion.div>
            </motion.button>
          </div>

          <p className="text-[10px] text-muted-foreground text-center mt-2 font-mono">
            Braket RAG · Powered by Designer × Optimizer × Validator agents
          </p>
        </div>
      </div>
    </div>
  );
};
