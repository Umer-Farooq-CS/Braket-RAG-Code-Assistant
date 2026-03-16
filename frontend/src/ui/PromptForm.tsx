import React, { useMemo, useState } from "react";
import type { GenerateRequest } from "../types/api";

export interface PromptFormValues {
  description: string;
  algorithm: string;
  enableValidator: boolean;
  enableOptimizer: boolean;
  enableEducational: boolean;
  maxOptimizationLoops: number;
}

interface PromptFormProps {
  loading: boolean;
  onSubmit: (payload: GenerateRequest) => void;
}

export const PromptForm: React.FC<PromptFormProps> = ({ loading, onSubmit }) => {
  const [values, setValues] = useState<PromptFormValues>({
    description: "",
    algorithm: "",
    enableValidator: true,
    enableOptimizer: true,
    enableEducational: true,
    maxOptimizationLoops: 3
  });

  const [touched, setTouched] = useState(false);

  const charCount = values.description.length;
  const isValid = values.description.trim().length > 0;

  const error = useMemo(() => {
    if (!touched) return "";
    if (!isValid) return "Describe the quantum task you want to generate.";
    return "";
  }, [isValid, touched]);

  const handleChange = (
    field: keyof PromptFormValues,
    value: string | boolean | number
  ) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setTouched(true);
    if (!isValid) return;

    const payload: GenerateRequest = {
      description: values.description.trim(),
      algorithm: values.algorithm || undefined,
      enable_validator: values.enableValidator,
      enable_optimizer: values.enableOptimizer,
      enable_educational: values.enableEducational,
      max_optimization_loops: values.maxOptimizationLoops
    };
    onSubmit(payload);
  };

  return (
    <form className="prompt-form" onSubmit={handleSubmit}>
      <div className="prompt-header-row">
        <span className="prompt-label">Describe your Braket task</span>
        <span className="prompt-meta">
          <span className="pill pill-soft">
            {charCount} chars
          </span>
        </span>
      </div>

      <textarea
        className="prompt-textarea"
        placeholder='e.g. "Create a VQE circuit for H2 with 4 qubits and explain each step."'
        value={values.description}
        onChange={(e) => handleChange("description", e.target.value)}
        onBlur={() => setTouched(true)}
        rows={6}
      />
      {error && <div className="field-error">{error}</div>}

      <div className="prompt-grid">
        <div className="prompt-column">
          <div className="field-group">
            <label className="field-label" htmlFor="algorithm">
              Algorithm hint
            </label>
            <input
              id="algorithm"
              className="field-input"
              placeholder="vqe, qaoa, grover, qft..."
              value={values.algorithm}
              onChange={(e) => handleChange("algorithm", e.target.value)}
            />
            <p className="field-help">
              Optional hint to steer the Designer agent.
            </p>
          </div>

          <div className="field-group">
            <div className="field-label">Agents</div>
            <div className="toggle-row">
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={values.enableValidator}
                  onChange={(e) => handleChange("enableValidator", e.target.checked)}
                />
                <span className="toggle-pill">
                  <span className="toggle-dot" />
                </span>
                <span className="toggle-text">Validator</span>
              </label>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={values.enableOptimizer}
                  onChange={(e) => handleChange("enableOptimizer", e.target.checked)}
                />
                <span className="toggle-pill">
                  <span className="toggle-dot" />
                </span>
                <span className="toggle-text">Optimizer</span>
              </label>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={values.enableEducational}
                  onChange={(e) => handleChange("enableEducational", e.target.checked)}
                />
                <span className="toggle-pill">
                  <span className="toggle-dot" />
                </span>
                <span className="toggle-text">Educational</span>
              </label>
            </div>
          </div>
        </div>

        <div className="prompt-column">
          <details className="accordion">
            <summary className="accordion-summary">
              Advanced pipeline controls
            </summary>
            <div className="accordion-body">
              <div className="field-group">
                <label className="field-label" htmlFor="loops">
                  Optimization loop limit
                </label>
                <input
                  id="loops"
                  type="number"
                  min={1}
                  max={10}
                  className="field-input"
                  value={values.maxOptimizationLoops}
                  onChange={(e) =>
                    handleChange("maxOptimizationLoops", Number(e.target.value) || 1)
                  }
                />
                <p className="field-help">
                  How many times the Optimizer ↔ Validator loop may run.
                </p>
              </div>
              <p className="field-help">
                Additional model and temperature controls can be surfaced here as the backend
                evolves.
              </p>
            </div>
          </details>
        </div>
      </div>

      <div className="prompt-footer">
        <button
          type="submit"
          className="primary-btn"
          disabled={loading || !isValid}
        >
          {loading ? "Running pipeline…" : "Run pipeline"}
        </button>
      </div>
    </form>
  );
};

