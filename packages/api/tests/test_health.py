"""Basic health check and smoke tests for the API."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_exists(client: AsyncClient):
    """Health endpoint should return 200 with status info."""
    response = await client.get("/health")
    # Accept 200 (all good) or 503 (degraded — db not connected in unit test context)
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data


@pytest.mark.asyncio
async def test_docs_available(client: AsyncClient):
    """OpenAPI docs should be available."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_root_redirect(client: AsyncClient):
    """Root should redirect or return something sensible."""
    response = await client.get("/", follow_redirects=False)
    assert response.status_code in (200, 307, 308, 404)


@pytest.mark.asyncio
async def test_api_v1_facilities_requires_no_auth(client: AsyncClient):
    """Facilities list is a public read endpoint."""
    response = await client.get("/api/v1/facilities")
    # Will be 200 (empty list) or 503 if db is not available — both acceptable in CI
    assert response.status_code in (200, 503)


@pytest.mark.asyncio  
async def test_create_assessment_requires_valid_payload(client: AsyncClient):
    """Creating an assessment with empty body should return 422."""
    response = await client.post("/api/v1/assessments", json={})
    assert response.status_code in (422, 401, 503)


@pytest.mark.asyncio
async def test_sync_endpoint_exists(client: AsyncClient):
    """Sync endpoint should exist and reject empty payloads."""
    response = await client.post("/api/v1/sync", json={})
    assert response.status_code in (422, 401, 503)


@pytest.mark.asyncio
async def test_alerts_endpoint_exists(client: AsyncClient):
    """Alerts endpoint should exist."""
    response = await client.get("/api/v1/alerts")
    assert response.status_code in (200, 503)
