"""
Unit tests for sales API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_sales_endpoints_require_auth():
    """Test that sales endpoints require authentication."""
    # Test without authentication headers
    response = client.get("/api/sales")
    assert response.status_code == 401
    
    response = client.post("/api/sales", json={})
    assert response.status_code == 401


# Add more tests as needed
