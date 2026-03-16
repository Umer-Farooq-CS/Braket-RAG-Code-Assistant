import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, MessageSquare, Clock, ChevronLeft, ChevronRight, Atom } from 'lucide-react';
import type { ChatSession } from '@/types/chat';

interface LeftSidebarProps {
  sessions: ChatSession[];
  activeSessionId: string | null;
  onNewSession: () => void;
  onSelectSession: (id: string) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const LeftSidebar: React.FC<LeftSidebarProps> = ({
  sessions,
  activeSessionId,
  onNewSession,
  onSelectSession,
  collapsed,
  onToggleCollapse,
}) => {
  return (
    <motion.aside
      animate={{ width: collapsed ? 56 : 260 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      className="relative flex flex-col border-r border-border/50 bg-sidebar overflow-hidden shrink-0"
    >
      {/* Header */}
      <div className={`flex items-center p-3 border-b border-border/50 gap-2 ${collapsed ? 'justify-center' : 'justify-between'}`}>
        {!collapsed && (
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-xs font-semibold text-muted-foreground uppercase tracking-widest"
          >
            History
          </motion.span>
        )}
        <button
          onClick={onToggleCollapse}
          className="w-7 h-7 flex items-center justify-center rounded-md text-muted-foreground hover:text-foreground hover:bg-sidebar-accent transition-colors"
        >
          {collapsed ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
        </button>
      </div>

      {/* New Session Button */}
      <div className="p-2">
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={onNewSession}
          className={`w-full flex items-center gap-2 rounded-xl gradient-primary text-white font-medium transition-all hover:opacity-90 active:scale-[0.97] ${
            collapsed ? 'justify-center p-2.5' : 'px-3 py-2.5 text-sm'
          }`}
        >
          <Plus className="w-4 h-4 shrink-0" />
          <AnimatePresence>
            {!collapsed && (
              <motion.span
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: 'auto' }}
                exit={{ opacity: 0, width: 0 }}
                className="overflow-hidden whitespace-nowrap"
              >
                New Circuit
              </motion.span>
            )}
          </AnimatePresence>
        </motion.button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1 scrollbar-thin">
        <AnimatePresence>
          {sessions.length === 0 && !collapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center justify-center gap-3 py-12 px-4 text-center"
            >
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                <Atom className="w-5 h-5 text-primary" />
              </div>
              <p className="text-xs text-muted-foreground">
                Start a new circuit to begin
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {sessions.map((session, i) => (
          <motion.button
            key={session.id}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            onClick={() => onSelectSession(session.id)}
            className={`w-full flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-left transition-colors group ${
              activeSessionId === session.id
                ? 'bg-primary/10 text-primary'
                : 'hover:bg-sidebar-accent text-sidebar-foreground'
            }`}
          >
            <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${
              activeSessionId === session.id ? 'text-primary' : 'text-muted-foreground'
            }`} />
            <AnimatePresence>
              {!collapsed && (
                <motion.div
                  initial={{ opacity: 0, width: 0 }}
                  animate={{ opacity: 1, width: 'auto' }}
                  exit={{ opacity: 0, width: 0 }}
                  className="flex-1 overflow-hidden min-w-0"
                >
                  <p className="text-xs font-medium truncate">{session.title}</p>
                  <div className="flex items-center gap-1 mt-0.5">
                    <Clock className="w-2.5 h-2.5 text-muted-foreground" />
                    <span className="text-[10px] text-muted-foreground">
                      {session.createdAt.toLocaleDateString()}
                    </span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.button>
        ))}
      </div>

      {/* Footer */}
      {!collapsed && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="p-3 border-t border-border/50"
        >
          <div className="flex items-center gap-2 px-2.5 py-2 rounded-lg bg-primary/5 border border-primary/10">
            <div className="w-2 h-2 rounded-full bg-success animate-pulse-dot" />
            <span className="text-[11px] text-muted-foreground font-mono">Braket SDK v1.88+</span>
          </div>
        </motion.div>
      )}
    </motion.aside>
  );
};
