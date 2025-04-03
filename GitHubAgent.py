from GitHubClient import GitHubClient
from PurposeDrivenAgent.CoderAgent import CoderAgent

class GitHubAgent(CoderAgent):
    def __init__(self, access_token, base_url, repo_name):
        """
        Initialize the GitHubAgent with the required parameters.

        :param access_token: GitHub access token for authentication.
        :param base_url: Base URL for GitHub or GitHub Enterprise.
        :param repo_name: Name of the repository to interact with.
        """
        super().__init__()  # Call the base class constructor
        self.access_token = access_token
        self.base_url = base_url
        self.repo_name = repo_name

    def execute(self):
        """
        Execute the main functionality of the GitHubAgent.
        Lists repositories of the authenticated user and prints their names.
        """
        # Create an instance of GitHubClient with the fetched parameters.
        client = GitHubClient(access_token=self.access_token, base_url=self.base_url, repo_name=self.repo_name)
        try:
            # List repositories of the authenticated user.
            repos = client.listRepositories()
            
            # Print the name of each repository.
            for repo in repos:
                print(repo.name)
        finally:
            # Ensure the connection is closed after use.
            client.closeConnection()
