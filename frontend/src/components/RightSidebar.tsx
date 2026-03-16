import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Bot, Cpu, ShieldCheck, GraduationCap, Lock } from 'lucide-react';
import type { AgentConfig } from '@/types/chat';

interface RightSidebarProps {
  open: boolean;
  onClose: () => void;
  config: AgentConfig;
  onConfigChange: (config: AgentConfig) => void;
}

const DEPTH_OPTIONS: AgentConfig['educationalDepth'][] = ['Low', 'Intermediate', 'High', 'Very High'];

interface AgentToggleProps {
  icon: React.ReactNode;
  label: string;
  description: string;
  enabled: boolean;
  locked?: boolean;
  color: string;
  onChange: (v: boolean) => void;
}

const AgentToggle: React.FC<AgentToggleProps> = ({
  icon, label, description, enabled, locked, color, onChange
}) => (
  <div className={`p-3 rounded-xl border transition-all ${
    enabled
      ? `border-${color}/30 bg-${color}/5`
      : 'border-border bg-muted/30'
  }`}>
    <div className="flex items-start justify-between gap-3">
      <div className="flex items-start gap-2.5 flex-1 min-w-0">
        <div className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
          enabled ? `bg-${color}/15 text-${color}` : 'bg-muted text-muted-foreground'
        }`}>
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-semibold text-foreground">{label}</span>
            {locked && <Lock className="w-2.5 h-2.5 text-muted-foreground" />}
          </div>
          <p className="text-[11px] text-muted-foreground mt-0.5 leading-snug">{description}</p>
        </div>
      </div>
      {/* Toggle */}
      <button
        onClick={() => !locked && onChange(!enabled)}
        disabled={locked}
        className={`relative w-9 h-5 rounded-full transition-all shrink-0 mt-0.5 ${
          locked ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        } ${enabled ? 'bg-gradient-to-r from-purple-600 to-blue-500' : 'bg-secondary'}`}
      >
        <motion.div
          layout
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          className={`absolute top-0.5 w-4 h-4 rounded-full bg-white shadow-sm ${
            enabled ? 'left-[calc(100%-1.125rem)]' : 'left-0.5'
          }`}
        />
      </button>
    </div>
    {enabled && (
      <motion.div
        initial={{ opacity: 0, height: 0 }}
        animate={{ opacity: 1, height: 'auto' }}
        exit={{ opacity: 0, height: 0 }}
        className="mt-2 pt-2 border-t border-border/50"
      >
        <div className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse-dot" />
          <span className="text-[10px] font-mono text-success">Active</span>
        </div>
      </motion.div>
    )}
  </div>
);

export const RightSidebar: React.FC<RightSidebarProps> = ({
  open, onClose, config, onConfigChange
}) => {
  return (
    <AnimatePresence>
      {open && (
        <motion.aside
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 300, opacity: 1 }}
          exit={{ width: 0, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          className="flex flex-col border-l border-border/50 bg-sidebar overflow-hidden shrink-0"
        >
          <div className="flex items-center justify-between px-4 py-3 border-b border-border/50">
            <span className="text-sm font-semibold">System Settings</span>
            <button
              onClick={onClose}
              className="w-6 h-6 flex items-center justify-center rounded-md text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin">
            {/* Agent Configuration */}
            <section>
              <h3 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest mb-3">
                Agent Pipeline
              </h3>
              <div className="space-y-2">
                <AgentToggle
                  icon={<Bot className="w-3.5 h-3.5" />}
                  label="Designer Agent"
                  description="Fetches RAG context and designs initial circuit layout."
                  enabled={config.designerEnabled}
                  locked={true}
                  color="primary"
                  onChange={(v) => onConfigChange({ ...config, designerEnabled: v })}
                />
                <AgentToggle
                  icon={<Cpu className="w-3.5 h-3.5" />}
                  label="Optimizer Agent"
                  description="Reduces gate depth and optimizes qubit allocation."
                  enabled={config.optimizerEnabled}
                  color="accent"
                  onChange={(v) => onConfigChange({ ...config, optimizerEnabled: v })}
                />
                <AgentToggle
                  icon={<ShieldCheck className="w-3.5 h-3.5" />}
                  label="Validator Agent"
                  description="Executes dry-run via Braket SDK to verify circuit validity."
                  enabled={config.validatorEnabled}
                  locked={true}
                  color="success"
                  onChange={(v) => onConfigChange({ ...config, validatorEnabled: v })}
                />
              </div>
            </section>

            {/* Educational Depth */}
            <section>
              <h3 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest mb-3 flex items-center gap-2">
                <GraduationCap className="w-3.5 h-3.5" />
                Educational Depth
              </h3>
              <div className="grid grid-cols-2 gap-1.5">
                {DEPTH_OPTIONS.map((depth) => (
                  <button
                    key={depth}
                    onClick={() => onConfigChange({ ...config, educationalDepth: depth })}
                    className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                      config.educationalDepth === depth
                        ? 'gradient-primary text-white shadow-sm'
                        : 'bg-muted/50 text-muted-foreground hover:bg-secondary hover:text-foreground border border-border'
                    }`}
                  >
                    {depth}
                  </button>
                ))}
              </div>
              <p className="text-[11px] text-muted-foreground mt-2 leading-snug">
                Controls explanation verbosity and quantum concept detail in responses.
              </p>
              <div className="flex items-center gap-1.5 mt-2 px-2 py-1.5 rounded-lg text-[10px] font-mono bg-primary/5 text-primary border border-primary/10">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse-dot" />
                {`Educational Agent · ${config.educationalDepth} detail`}
              </div>
            </section>

            {/* Model Info */}
            <section>
              <h3 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest mb-3">
                Model Configuration
              </h3>
              <div className="space-y-2">
                {[
                  { label: 'Designer LLM', value: 'Amazon Nova Pro' },
                  { label: 'Validator LLM', value: 'Amazon Nova Premier' },
                  { label: 'Optimizer LLM', value: 'Amazon Nova Pro' },
                  { label: 'Educational LLM', value: 'Amazon Nova 2 Lite' },
                  { label: 'Embeddings', value: 'BAAI/bge-base-en-v1.5' },
                  { label: 'Simulator', value: 'Amazon Braket Local' },
                  { label: 'RAG Chunks', value: 'top-k=5' },
                ].map(({ label, value }) => (
                  <div key={label} className="flex justify-between items-center py-1.5 border-b border-border/30">
                    <span className="text-[11px] text-muted-foreground">{label}</span>
                    <span className="text-[11px] font-mono text-foreground bg-secondary px-2 py-0.5 rounded-md">{value}</span>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
};
