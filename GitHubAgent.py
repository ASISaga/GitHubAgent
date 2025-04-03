import os
from GitHubClient import GitHubClient
from config import GITHUB_ACCESS_TOKEN_ENV, GITHUB_ENTERPRISE_BASE_URL

if __name__ == "__main__":
    # Fetch environment variables for access token and base URL.
    access_token = os.getenv(GITHUB_ACCESS_TOKEN_ENV)
    base_url = os.getenv(GITHUB_ENTERPRISE_BASE_URL)

    # Create an instance of GitHubClient with the fetched parameters.
    client = GitHubClient(access_token=access_token, base_url=base_url)
    try:
        # List repositories of the authenticated user.
        repos = client.list_repositories()
        # Print the name of each repository.
        for repo in repos:
            print(repo.name)
    finally:
        # Ensure the connection is closed after use.
        client.close_connection()
