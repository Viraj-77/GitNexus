"""
GitHub Client Module
Handles all GitHub API interactions using PyGithub
"""

import os
from github import Github, GithubException
from typing import Dict, List, Optional


class GitHubClient:
    """GitHub API client wrapper for automation tasks"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client with access token
        
        Args:
            token: GitHub Personal Access Token (if None, reads from GITHUB_TOKEN env var)
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token not provided. Set GITHUB_TOKEN environment variable.")
        
        self.github = Github(self.token)
        self.user = self.github.get_user()
    
    def create_repo(self, name: str, private: bool = False, description: str = "") -> Dict:
        """
        Create a new GitHub repository
        
        Args:
            name: Repository name
            private: Whether repo should be private (default: False for public)
            description: Repository description
            
        Returns:
            Dict with keys: name, url, private
        """
        try:
            repo = self.user.create_repo(
                name=name,
                private=private,
                description=description,
                auto_init=True  # Initialize with README
            )
            return {
                "name": repo.name,
                "url": repo.html_url,
                "private": repo.private,
                "description": repo.description
            }
        except GithubException as e:
            raise Exception(f"Failed to create repository: {e.data.get('message', str(e))}")
    
    def list_repos(self) -> List[Dict]:
        """
        List all repositories for the authenticated user
        
        Returns:
            List of dicts with keys: name, url, private
        """
        try:
            repos = self.user.get_repos()
            return [
                {
                    "name": repo.name,
                    "url": repo.html_url,
                    "private": repo.private,
                    "description": repo.description or ""
                }
                for repo in repos
            ]
        except GithubException as e:
            raise Exception(f"Failed to list repositories: {e.data.get('message', str(e))}")
    
    def create_issue(self, repo_full_name: str, title: str, body: str = "") -> Dict:
        """
        Create an issue in a repository
        
        Args:
            repo_full_name: Full repository name (e.g., "username/repo")
            title: Issue title
            body: Issue body/description
            
        Returns:
            Dict with keys: number, url, title, state
        """
        try:
            self._validate_repo_name(repo_full_name)
            repo = self.github.get_repo(repo_full_name)
            issue = repo.create_issue(title=title, body=body)
            return {
                "number": issue.number,
                "url": issue.html_url,
                "title": issue.title,
                "state": issue.state
            }
        except GithubException as e:
            raise Exception(f"Failed to create issue: {e.data.get('message', str(e))}")
    
    def list_issues(self, repo_full_name: str, state: str = "open") -> List[Dict]:
        """
        List issues in a repository
        
        Args:
            repo_full_name: Full repository name (e.g., "username/repo")
            state: Issue state filter ("open", "closed", or "all")
            
        Returns:
            List of dicts with keys: number, title, url, state
        """
        try:
            self._validate_repo_name(repo_full_name)
            repo = self.github.get_repo(repo_full_name)
            issues = repo.get_issues(state=state)
            return [
                {
                    "number": issue.number,
                    "title": issue.title,
                    "url": issue.html_url,
                    "state": issue.state
                }
                for issue in issues
            ]
        except GithubException as e:
            raise Exception(f"Failed to list issues: {e.data.get('message', str(e))}")
    
    def commit_file(self, repo_full_name: str, path: str, content: str, message: str) -> Dict:
        """
        Create or update a file in a repository
        
        Args:
            repo_full_name: Full repository name (e.g., "username/repo")
            path: File path in repository
            content: File content
            message: Commit message
            
        Returns:
            Dict with keys: commit_sha, url, action (created/updated)
        """
        try:
            self._validate_repo_name(repo_full_name)
            repo = self.github.get_repo(repo_full_name)
            
            # Check if file exists
            try:
                existing_file = repo.get_contents(path)
                # File exists, update it
                result = repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=existing_file.sha
                )
                action = "updated"
            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, create it
                    result = repo.create_file(
                        path=path,
                        message=message,
                        content=content
                    )
                    action = "created"
                else:
                    raise
            
            return {
                "commit_sha": result["commit"].sha,
                "url": result["content"].html_url,
                "action": action,
                "path": path
            }
        except GithubException as e:
            raise Exception(f"Failed to commit file: {e.data.get('message', str(e))}")
    
    def read_file(self, repo_full_name: str, path: str) -> Dict:
        """
        Read a file from a repository
        
        Args:
            repo_full_name: Full repository name (e.g., "username/repo")
            path: File path in repository
            
        Returns:
            Dict with keys: path, content, url
        """
        try:
            self._validate_repo_name(repo_full_name)
            repo = self.github.get_repo(repo_full_name)
            file_content = repo.get_contents(path)
            
            return {
                "path": file_content.path,
                "content": file_content.decoded_content.decode('utf-8'),
                "url": file_content.html_url,
                "size": file_content.size
            }
        except GithubException as e:
            if e.status == 404:
                raise Exception(f"File not found: {path}")
            raise Exception(f"Failed to read file: {e.data.get('message', str(e))}")
    
    @staticmethod
    def _validate_repo_name(repo_full_name: str):
        """
        Validate repository full name format
        
        Args:
            repo_full_name: Full repository name to validate
            
        Raises:
            ValueError: If format is invalid
        """
        if not repo_full_name or "/" not in repo_full_name:
            raise ValueError(
                "Invalid repository name. Must be in format 'username/repo'"
            )
        
        parts = repo_full_name.split("/")
        if len(parts) != 2 or not all(parts):
            raise ValueError(
                "Invalid repository name. Must be in format 'username/repo'"
            )
