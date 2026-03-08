"""Configuration package for Cirq-RAG-Code-Assistant."""

import sys
from pathlib import Path

# Add project root to path to access config folder
_project_root = Path(__file__).parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Import from root config folder
try:
    from config import get_config, get_config_loader, reload_config, ConfigLoader
except ImportError:
    # Fallback if config folder not in path
    import importlib.util
    config_path = _project_root / "config" / "config_loader.py"
    if config_path.exists():
        spec = importlib.util.spec_from_file_location("config_loader", config_path)
        config_loader_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_loader_module)
        get_config = config_loader_module.get_config
        get_config_loader = config_loader_module.get_config_loader
        reload_config = config_loader_module.reload_config
        ConfigLoader = config_loader_module.ConfigLoader
    else:
        raise ImportError("Config loader not found. Please ensure config/config_loader.py exists.")

from .logging import LoggingConfig, setup_logging, get_logger, setup_default_logging

__all__ = [
    "LoggingConfig",
    "setup_logging",
    "get_logger",
    "setup_default_logging",
    "ConfigLoader",
    "get_config_loader",
    "get_config",
    "reload_config",
]