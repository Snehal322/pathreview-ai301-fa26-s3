import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from api.routes.health import health_check

@pytest.mark.asyncio
async def test_health_check_postgres_healthy():
    mock_db = AsyncMock()
    mock_db.execute.return_value = None

    # Patch redis so redis check doesn't fail the overall health check during unit test
    with patch("redis.Redis") as mock_redis:
        mock_redis.return_value.ping.return_value = True
        
        try:
            response = await health_check(db=mock_db)
            # If all pass, it returns dict response directly
            assert response["dependencies"]["postgres"] == "healthy"
        except HTTPException as exc:
            # If redis or vector_db still raises 503, verify postgres itself is healthy in detail payload
            assert exc.detail["dependencies"]["postgres"] == "healthy"

    # Confirm database execute was called once with the text clause
    mock_db.execute.assert_called_once()