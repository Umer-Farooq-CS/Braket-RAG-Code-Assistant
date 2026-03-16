import type { GenerateRequest, GenerateResponse, RunSummary } from "../types/api";

async function handleJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }
  return (await res.json()) as T;
}

export async function runPipeline(payload: GenerateRequest): Promise<GenerateResponse> {
  const res = await fetch("/api/v1/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  return handleJson<GenerateResponse>(res);
}

export async function listRuns(): Promise<RunSummary[]> {
  const res = await fetch("/api/v1/runs");
  return handleJson<RunSummary[]>(res);
}

export type { GenerateRequest, GenerateResponse, RunSummary };

