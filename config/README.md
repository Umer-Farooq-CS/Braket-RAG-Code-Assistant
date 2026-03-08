# Configuration Directory

This directory contains all configuration files for the Cirq-RAG-Code-Assistant project.

## Files

- **`config.json`** - Main configuration file with all settings
- **`config.dev.json`** - Development-specific configuration
- **`config.template.json`** - Template file for creating your own config
- **`config_loader.py`** - Python module that loads and manages configuration
- **`__init__.py`** - Package initialization file

## 📁 Directory Structure

```
config/
├── config.json              # Main configuration
├── config.dev.json          # Dev overrides
├── config.template.json     # Template
├── config_loader.py         # Loader module
├── __init__.py
├── README.md                # This file
└── ollama/                  # Ollama Modelfiles
    ├── designer_agent.Modelfile      # Code generation agent
    └── educational_agent.Modelfile   # Explanation agent
```

## Usage

### In Python Files

```python
from config import get_config, get_config_loader

# Get config dictionary
config = get_config()
model_name = config.get("models.embedding.model_name")

# Get config loader for advanced operations
config_loader = get_config_loader()
rag_section = config_loader.get_section("rag")
```

### In Notebooks

```python
import sys
from pathlib import Path

# Add project root to path
project_root = Path("..").resolve()
sys.path.insert(0, str(project_root))

# Import config
from config import get_config, get_config_loader

config = get_config()
```

## Configuration Structure

See `config.template.json` for the complete configuration structure with all available options.

## Environment Variables

The following environment variables can override config values:

- `OPENAI_API_KEY` - OpenAI API key
- `HUGGINGFACE_API_KEY` - Hugging Face API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `OLLAMA_HOST` - Ollama server URL (default: `http://localhost:11434`)
- `ENVIRONMENT` - Environment name (development, production)
- `DEBUG` - Debug mode (true/false)
- `LOG_LEVEL` - Logging level

## Setup

1. Copy the template:
   ```bash
   cp config/config.template.json config/config.json
   ```

2. Edit `config/config.json` and add your API keys

3. The config loader will automatically:
   - Load the appropriate config file based on environment
   - Apply environment variable overrides
   - Create all necessary directories
   - Setup PyTorch/CUDA configuration

---

## 🤖 Ollama Modelfiles

Custom Modelfiles define agent-specific LLM configurations with optimized parameters.

### What are Modelfiles?

Modelfiles are Ollama's configuration format that lets you:
- Set a **base model** (e.g., `llama3.1:8b`, `qwen2.5-coder:14b`)
- Define a **SYSTEM prompt** for agent behavior
- Configure **generation parameters** (temperature, tokens, etc.)
- Optimize **memory/GPU settings** for your hardware

### Available Modelfiles

| File | Agent | Purpose | Base Model |
|------|-------|---------|------------|
| `designer_agent.Modelfile` | cirq-designer-agent | Generate Cirq code (JSON output) | qwen2.5-coder:14b |
| `educational_agent.Modelfile` | cirq-edu-agent | Explain circuits (Markdown output) | llama3.1:8b |

### Commands

**Create an agent model:**
```bash
cd config/ollama
ollama create cirq-designer-agent -f designer_agent.Modelfile
```

**Remove an agent model:**
```bash
ollama rm cirq-designer-agent
```

**List all models:**
```bash
ollama list
```

**Test a model:**
```bash
ollama run cirq-designer-agent "Create a Bell state circuit"
```

**Recreate after modifying Modelfile:**
```bash
ollama rm cirq-designer-agent
ollama create cirq-designer-agent -f designer_agent.Modelfile
```

### Modelfile Parameters Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `FROM` | Base model to use | `FROM llama3.1:8b-instruct-q5_K_M` |
| `SYSTEM` | System prompt | `SYSTEM """You are a quantum expert..."""` |
| `temperature` | Randomness (0-1) | `PARAMETER temperature 0.1` |
| `top_p` | Nucleus sampling | `PARAMETER top_p 0.9` |
| `num_predict` | Max output tokens | `PARAMETER num_predict 2000` |
| `num_gpu` | GPU layers to load | `PARAMETER num_gpu 35` |
| `num_ctx` | Context window size | `PARAMETER num_ctx 2048` |
| `num_batch` | Batch size | `PARAMETER num_batch 512` |

### Customizing Modelfiles

To adjust for your hardware:

**Low VRAM (< 8GB):**
```dockerfile
PARAMETER num_gpu 15
PARAMETER num_ctx 1024
```

**High VRAM (16GB+):**
```dockerfile
PARAMETER num_gpu 50
PARAMETER num_ctx 4096
```

**CPU-only:**
```dockerfile
PARAMETER num_gpu 0
```
