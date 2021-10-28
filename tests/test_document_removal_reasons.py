"""Test removal message."""
import pytest

from app import document_removal_reasons


@pytest.mark.parametrize(
    "removal_reasons", [["blog"], ["newbie"], ["porn"], ["video"], ["newbie", "video"]]
)
def test_document_removal_reasons(submission, removal_reasons):
    msg = document_removal_reasons(submission, removal_reasons)

    assert len(msg) > 80
    assert "* " in msg
