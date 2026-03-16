import React, { useState, useCallback } from 'react';
import { Header } from '@/components/Header';
import { LeftSidebar } from '@/components/LeftSidebar';
import { RightSidebar } from '@/components/RightSidebar';
import { ChatWindow } from '@/components/ChatWindow';
import { generateCode } from '@/api/client';
import type { ChatSession, ChatMessage, AgentConfig, AgentStatus } from '@/types/chat';
import type { GenerateResponse, BackendAgentStep } from '@/api/client';

function mapBackendStatus(status: string): AgentStatus['status'] {
  if (status === 'success' || status === 'done') return 'done';
  if (status === 'running') return 'running';
  if (status === 'skipped') return 'skipped';
  if (status === 'warning' || status === 'info') return 'done';
  if (status === 'error') return 'done';
  return 'idle';
}

const AGENT_LABELS: Record<string, string> = {
  designer: 'Designer Agent',
  optimizer: 'Optimizer Agent',
  validator: 'Validator Agent',
  final_validator: 'Final Validator',
  educational: 'Educational Agent',
};

function mapAgentSteps(steps: BackendAgentStep[]): AgentStatus[] {
  return steps.map((s) => ({
    id: s.name as AgentStatus['id'],
    label: AGENT_LABELS[s.name] ?? s.name,
    status: mapBackendStatus(s.status),
    detail: s.summary ?? undefined,
  }));
}

function formatExplanation(raw: Record<string, unknown>): string {
  if (raw.markdown && typeof raw.markdown === 'string') {
    return raw.markdown;
  }
  return formatExplanationParts(raw);
}

function formatExplanationParts(raw: Record<string, unknown>): string {
  const parts: string[] = [];

  if (raw.overview && typeof raw.overview === 'string') {
    parts.push(`## Overview\n\n${raw.overview}`);
  }
  if (raw.step_by_step && Array.isArray(raw.step_by_step)) {
    parts.push('## Step-by-Step Explanation\n');
    raw.step_by_step.forEach((s, i) => parts.push(`${i + 1}. ${String(s)}`));
  }
  if (raw.key_concepts && Array.isArray(raw.key_concepts)) {
    parts.push('\n## Key Concepts\n');
    raw.key_concepts.forEach(c => parts.push(`- ${String(c)}`));
  }
  if (raw.tips && Array.isArray(raw.tips)) {
    parts.push('\n## Tips\n');
    raw.tips.forEach(t => parts.push(`- ${String(t)}`));
  }
  if (parts.length > 0) return parts.join('\n');

  return formatRawEntries(raw);
}

function formatRawEntries(raw: Record<string, unknown>): string {
  const entries = Object.entries(raw).filter(([, v]) => v != null);
  if (entries.length === 0) return '';

  const parts: string[] = [];
  for (const [key, val] of entries) {
    const heading = key.replaceAll('_', ' ').replaceAll(/\b\w/g, c => c.toUpperCase());
    if (typeof val === 'string') {
      parts.push(`## ${heading}\n\n${val}`);
    } else if (Array.isArray(val)) {
      parts.push(`## ${heading}\n`);
      val.forEach(item => {
        const text = typeof item === 'string' ? item : JSON.stringify(item);
        parts.push(`- ${text}`);
      });
    }
  }
  return parts.length > 0 ? parts.join('\n') : JSON.stringify(raw, null, 2);
}

function toNum(v: unknown): number {
  return typeof v === 'number' ? v : 0;
}

function safeRecord(obj: unknown): Record<string, unknown> {
  return (typeof obj === 'object' && obj !== null ? obj : {}) as Record<string, unknown>;
}

function extractMetrics(response: GenerateResponse): { depth: number; gates: number; qubits: number } {
  const validatorStep = [...response.agents].reverse().find(
    a => (a.name === 'final_validator' || a.name === 'validator') && a.metrics
  );
  const sm = safeRecord(validatorStep?.metrics);

  const rawResult = response.raw_result ?? {};
  const validation = safeRecord(rawResult.final_validation ?? rawResult.validation);
  const valAnalysis = safeRecord(validation.analysis);
  const vm = safeRecord(valAnalysis.metrics);
  const om = safeRecord(rawResult.optimization_metrics);

  const depth = toNum(sm.depth ?? vm.depth ?? om.depth);
  const gates = toNum(sm.num_operations ?? vm.num_operations ?? om.num_operations);
  const qubits = toNum(sm.num_qubits ?? vm.num_qubits ?? om.num_qubits);

  return { depth, gates, qubits };
}

function getValidationLabel(hasValidator: boolean, passed: boolean): 'Passed' | 'Failed' | 'Skipped' {
  if (!hasValidator) return 'Skipped';
  return passed ? 'Passed' : 'Failed';
}

function buildAssistantMessage(response: GenerateResponse, config: AgentConfig): ChatMessage {
  const agentStatuses = mapAgentSteps(response.agents);

  let explanation = '';
  if (response.explanation) {
    const raw = response.explanation;
    if (typeof raw === 'string') {
      explanation = raw;
    } else {
      explanation = formatExplanation(raw);
    }
  }

  const hasValidator = response.agents.some(a => a.name === 'validator' || a.name === 'final_validator');
  const validatorPassed = response.agents.some(
    a => (a.name === 'validator' || a.name === 'final_validator') && a.metrics?.validation_passed === true
  );

  const content = explanation
    || (response.status === 'completed'
        ? 'Pipeline completed successfully. See the generated code below.'
        : `Pipeline finished with status: **${response.status}**`);

  const { depth, gates, qubits } = extractMetrics(response);

  const optimizerStep = response.agents.find(a => a.name === 'optimizer');
  const optDiffs = (optimizerStep?.metrics ?? {}) as Record<string, number>;
  let optimizationNote: string | undefined;
  if (optimizerStep) {
    const depthDelta = optDiffs.depth ?? 0;
    optimizationNote = depthDelta < 0
      ? `Depth reduced by ${Math.abs(depthDelta)}`
      : 'Optimized';
  }

  return {
    id: response.run_id,
    role: 'assistant',
    content,
    agentStatuses,
    codeBlock: response.final_code
      ? { language: 'python', code: response.final_code, filename: 'circuit.py' }
      : undefined,
    metrics: response.final_code
      ? {
          depth,
          gates,
          qubits,
          validation: getValidationLabel(hasValidator, validatorPassed),
          simulator: 'Amazon Braket Local',
          optimizationNote,
        }
      : undefined,
    isStreaming: false,
    timestamp: new Date(),
  };
}

function buildOptimisticSteps(config: AgentConfig): AgentStatus[] {
  const steps: AgentStatus[] = [
    { id: 'designer', label: 'Designer Agent', status: 'running', detail: 'Generating Braket code from RAG context...' },
  ];
  if (config.validatorEnabled) {
    steps.push({ id: 'validator', label: 'Validator Agent', status: 'idle' });
  }
  if (config.optimizerEnabled) {
    steps.push({ id: 'optimizer', label: 'Optimizer Agent', status: 'idle' });
  }
  if (config.educationalDepth !== 'Low') {
    steps.push({ id: 'educational', label: 'Educational Agent', status: 'idle' });
  }
  return steps;
}

const DEFAULT_CONFIG: AgentConfig = {
  designerEnabled: true,
  optimizerEnabled: true,
  validatorEnabled: true,
  educationalDepth: 'High',
};

const Index: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [config, setConfig] = useState<AgentConfig>(DEFAULT_CONFIG);
  const [isGenerating, setIsGenerating] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState<ChatMessage | null>(null);

  const activeSession = sessions.find(s => s.id === activeSessionId) ?? null;
  const visibleMessages: ChatMessage[] = [
    ...(activeSession?.messages ?? []),
    ...(streamingMessage ? [streamingMessage] : []),
  ];

  const createNewSession = useCallback(() => {
    const id = crypto.randomUUID();
    const session: ChatSession = {
      id,
      title: 'New Circuit',
      messages: [],
      createdAt: new Date(),
    };
    setSessions(prev => [session, ...prev]);
    setActiveSessionId(id);
    setStreamingMessage(null);
  }, []);

  const handleSendMessage = useCallback(async (content: string) => {
    if (isGenerating) return;

    let sessionId = activeSessionId;
    if (!sessionId) {
      const id = crypto.randomUUID();
      const session: ChatSession = {
        id,
        title: content.slice(0, 40),
        messages: [],
        createdAt: new Date(),
      };
      setSessions(prev => [session, ...prev]);
      setActiveSessionId(id);
      sessionId = id;
    }

    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setSessions(prev => prev.map(s =>
      s.id === sessionId
        ? { ...s, messages: [...s.messages, userMsg], title: s.messages.length === 0 ? content.slice(0, 40) : s.title }
        : s
    ));

    setIsGenerating(true);
    const streamId = crypto.randomUUID();
    const optimisticSteps = buildOptimisticSteps(config);
    setStreamingMessage({
      id: streamId,
      role: 'assistant',
      content: '',
      agentStatuses: optimisticSteps,
      isStreaming: true,
      timestamp: new Date(),
    });

    try {
      const response = await generateCode(content, config);
      const assistantMsg = buildAssistantMessage(response, config);

      setSessions(s => s.map(sess =>
        sess.id === sessionId
          ? { ...sess, messages: [...sess.messages, assistantMsg] }
          : sess
      ));
      setStreamingMessage(null);
    } catch (err) {
      const errorText = err instanceof Error ? err.message : String(err);
      const errorMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `**Error from pipeline:**\n\n\`\`\`\n${errorText}\n\`\`\`\n\nPlease check that the FastAPI backend is running on port 8000.`,
        agentStatuses: optimisticSteps.map(s => ({ ...s, status: 'skipped' as const })),
        isStreaming: false,
        timestamp: new Date(),
      };
      setSessions(s => s.map(sess =>
        sess.id === sessionId
          ? { ...sess, messages: [...sess.messages, errorMsg] }
          : sess
      ));
      setStreamingMessage(null);
    } finally {
      setIsGenerating(false);
    }
  }, [activeSessionId, isGenerating, config]);

  const handleStopGeneration = useCallback(() => {
    setIsGenerating(false);
    if (streamingMessage) {
      setSessions(prev => prev.map(s =>
        s.id === activeSessionId
          ? { ...s, messages: [...s.messages, { ...streamingMessage, isStreaming: false }] }
          : s
      ));
      setStreamingMessage(null);
    }
  }, [streamingMessage, activeSessionId]);

  return (
    <div className="flex flex-col h-screen bg-background text-foreground overflow-hidden">
      <Header
        onSettingsToggle={() => setSettingsOpen(v => !v)}
        settingsOpen={settingsOpen}
      />
      <div className="flex flex-1 overflow-hidden">
        <LeftSidebar
          sessions={sessions}
          activeSessionId={activeSessionId}
          onNewSession={createNewSession}
          onSelectSession={setActiveSessionId}
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(v => !v)}
        />

        <main className="flex-1 overflow-hidden">
          <ChatWindow
            messages={visibleMessages}
            isGenerating={isGenerating}
            onSendMessage={handleSendMessage}
            onStopGeneration={handleStopGeneration}
            config={config}
          />
        </main>

        <RightSidebar
          open={settingsOpen}
          onClose={() => setSettingsOpen(false)}
          config={config}
          onConfigChange={setConfig}
        />
      </div>
    </div>
  );
};

export default Index;
