import os

from github import Github
import requests


class GiteaSettings:
    def __init__(self, gitea_token: str, gitea_owner: str, gitea_api_url: str, gitea_api_ssl: bool = True) -> None:
        self.token = gitea_token
        self.owner = gitea_owner
        self.api_url = gitea_api_url
        self.api_ssl = gitea_api_ssl
        self.api_migrate_url = f"{self.api_url}/repos/migrate"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"token {self.token}",
        }


class GitHubSettings:
    def __init__(self, github_pat: str, github_organization: str, gitea_conf: GiteaSettings) -> None:
        self.pat = github_pat
        self.gitea_conf = gitea_conf
        self.org = github_organization

    def get_repos(self) -> dict:
        g = Github(self.pat)
        organization = g.get_organization(self.org)
        repos = organization.get_repos(type="all")
        return repos

    def mirror(self, payload: dict) -> None:
        requests.post(
            url=self.gitea_conf.api_migrate_url,
            headers=self.gitea_conf.headers,
            verify=self.gitea_conf.api_ssl,
            json=payload,
        )

    def get_payload(self, repo) -> dict:
        payload = {
            "service": "github",
            "auth_token": self.pat,
            "clone_addr": f"https://github.com/{self.org}/{repo.name}",
            "mirror": True,
            "private": repo.private,
            "repo_name": repo.name,
            "repo_owner": self.gitea_conf.owner,
        }
        return payload

    def mirror_repos(self):
        for repo in self.get_repos():
            payload = self.get_payload(repo)
            self.mirror(payload=payload)


# Gitea configuration
gitea_conf = GiteaSettings(
    gitea_token=os.environ.get("GITEA_TOKEN", ""),
    gitea_owner=os.environ.get("GITEA_OWNER", "osism"),
    gitea_api_url=os.environ.get("GITEA_API_URL", "https://gitea.services.osism.tech/api/v1"),
    gitea_api_ssl=os.environ.get("GITEA_API_SSL", True),
)

# GitHub mirroring
github_handle = GitHubSettings(
    github_pat=os.environ.get("GITHUB_PAT", ""),
    github_organization=os.environ.get("GITHUB_ORGANIZATION", "osism"),
    gitea_conf=gitea_conf,
)
github_handle.mirror_repos()
