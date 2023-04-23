"""
Скрипт для проверки обновлений образов Docker.

Зависимости:
* Docker Hub Tool https://github.com/docker/hub-tool
* Docker Hub учетная запись
* Docker должен быть установлен
"""

import json
import logging
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import pexpect
from dateutil import parser
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")

MARKDOWN_FILE = "roles/homelab_svc/spnas/README.md"
ARM = ["arm32", "arm64"]


def get_repos(file_path: str) -> list:
    """Find all docker image repository names in markdown file."""
    content = Path(file_path).read_text()
    return re.findall(r"\[(.+?)\]", content)


def docker_login(username: str, password: str) -> None:
    """Login to the Docker Hub in hub-tool."""
    child = pexpect.spawn("hub-tool login")
    child.expect("Username:")
    child.sendline(username)
    child.expect("Password:")
    child.sendline(password)
    child.expect("Login Succeeded", timeout=10)


def list_tags(repository: str) -> list[dict]:
    """List all docker image tags in repository."""
    try:
        logger.info("%s", repository)
        hub_tool = subprocess.run(
            [
                "hub-tool",
                "tag",
                "ls",
                "--format",
                "json",
                "--sort",
                "updated",
                repository,
            ],
            capture_output=True,
            check=True,
            encoding="utf-8",
        )
        if not hub_tool.stdout:
            logger.error("%s: something bad happened", repository)
            return
        if hub_tool.stdout == "null\n":
            logger.error("%s: repo not found on docker hub", repository)
            return
        return json.loads(hub_tool.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)


def filter_tags(tags: list[dict], days: int = 7) -> None:
    """Filter docker image tags by date."""
    for tag in tags:
        tag_last_updated = tag["LastUpdated"]
        tag_last_updated_dt = parser.parse(tag_last_updated).replace(tzinfo=None)
        if tag_last_updated_dt < datetime.now() - timedelta(days=days):
            return
        tag_name = tag["Name"]
        if not any(platform in tag_name for platform in ARM):
            print(tag_name, "-", tag_last_updated)


def main():
    """Main function."""
    docker_login(DOCKER_USERNAME, DOCKER_PASSWORD)
    repos = get_repos(MARKDOWN_FILE)
    for repo in repos:
        tags = list_tags(repo)
        if tags is not None:
            filter_tags(tags)
            print("")


if __name__ == "__main__":
    __version__ = "0.0.1"
    logging.basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(name)s:%(lineno)s:%(funcName)20s()] --- %(message)s",
        level=logging.DEBUG,
    )
    main()
