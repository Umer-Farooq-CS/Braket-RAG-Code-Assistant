export type AgentName =
  | "designer"
  | "validator"
  | "optimizer"
  | "final_validator"
  | "educational";

export interface AgentStep {
  name: AgentName;
  status: string;
  summary?: string;
  code?: string;
  logs?: string;
  metrics?: Record<string, unknown>;
}

export interface GenerateRequest {
  description: string;
  algorithm?: string;
  enable_validator: boolean;
  enable_optimizer: boolean;
  enable_educational: boolean;
  max_optimization_loops: number;
}

export interface GenerateResponse {
  run_id: string;
  status: string;
  created_at: string;
  prompt: string;
  algorithm?: string;
  agents: AgentStep[];
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

