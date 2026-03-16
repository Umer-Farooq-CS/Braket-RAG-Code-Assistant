export interface AgentStatus {
  id: 'designer' | 'optimizer' | 'validator' | 'final_validator' | 'educational';
  label: string;
  status: 'idle' | 'running' | 'done' | 'skipped';
  detail?: string;
}

export interface CircuitMetrics {
  depth: number;
  gates: number;
  qubits: number;
  validation: 'Passed' | 'Failed' | 'Skipped';
  simulator?: string;
  optimizationNote?: string;
  educationalSummary?: string;
}

export type MessageRole = 'user' | 'assistant';

export interface CodeBlock {
  language: string;
  code: string;
  filename?: string;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  codeBlock?: CodeBlock;
  agentStatuses?: AgentStatus[];
  metrics?: CircuitMetrics;
  isStreaming?: boolean;
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: Date;
}

export interface AgentConfig {
  designerEnabled: boolean;
  optimizerEnabled: boolean;
  validatorEnabled: boolean;
  educationalDepth: 'Low' | 'Intermediate' | 'High' | 'Very High';
}
