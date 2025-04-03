from github import Github, Auth
from config import DEFAULT_BASE_URL

class GitHubClient:
    """
    A client for interacting with the GitHub API using PyGithub.

    This class provides methods to authenticate with GitHub, retrieve user information,
    and list repositories. It uses an access token for authentication and supports
    both the public GitHub API and GitHub Enterprise instances.
    """

    def __init__(self, access_token, base_url, repo_name):
        """
        Initialize the GitHubClient with an access token and base URL.

        :param access_token: GitHub access token. This is required for authentication.
        :param base_url: Base URL for GitHub API. Defaults to the public GitHub API if not provided.
        """
        # Use the provided access token.
        self.access_token = access_token
        if not self.access_token:
            # Raise an error if the access token is not provided.
            raise ValueError("Access token is required")
        
        # Use the provided base URL or default to the public GitHub API URL.
        self.base_url = base_url or DEFAULT_BASE_URL
        
        # Authenticate using the provided access token.
        self.auth = Auth.Token(self.access_token)
        
        # Initialize the PyGithub client with the base URL and authentication.
        self.github = Github(base_url=self.base_url, auth=self.auth)

        self.repo = self.getRepository(repo_name=repo_name)
        # Initialize the repository object using the provided repository name.

    def getAuthenticatedUser(self):
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

    def listRepositories(self, per_page=30):
        """
        List repositories of the authenticated user.

        :param per_page: Number of repositories to fetch per page. Defaults to 30.
        :return: A paginated list of repositories.
        :raises: Exception if there is an error during the API call.
        """
        try:
            # Retrieve the authenticated user.
            user = self.getAuthenticatedUser()
            # Fetch and return the repositories of the authenticated user.
            return user.get_repos(per_page=per_page)
        except Exception as error:
            # Print and re-raise the error if the API call fails.
            print("Error listing repositories:", error)
            raise

    def getRepository(self, repo_name):
        """
        Retrieve a specific repository by name.

        :param repo_name: Name of the repository to retrieve.
        :return: Repository object.
        :raises: Exception if there is an error during the API call.
        """
        try:
            # Fetch and return the specified repository using the PyGithub client.
            self.repo = self.github.get_repo(repo_name)
        except Exception as error:
            # Print and re-raise the error if the API call fails.
            print("Error retrieving repository:", error)
            raise

    def pushCommit(self, commit_message, file_path, content):
        """
        Push a commit to a specified repository.
        Using PyGitHub, you don't "push" changes in the same way as you would with Git on your local machine (i.e., using a  command).
        Instead, you interact directly with the GitHub API to commit changes. When you create or update a file using PyGitHub methods,
        GitHub creates a commit in your repository. 
        
        :param commit_message: Commit message for the push.
        :param file_path: Path of the file to be committed.
        :param content: Content of the file to be committed.
        :raises: Exception if there is an error during the API call.
        """
        try:
            # If the file exists, update it. This call creates a commit on your specified branch.
            self.repo.update_file(file_path, commit_message, content, content.sha, branch="main")
            print(f"Updated {file_path} successfully.")

            # Create or update the file in the repository with the provided content.
        except Exception as error:
            try:
                # If the file does not exist, create it instead.
                self.repo.create_file(file_path, commit_message, content)
                print(f"Created {file_path} successfully.")
            except Exception as error:
                # Print and re-raise the error if the API call fails.
                print("Error pushing commit:", error)
                raise

    def closeConnection(self):
        """
        Close the GitHub connection.

        Note: PyGithub does not require explicit connection closure, but this method is provided for future extensibility.
        """
        self.github.close()