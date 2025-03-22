import GitHubAgent from './push';

// Usage example
(async () => {
  const authToken = "your_personal_access_token"; // Your GitHub personal access token
  const owner = "your_github_username"; // Your GitHub username
  const repo = "your_repository_name"; // Your GitHub repository name
  const branch = "branch_name"; // The branch name where you want to push the file
  const filePath = "path/to/your/file.txt"; // The path to the file in the repository
  const fileContent = "Hello World!"; // The content of the file
  const commitMessage = "Your commit message"; // The commit message

  // Create an instance of GitHubAgent
  const agent = new GitHubAgent(authToken, owner, repo, branch);
  // Push the file to the repository
  await agent.pushFile(filePath, fileContent, commitMessage);
})();