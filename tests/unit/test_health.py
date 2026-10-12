from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
import pytest
from sqlalchemy.sql.elements import TextClause
from api.routes.health import health_check

@pytest.mark.asyncio
async def test_health_check_uses_text_clause():
    mock_db = AsyncMock()
    mock_db.execute.return_value = True

    mock_settings = MagicMock()
    mock_settings.redis_host = "localhost"
    mock_settings.redis_port = 6379
    mock_settings.vector_db_url = None

    with patch("redis.Redis") as mock_redis, patch("core.config.settings", mock_settings):
        mock_redis.return_value.ping.return_value = True
        
        response = await health_check(db=mock_db)
        
        mock_db.execute.assert_called_once()
        executed_arg = mock_db.execute.call_args[0][0]
        assert isinstance(executed_arg, TextClause), "SQL query must be wrapped in SQLAlchemy text() clause"
        assert response["status"] == "healthy"