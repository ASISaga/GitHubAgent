import os
from GitHubAgent import GitHubAgent
from config import GITHUB_ACCESS_TOKEN_ENV, GITHUB_ENTERPRISE_BASE_URL

if __name__ == "__main__":
    # Fetch environment variables for access token and base URL.
    access_token = os.getenv(GITHUB_ACCESS_TOKEN_ENV)
    base_url = os.getenv(GITHUB_ENTERPRISE_BASE_URL)

    # Instantiate GitHubAgent and execute its functionality.
    agent = GitHubAgent(access_token=access_token, base_url=base_url, repo_name="your-repo-name")
    agent.execute()
