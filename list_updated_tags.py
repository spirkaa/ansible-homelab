"""
Скрипт для проверки обновлений образов Docker.

Зависимости:
* Docker Hub Tool https://github.com/docker/hub-tool
* Docker Hub учетная запись
* Docker должен быть установлен
"""

import logging
import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from dateutil import parser
from pathlib import Path

import pexpect
from dotenv import load_dotenv

logger = logging.getLogger("__name__")

load_dotenv()

DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")


def get_repos(file_path: str) -> list:
    """
    Find repo names in markdown files
    """
    content = Path(file_path).read_text()
    return re.findall(r"\[(.+?)\]", content)


def docker_login(username: str, password: str):
    """
    Login to the Docker Hub
    """
    child = pexpect.spawn("hub-tool login")
    child.expect("Username:")
    child.sendline(username)
    child.expect("Password:")
    child.sendline(password)
    child.expect("Login Succeeded", timeout=10)


def list_updated_tags(repository: str, days: int = 7):
    """
    List all tags in repo and filter results by date
    """
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
        if hub_tool.stdout:
            if hub_tool.stdout != "null\n":
                for tag in json.loads(hub_tool.stdout):
                    tag_last_updated = tag["LastUpdated"]
                    tag_last_updated_dt = parser.parse(tag_last_updated).replace(
                        tzinfo=None
                    )
                    if tag_last_updated_dt > datetime.now() - timedelta(days=days):
                        tag_name = tag["Name"]
                        if not any(platform in tag_name for platform in ["arm32", "arm64"]):
                            print(tag_name, "-", tag_last_updated)
            else:
                logger.error("%s: repo not found on docker hub", repository)
        else:
            logger.error("%s: something bad happened", repository)
        print("")
    except subprocess.CalledProcessError as e:
        print(e.stderr)


def main():
    docker_login(DOCKER_USERNAME, DOCKER_PASSWORD)
    repos = get_repos("roles/homelab_svc/spnas/README.md")
    for repo in repos:
        list_updated_tags(repo)


if __name__ == "__main__":
    __version__ = "0.0.1"
    logging.basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(name)s:%(lineno)s:%(funcName)20s()] --- %(message)s",
        level=logging.DEBUG,
    )

    main()
