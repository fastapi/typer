import logging
import sys
from pathlib import Path
from typing import Optional

from github import Github
from github.PullRequest import PullRequest
from pydantic import BaseModel, BaseSettings, SecretStr, ValidationError


class Settings(BaseSettings):
    github_repository: str
    github_event_path: Path
    github_event_name: Optional[str] = None
    input_token: SecretStr
    input_deploy_url: str


class PartialGithubEventHeadCommit(BaseModel):
    id: str


class PartialGithubEventWorkflowRun(BaseModel):
    head_commit: PartialGithubEventHeadCommit


class PartialGithubEvent(BaseModel):
    workflow_run: PartialGithubEventWorkflowRun


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    logging.info(f"Using config: {settings.json()}")
    g = Github(settings.input_token.get_secret_value())
    repo = g.get_repo(settings.github_repository)
    try:
        event = PartialGithubEvent.parse_file(settings.github_event_path)
    except ValidationError as e:
        logging.error(f"Error parsing event file: {e.errors()}")
        sys.exit(0)
    use_pr: Optional[PullRequest] = None
    for pr in repo.get_pulls():
        if pr.head.sha == event.workflow_run.head_commit.id:
            use_pr = pr
            break
    if not use_pr:
        logging.error(f"No PR found for hash: {event.workflow_run.head_commit.id}")
        sys.exit(0)
    use_pr.create_issue_comment(
        f"📝 Docs preview for commit {use_pr.head.sha} at: {settings.input_deploy_url}"
    )
    logging.info("Finished")
