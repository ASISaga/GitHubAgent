import os
from GitHubClient import GitHubClient
from config import GITHUB_ACCESS_TOKEN_ENV, GITHUB_ENTERPRISE_BASE_URL

if __name__ == "__main__":
    # Fetch environment variables for access token and base URL.
    # The access token is required to authenticate with the GitHub API.
    # The base URL is optional and can be used to specify a custom GitHub Enterprise instance.
    access_token = os.getenv(GITHUB_ACCESS_TOKEN_ENV)
    base_url = os.getenv(GITHUB_ENTERPRISE_BASE_URL)

    # Create an instance of GitHubClient with the fetched parameters.
    # This initializes the client with the provided access token and base URL.
    client = GitHubClient(access_token=access_token, base_url=base_url)
    try:
        # List repositories of the authenticated user.
        # The listRepositories method fetches the repositories associated with the authenticated user.
        repos = client.listRepositories()
        
        # Print the name of each repository.
        # Iterate through the repositories and display their names in the console.
        for repo in repos:
            print(repo.name)
    finally:
        # Ensure the connection is closed after use.
        # Although PyGithub does not require explicit connection closure, this ensures proper cleanup.
        client.closeConnection()
