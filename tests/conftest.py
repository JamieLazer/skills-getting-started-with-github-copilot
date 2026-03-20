"""Shared test fixtures and configuration for the Mergington API tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provide a TestClient for the FastAPI app.
    
    This fixture creates a test client that can be used to make requests
    to the API endpoints without running a real server.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Provide a sample email for test signup operations."""
    return "test_student@mergington.edu"


@pytest.fixture
def existing_activity():
    """Provide an activity name that exists in the app."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Provide an activity name that doesn't exist in the app."""
    return "Nonexistent Club"
