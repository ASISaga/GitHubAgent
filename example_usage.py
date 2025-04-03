from GitHubClient import GitHubClient

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
