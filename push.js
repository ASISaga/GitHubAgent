import { Octokit } from "@octokit/rest";

// GitHubAgent class to handle GitHub operations
class GitHubAgent {
  // Constructor to initialize the Octokit client and repository details
  constructor(authToken, owner, repo, branch) {
    this.octokit = new Octokit({ auth: authToken });
    this.owner = owner;
    this.repo = repo;
    this.branch = branch;
  }

  // Method to get the reference (SHA) of the branch
  async getBranchRef() {
    try {
      const { data: refData } = await this.octokit.git.getRef({
        owner: this.owner,
        repo: this.repo,
        ref: `heads/${this.branch}`,
      });
      return refData.object.sha;
    } catch (error) {
      console.error("Error getting branch reference:", error);
      throw error;
    }
  }

  // Method to get the commit data for a given SHA
  async getCommit(sha) {
    try {
      const { data: commitData } = await this.octokit.git.getCommit({
        owner: this.owner,
        repo: this.repo,
        commit_sha: sha,
      });
      return commitData;
    } catch (error) {
      console.error("Error getting commit data:", error);
      throw error;
    }
  }

  // Method to create a blob (binary large object) for the file content
  async createBlob(content) {
    try {
      const fileContentInBase64 = Buffer.from(content).toString("base64");
      const { data: blobData } = await this.octokit.git.createBlob({
        owner: this.owner,
        repo: this.repo,
        content: fileContentInBase64,
        encoding: "base64",
      });
      return blobData.sha;
    } catch (error) {
      console.error("Error creating blob:", error);
      throw error;
    }
  }

  // Method to create a tree object that includes the new blob
  async createTree(baseTreeSha, blobSha, filePath) {
    try {
      const { data: treeData } = await this.octokit.git.createTree({
        owner: this.owner,
        repo: this.repo,
        base_tree: baseTreeSha,
        tree: [
          {
            path: filePath,
            mode: "100644",
            type: "blob",
            sha: blobSha,
          },
        ],
      });
      return treeData.sha;
    } catch (error) {
      console.error("Error creating tree:", error);
      throw error;
    }
  }

  // Method to create a new commit with the new tree
  async createCommit(message, treeSha, parentSha) {
    try {
      const { data: newCommitData } = await this.octokit.git.createCommit({
        owner: this.owner,
        repo: this.repo,
        message: message,
        tree: treeSha,
        parents: [parentSha],
      });
      return newCommitData.sha;
    } catch (error) {
      console.error("Error creating commit:", error);
      throw error;
    }
  }

  // Method to update the branch reference to point to the new commit
  async updateBranchRef(newCommitSha) {
    try {
      await this.octokit.git.updateRef({
        owner: this.owner,
        repo: this.repo,
        ref: `heads/${this.branch}`,
        sha: newCommitSha,
      });
    } catch (error) {
      console.error("Error updating branch reference:", error);
      throw error;
    }
  }

  // Method to push a file to the repository
  async pushFile(filePath, fileContent, commitMessage) {
    try {
      // Get the latest commit SHA of the branch
      const latestCommitSha = await this.getBranchRef();
      // Get the latest commit data
      const latestCommit = await this.getCommit(latestCommitSha);
      // Get the base tree SHA of the latest commit
      const baseTreeSha = latestCommit.tree.sha;
      // Create a blob for the file content
      const blobSha = await this.createBlob(fileContent);
      // Create a new tree that includes the new blob
      const newTreeSha = await this.createTree(baseTreeSha, blobSha, filePath);
      // Create a new commit with the new tree
      const newCommitSha = await this.createCommit(commitMessage, newTreeSha, latestCommitSha);
      // Update the branch reference to point to the new commit
      await this.updateBranchRef(newCommitSha);
    } catch (error) {
      console.error("Error pushing file:", error);
      throw error;
    }
  }
}

export default GitHubAgent;
