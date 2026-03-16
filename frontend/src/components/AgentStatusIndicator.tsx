import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Cpu, ShieldCheck, GraduationCap, ShieldAlert, Check, Loader2, SkipForward } from 'lucide-react';
import type { AgentStatus } from '@/types/chat';

interface AgentStatusIndicatorProps {
  statuses: AgentStatus[];
}

const agentMeta: Record<string, { icon: React.FC<{ className?: string }>; label: string; color: string; bg: string; border: string }> = {
  designer: {
    icon: Bot,
    label: 'Designer Agent',
    color: 'text-primary',
    bg: 'bg-primary/10',
    border: 'border-primary/20',
  },
  optimizer: {
    icon: Cpu,
    label: 'Optimizer Agent',
    color: 'text-accent',
    bg: 'bg-accent/10',
    border: 'border-accent/20',
  },
  validator: {
    icon: ShieldCheck,
    label: 'Validator Agent',
    color: 'text-success',
    bg: 'bg-success/10',
    border: 'border-success/20',
  },
  final_validator: {
    icon: ShieldAlert,
    label: 'Final Validator',
    color: 'text-success',
    bg: 'bg-success/10',
    border: 'border-success/20',
  },
  educational: {
    icon: GraduationCap,
    label: 'Educational Agent',
    color: 'text-primary',
    bg: 'bg-primary/10',
    border: 'border-primary/20',
  },
};

const stepVariants = {
  initial: { opacity: 0, x: -8 },
  animate: { opacity: 1, x: 0 },
};

export const AgentStatusIndicator: React.FC<AgentStatusIndicatorProps> = ({ statuses }) => {
  return (
    <div className="flex flex-col gap-2 my-2">
      {statuses.map((step, i) => {
        const meta = agentMeta[step.id] ?? agentMeta.designer;
        const Icon = meta.icon;
        const isRunning = step.status === 'running';
        const isDone = step.status === 'done';
        const isSkipped = step.status === 'skipped';

        return (
          <motion.div
            key={step.id}
            variants={stepVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: i * 0.12, ease: [0.25, 0.1, 0.25, 1], duration: 0.3 }}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all ${
              isRunning
                ? `${meta.bg} ${meta.border}`
                : isDone
                ? 'bg-success/5 border-success/20'
                : isSkipped
                ? 'bg-muted/30 border-border/50'
                : 'bg-muted/20 border-border/30'
            }`}
          >
            {/* Icon */}
            <div className={`w-6 h-6 rounded-md flex items-center justify-center shrink-0 ${meta.bg}`}>
              <Icon className={`w-3.5 h-3.5 ${meta.color}`} />
            </div>

            {/* Text */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-foreground">{meta.label}</span>
                {isRunning && (
                  <span className={`text-[10px] font-mono ${meta.color} px-1.5 py-0.5 rounded-full ${meta.bg}`}>
                    running
                  </span>
                )}
              </div>
              {step.detail && (
                <p className="text-[11px] text-muted-foreground mt-0.5 truncate font-mono">
                  {step.detail}
                </p>
              )}
            </div>

            {/* Status indicator */}
            <div className="shrink-0">
              {isRunning && (
                <Loader2 className={`w-4 h-4 ${meta.color} animate-spin`} />
              )}
              {isDone && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', stiffness: 400, damping: 20 }}
                  className="w-4 h-4 rounded-full bg-success flex items-center justify-center"
                >
                  <Check className="w-2.5 h-2.5 text-white" />
                </motion.div>
              )}
              {isSkipped && (
                <SkipForward className="w-4 h-4 text-muted-foreground" />
              )}
              {step.status === 'idle' && (
                <div className="w-4 h-4 rounded-full border-2 border-border" />
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};
