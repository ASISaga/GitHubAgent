from github import Github, Auth
import os
from config import GITHUB_ACCESS_TOKEN_ENV, GITHUB_ENTERPRISE_BASE_URL, DEFAULT_BASE_URL

class GitHubClient:
    def __init__(self, access_token=None, base_url=None):
        """
        Initialize the GitHubClient with an access token and base URL.

        :param access_token: Optional GitHub access token. If not provided, it will be fetched from the environment variable.
        :param base_url: Optional base URL for GitHub API. Defaults to the enterprise base URL or the public GitHub API URL.
        """
        # Use the provided access token or fetch it from the environment variable.
        self.access_token = access_token or os.getenv(GITHUB_ACCESS_TOKEN_ENV)
        if not self.access_token:
            # Raise an error if the access token is not provided or not set in the environment.
            raise ValueError(f"{GITHUB_ACCESS_TOKEN_ENV} environment variable is not set")
        
        # Use the provided base URL or fetch it from the environment variable. Default to the public GitHub API URL.
        self.base_url = base_url or os.getenv(GITHUB_ENTERPRISE_BASE_URL, DEFAULT_BASE_URL)
        
        # Authenticate using the provided or fetched access token.
        self.auth = Auth.Token(self.access_token)
        
        # Initialize the PyGithub client with the base URL and authentication.
        self.github = Github(base_url=self.base_url, auth=self.auth)

    def get_authenticated_user(self):
        """
        Retrieve the authenticated user.

        :return: Authenticated user object.
        :raises: Exception if there is an error during the API call.
        """
        try:
            # Fetch and return the authenticated user using the PyGithub client.
            return self.github.get_user()
        except Exception as error:
            # Print and re-raise the error if the API call fails.
            print("Error retrieving authenticated user:", error)
            raise

    def list_repositories(self, per_page=30):
        """
        List repositories of the authenticated user.

        :param per_page: Number of repositories to fetch per page. Defaults to 30.
        :return: A paginated list of repositories.
        :raises: Exception if there is an error during the API call.
        """
        try:
            # Retrieve the authenticated user.
            user = self.get_authenticated_user()
            # Fetch and return the repositories of the authenticated user.
            return user.get_repos(per_page=per_page)
        except Exception as error:
            # Print and re-raise the error if the API call fails.
            print("Error listing repositories:", error)
            raise

    def close_connection(self):
        """
        Close the GitHub connection.

        Note: PyGithub does not require explicit connection closure, but this method is provided for future extensibility.
        """
        self.github.close()

# Example usage:
if __name__ == "__main__":
    # Create an instance of GitHubClient.
    client = GitHubClient()
    try:
        # List repositories of the authenticated user.
        repos = client.list_repositories()
        # Print the name of each repository.
        for repo in repos:
            print(repo.name)
    finally:
        # Ensure the connection is closed after use.
        client.close_connection()