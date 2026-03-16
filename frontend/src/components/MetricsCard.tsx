import React from 'react';
import { motion } from 'framer-motion';
import { Activity, GitMerge, Cpu, ShieldCheck, ShieldX, Zap } from 'lucide-react';
import type { CircuitMetrics } from '@/types/chat';

interface MetricsCardProps {
  metrics: CircuitMetrics;
}

export const MetricsCard: React.FC<MetricsCardProps> = ({ metrics }) => {
  const validationPassed = metrics.validation === 'Passed';

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1, duration: 0.3 }}
      className="rounded-b-xl border border-t-0 border-border/50 bg-surface/50 backdrop-blur-md p-3"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-muted-foreground" />
          <span className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest">
            Circuit Metrics
          </span>
        </div>
        <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono font-semibold ${
          validationPassed
            ? 'bg-success/10 text-success border border-success/20'
            : metrics.validation === 'Failed'
            ? 'bg-destructive/10 text-destructive border border-destructive/20'
            : 'bg-muted/50 text-muted-foreground border border-border'
        }`}>
          {validationPassed
            ? <ShieldCheck className="w-3 h-3" />
            : <ShieldX className="w-3 h-3" />
          }
          Validation {metrics.validation}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2">
        {[
          { label: 'Depth', value: metrics.depth, icon: GitMerge, color: 'text-accent' },
          { label: 'Gates', value: metrics.gates, icon: Cpu, color: 'text-primary' },
          { label: 'Qubits', value: metrics.qubits, icon: Zap, color: 'text-success' },
        ].map(({ label, value, icon: Icon, color }) => (
          <div
            key={label}
            className="flex flex-col items-center gap-1 px-3 py-2.5 rounded-lg bg-background/60 border border-border/50"
          >
            <Icon className={`w-3 h-3 ${color}`} />
            <span className={`text-lg font-mono font-bold tracking-tighter ${color}`}>
              {value}
            </span>
            <span className="text-[10px] text-muted-foreground uppercase tracking-wider">
              {label}
            </span>
          </div>
        ))}
      </div>

      {(metrics.simulator || metrics.optimizationNote) && (
        <div className="mt-2.5 pt-2.5 border-t border-border/30 flex flex-wrap gap-2">
          {metrics.simulator && (
            <span className="flex items-center gap-1 text-[10px] font-mono text-muted-foreground px-2 py-1 rounded-md bg-muted/30">
              <Zap className="w-2.5 h-2.5" />
              {metrics.simulator}
            </span>
          )}
          {metrics.optimizationNote && (
            <span className="text-[10px] text-success font-mono px-2 py-1 rounded-md bg-success/5 border border-success/10">
              ↓ {metrics.optimizationNote}
            </span>
          )}
        </div>
      )}
    </motion.div>
  );
};
