"""u/datascience-bot -- Submission Moderator.

Logic for moderating submissions to r/datascience.
"""
from typing import List

import praw


def classify_submission(submission: praw.models.Submission):
    """Classify submissions per removal reasons."""
    removal_reasons: List[str] = []

    if submission.author.comment_karma + submission.author.link_karma < 50:
        removal_reasons.append("newbie")

    for rr in ("blog", "porn", "video"):
        with open(f"app/data/blocklists/{rr}.txt", "r") as ifile:
            if any(line.strip() in submission.url for line in ifile):
                removal_reasons.append(rr)

    return sorted(removal_reasons)


def document_removal_reasons(
    submission: praw.models.Submission, removal_reasons: List[str]
):
    """Document removal reasons.

    Write a concise message summarizing why the submission must be removed.
    """
    violations: List[str] = []

    if "blog" in removal_reasons:
        violations.append(
            "**Articles from blog aggregators are not allowed.** "
            f"Submissions from {submission.domain} are not allowed on "
            "r/datascience."
        )
    if "newbie" in removal_reasons:
        min_k = 50
        user_k = submission.author.comment_karma + submission.author.link_karma
        entering_and_transitioning_thread = "[Entering and Transitioning thread](https://www.reddit.com/r/datascience/search/?q=Weekly%20Entering%20%26%20Transitioning%20Thread&restrict_sr=1&sort=new&t=week)"  # noqa: E501
        violations.append(
            "**Not enough karma.** "
            "You don't have enough karma to start a new thread on r/datascience. "
            f"Please post your questions in the {entering_and_transitioning_thread} "
            f"until you accumulate at least {min_k} karma. "
            f"Right now you have {user_k} karma."
        )
    if "porn" in removal_reasons:
        violations.append(
            "**NSFW links are not allowed.** Porn is not allowed on r/datascience."
        )
    if "video" in removal_reasons:
        violations.append(
            "**Videos are not allowed.** "
            f"Submissions from {submission.domain} are not allowed on r/datascience."
        )

    preamble = (
        f"Hi u/{submission.author.name},"
        "I removed your submission for the following removal reasons:"
    )
    formatted_violations = "\n".join([f"* {v}" for v in violations])
    msg = "\n\n".join([preamble, formatted_violations])

    return msg
