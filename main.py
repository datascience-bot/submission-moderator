"""Run submission moderator."""
from argparse import ArgumentParser
import logging
from os import getenv

import praw

from app import classify_submission
from app import document_removal_reasons

logger = logging.getLogger(__name__)

FLAGS = ArgumentParser()

FLAGS.add_argument(
    "-u",
    "--username",
    action="store",
    default=getenv("PRAW_USERNAME"),
    dest="username",
    required=False,
    type=str,
    help="Reddit user's username.",
)
FLAGS.add_argument(
    "-p",
    "--password",
    action="store",
    default=getenv("PRAW_PASSWORD"),
    dest="password",
    required=False,
    type=str,
    help="Reddit user's password.",
)
FLAGS.add_argument(
    "-c",
    "--client_id",
    action="store",
    default=getenv("PRAW_CLIENT_ID"),
    dest="client_id",
    required=False,
    type=str,
    help="Reddit API client_id.",
)
FLAGS.add_argument(
    "-s",
    "--client_secret",
    action="store",
    default=getenv("PRAW_CLIENT_SECRET"),
    dest="client_secret",
    required=False,
    type=str,
    help="Reddit API client_secret.",
)


def main():
    """Login to reddit and moderate submissions."""
    flags = FLAGS.parse_args()

    reddit = praw.Reddit(
        client_id=flags.client_id,
        client_secret=flags.client_secret,
        user_agent="u/datascience-bot",
        username=flags.username,
        password=flags.password,
    )

    for submission in reddit.subreddit("datascience").new(limit=10):
        if submission.approved:
            continue

        removal_reasons = classify_submission(submission)
        if removal_reasons:
            msg = document_removal_reasons(submission, removal_reasons)
            comment = submission.reply(msg)
            comment.mod.distinguish(how="yes", sticky=True)
            submission.mod.remove()
        else:
            submission.mod.approve()


if __name__ == "__main__":
    main()
