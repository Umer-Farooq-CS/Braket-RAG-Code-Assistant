import React, { useEffect, useState } from "react";
import { ThemeName, applyTheme, getInitialTheme } from "../theme";
import { ThemeToggle } from "./ThemeToggle";
import { PromptForm } from "./PromptForm";
import type { AgentStep, GenerateRequest, GenerateResponse, RunSummary } from "../types/api";
import { listRuns, runPipeline } from "../api/client";

export const AppShell: React.FC = () => {
  const [theme, setTheme] = useState<ThemeName>(getInitialTheme);
  const [loading, setLoading] = useState(false);
  const [pipeline, setPipeline] = useState<GenerateResponse | null>(null);
  const [history, setHistory] = useState<RunSummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  useEffect(() => {
    listRuns()
      .then(setHistory)
      .catch(() => {
        // history is a nice-to-have; ignore failures on initial load
      });
  }, []);

  const handleRun = async (payload: GenerateRequest) => {
    setLoading(true);
    setError(null);
    try {
      const result = await runPipeline(payload);
      setPipeline(result);
      // refresh history list
      const runs = await listRuns();
      setHistory(runs);
    } catch (e) {
      const message = e instanceof Error ? e.message : String(e);
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const currentAgents: AgentStep[] = pipeline?.agents ?? [];

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="app-title-block">
          <span className="badge">v0.1</span>
          <h1 className="app-title">Braket RAG Code Assistant</h1>
          <p className="app-subtitle">
            Neo-brutalist lab for multi-agent Braket code generation.
          </p>
        </div>
        <div className="app-header-actions">
          <span className="env-pill">Local · FastAPI</span>
          <ThemeToggle theme={theme} onChange={setTheme} />
        </div>
      </header>

      <main className="app-main">
        <div className="pane pane-left">
          <div className="pane-label">Prompt &amp; Controls</div>
          <PromptForm loading={loading} onSubmit={handleRun} />
          {error && <div className="toast toast-error">{error}</div>}
        </div>
        <div className="pane pane-right">
          <div className="pane-label">Pipeline · Result · History</div>
          <div className="pane-right-content">
            <div className="right-section">
              <h2 className="section-title">Pipeline</h2>
              {currentAgents.length === 0 ? (
                <div className="pane-placeholder">
                  Run a prompt to see the multi-agent pipeline unfold here.
                </div>
              ) : (
                <div className="pipeline-row">
                  {currentAgents.map((step) => (
                    <div key={step.name} className={`agent-card agent-${step.name}`}>
                      <div className="agent-card-header">
                        <span className="agent-name">{step.name}</span>
                        <span className={`status-pill status-${step.status}`}>
                          {step.status}
                        </span>
                      </div>
                      {step.summary && (
                        <p className="agent-summary">{step.summary}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="right-section">
              <h2 className="section-title">Final code &amp; explanation</h2>
              {pipeline?.final_code ? (
                <pre className="code-block">
{pipeline.final_code}
                </pre>
              ) : (
                <div className="pane-placeholder">
                  Final Braket code will appear here after a successful run.
                </div>
              )}
            </div>

            <div className="right-section">
              <h2 className="section-title">Recent runs</h2>
              {history.length === 0 ? (
                <div className="pane-placeholder">
                  Recent runs will appear here as you use the assistant.
                </div>
              ) : (
                <ul className="history-list">
                  {history.map((item) => (
                    <li key={item.run_id} className="history-item">
                      <div className="history-main">
                        <span className="history-prompt">
                          {item.prompt_preview}
                        </span>
                        <span className={`status-pill status-${item.status}`}>
                          {item.status}
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

