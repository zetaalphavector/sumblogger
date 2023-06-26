class TestHealthCheck:
    async def test_healthcheck(self, test_client):
        response = await test_client.get("/healthcheck")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
