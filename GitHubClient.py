from github import Github, Auth
from config import DEFAULT_BASE_URL

class GitHubClient:
    def __init__(self, access_token, base_url):
        """
        Initialize the GitHubClient with an access token and base URL.

        :param access_token: GitHub access token.
        :param base_url: Base URL for GitHub API.
        """
        # Use the provided access token.
        self.access_token = access_token
        if not self.access_token:
            # Raise an error if the access token is not provided.
            raise ValueError("Access token is required")
        
        # Use the provided base URL.
        self.base_url = base_url or DEFAULT_BASE_URL
        
        # Authenticate using the provided access token.
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