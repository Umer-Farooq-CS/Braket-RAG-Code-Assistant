import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { Atom } from 'lucide-react';
import type { ChatMessage } from '@/types/chat';
import { AgentStatusIndicator } from './AgentStatusIndicator';
import { CodeBlock } from './CodeBlock';
import { MetricsCard } from './MetricsCard';

interface MessageBubbleProps {
  message: ChatMessage;
}

const TypingIndicator = () => (
  <div className="flex items-center gap-1 px-4 py-3">
    {[0, 1, 2].map((i) => (
      <motion.div
        key={i}
        className="w-1.5 h-1.5 rounded-full bg-muted-foreground"
        animate={{ scale: [1, 1.4, 1], opacity: [0.4, 1, 0.4] }}
        transition={{ duration: 1, delay: i * 0.2, repeat: Infinity }}
      />
    ))}
  </div>
);

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-end"
      >
        <div className="max-w-[75%] px-4 py-3 rounded-2xl rounded-br-md gradient-primary text-white text-sm leading-relaxed shadow-lg">
          {message.content}
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-start gap-3"
    >
      {/* Avatar */}
      <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center shrink-0 mt-0.5">
        <Atom className="w-3.5 h-3.5 text-white" />
      </div>

      <div className="flex-1 min-w-0 space-y-3">
        {/* Agent status steps */}
        {message.agentStatuses && message.agentStatuses.length > 0 && (
          <AgentStatusIndicator statuses={message.agentStatuses} />
        )}

        {/* Streaming / typing */}
        {message.isStreaming && !message.content && !message.agentStatuses?.length && (
          <div className="rounded-xl bg-surface border border-border/50 card-shadow inline-block">
            <TypingIndicator />
          </div>
        )}

        {/* Text content */}
        {message.content && (
          <div className="rounded-xl bg-surface border border-border/50 card-shadow px-4 py-3 text-sm leading-relaxed prose prose-sm max-w-none dark:prose-invert prose-code:text-primary prose-code:bg-muted prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:text-xs prose-headings:text-foreground prose-p:text-foreground prose-li:text-foreground">
            {message.isStreaming ? (
              <span>{message.content}<span className="inline-block w-0.5 h-4 bg-primary ml-0.5 animate-pulse" /></span>
            ) : (
              <ReactMarkdown>{message.content}</ReactMarkdown>
            )}
          </div>
        )}

        {/* Code block */}
        {message.codeBlock && (
          <div>
            <CodeBlock
              block={message.codeBlock}
              isPulsing={message.isStreaming}
            />
            {/* Metrics — shown below code, merged border */}
            {message.metrics && !message.isStreaming && (
              <MetricsCard metrics={message.metrics} />
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
};
