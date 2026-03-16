import { motion } from 'framer-motion';
import { Sun, Moon, Settings, Atom, Zap } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import React from 'react';

interface HeaderProps {
  onSettingsToggle: () => void;
  settingsOpen: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onSettingsToggle, settingsOpen }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="h-14 flex items-center justify-between px-4 border-b border-border/50 glass-panel relative z-10 shrink-0">
      {/* Logo + Title */}
      <div className="flex items-center gap-2.5">
        <div className="relative">
          <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center">
            <Atom className="w-4 h-4 text-white" />
          </div>
          <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-success rounded-full border-2 border-background" />
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-semibold leading-none gradient-text">
            Braket RAG Assistant
          </span>
          <span className="text-[10px] text-muted-foreground leading-none mt-0.5 font-mono">
            Multi-Agent · AWS Braket SDK
          </span>
        </div>
      </div>

      {/* Status chip */}
      <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-success/10 border border-success/20">
        <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse-dot" />
        <span className="text-[11px] font-mono text-success">3 agents online</span>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-1">
        {/* Theme toggle */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={toggleTheme}
          className="w-8 h-8 flex items-center justify-center rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
          aria-label="Toggle theme"
        >
          <motion.div
            key={theme}
            initial={{ rotate: -30, opacity: 0 }}
            animate={{ rotate: 0, opacity: 1 }}
            transition={{ duration: 0.2 }}
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </motion.div>
        </motion.button>

        {/* Settings */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={onSettingsToggle}
          className={`w-8 h-8 flex items-center justify-center rounded-lg transition-colors ${
            settingsOpen
              ? 'text-primary bg-primary/10'
              : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
          }`}
          aria-label="System settings"
        >
          <Settings className="w-4 h-4" />
        </motion.button>

        {/* Braket badge */}
        <div className="hidden sm:flex items-center gap-1.5 ml-1 px-2.5 py-1 rounded-md bg-secondary border border-border">
          <Zap className="w-3 h-3 text-accent" />
          <span className="text-[11px] font-mono text-muted-foreground">Braket</span>
        </div>
      </div>
    </header>
  );
};
