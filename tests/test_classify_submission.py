"""Test submission classifier."""
from app import classify_submission

# Sample blocklisted blog url.
BLOG_URL: str = "https://medium.com/refraction-tech-everything/how-netflix-works-the-hugely-simplified-complex-stuff-that-happens-every-time-you-hit-play-3a40c9be254b"  # noqa: E501


def test_classify_submission__blog(submission):
    submission.url = BLOG_URL

    actual = classify_submission(submission)
    expected = ["blog"]

    assert expected == actual


def test_classify_submission__clean(submission):
    actual = classify_submission(submission)
    expected = []

    assert expected == actual


def test_classify_submission__newbie(submission):
    submission.author.comment_karma = 1
    submission.author.link_karma = 1

    actual = classify_submission(submission)
    expected = ["newbie"]

    assert expected == actual


def test_classify_submission__porn(submission):
    submission.url = "https://www.pornhub.com/some-link"

    actual = classify_submission(submission)
    expected = ["porn"]

    assert expected == actual


def test_classify_submission_video(submission):
    submission.url = "https://www.youtube.com/watch?v=l_RtpWGa8LY"

    actual = classify_submission(submission)
    expected = ["video"]

    assert expected == actual


def test_classify_submission__blog_newbie(submission):
    submission.author.comment_karma = 1
    submission.author.link_karma = 1
    submission.url = BLOG_URL

    actual = classify_submission(submission)
    expected = ["blog", "newbie"]

    assert expected == actual
