"""Pytest configuration and shared fixtures."""

import pytest
import sys
import os
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture
def src_path():
    """Return the src directory path."""
    return project_root / "src"

@pytest.fixture
def test_data_path():
    """Return the test data directory path."""
    return Path(__file__).parent / "data"

@pytest.fixture
def temp_output_path(tmp_path):
    """Return a temporary output directory."""
    return tmp_path / "outputs"

@pytest.fixture(scope="session")
def test_config():
    """Return test configuration."""
    return {
        "test_mode": True,
        "log_level": "DEBUG",
        "max_iterations": 5,
        "timeout_seconds": 30,
    }

@pytest.fixture
def mock_braket_circuit():
    """Return a mock Braket circuit for testing."""
    from braket.circuits import Circuit

    circuit = Circuit()
    circuit.h(0)
    circuit.cnot(0, 1)

    return circuit

@pytest.fixture
def mock_quantum_algorithm():
    """Return mock quantum algorithm data."""
    return {
        "name": "test_algorithm",
        "description": "A test quantum algorithm",
        "qubits": 2,
        "gates": ["H", "CNOT", "M"],
        "expected_output": "00 or 11 with equal probability"
    }

# Markers for different test types
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "gpu: marks tests that require GPU")
    config.addinivalue_line("markers", "quantum: marks tests that require quantum simulators")
