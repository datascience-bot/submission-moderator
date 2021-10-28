"""Configure tests."""
from unittest.mock import Mock

import pytest


@pytest.fixture(scope="function")
def submission():
    """Mock a submission with the commonly accessed attributes."""
    submission = Mock()
    submission.author = Mock()
    submission.author.comment_karma = 42
    submission.author.link_karma = 42
    submission.url = "reddit.com"

    return submission
