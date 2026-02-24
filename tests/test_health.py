def test_health_endpoints(client):
    api_health = client.get("/api/health")
    assert api_health.status_code == 200
    assert api_health.json().get("status") == "healthy"
