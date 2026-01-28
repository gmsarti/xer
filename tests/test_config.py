import pytest
from xer.config import get_settings

def test_default_log_level():
    settings = get_settings()
    assert settings.log_level == "INFO"
    # Ensure the logger respects the level
    from xer.logger import logger
    assert logger.level == getattr(__import__('logging'), 'INFO')
