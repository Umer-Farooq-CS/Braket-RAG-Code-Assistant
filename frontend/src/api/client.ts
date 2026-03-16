import type { AgentConfig } from "@/types/chat";

export interface BackendAgentStep {
  name: string;
  status: string;
  summary?: string;
  code?: string;
  logs?: string;
  metrics?: Record<string, unknown>;
}

export interface GenerateResponse {
  run_id: string;
  status: string;
  created_at: string;
  prompt: string;
  algorithm?: string;
  agents: BackendAgentStep[];
  final_code?: string;
  explanation?: Record<string, unknown>;
  raw_result: Record<string, unknown>;
}

export interface RunSummary {
  run_id: string;
  created_at: string;
  prompt_preview: string;
  status: string;
  enable_validator: boolean;
  enable_optimizer: boolean;
  enable_educational: boolean;
}

async function handleJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }
  return (await res.json()) as T;
}

export async function generateCode(
  description: string,
  config: AgentConfig,
): Promise<GenerateResponse> {
  const depthMap: Record<AgentConfig["educationalDepth"], string> = {
    Low: "low",
    Intermediate: "intermediate",
    High: "high",
    "Very High": "very_high",
  };

  const res = await fetch("/api/v1/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      description,
      algorithm: undefined,
      enable_validator: config.validatorEnabled,
      enable_optimizer: config.optimizerEnabled,
      // Educational agent is always enabled; depth controls verbosity only.
      enable_educational: true,
      educational_depth: depthMap[config.educationalDepth] ?? "intermediate",
      max_optimization_loops: 3,
    }),
  });
  return handleJson<GenerateResponse>(res);
}

export async function listRuns(): Promise<RunSummary[]> {
  const res = await fetch("/api/v1/runs");
  return handleJson<RunSummary[]>(res);
}
