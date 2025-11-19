# --- DEPENDENCIES ---
# 1. System Dependencies (MacOS/Linux):
#    brew install python3
#
# 2. Set virtual environment:
#    python3 -m venv .venv
#    source .venv/bin/activate

# 3. Install dependencies:
#    pip install agno google-generativeai PyGithub
#
# 4. Create GitHub Personal Access Token with required permissions:
#    - Go to: https://github.com/settings/tokens
#    - For Classic Token: Select "repo" scope (or "public_repo" for public repos only)
#    - For Fine-grained Token: Set "Issues" and "Pull requests" to "Read and write"
#
# 5. Set environment variables:
#    export GOOGLE_API_KEY=your-google-api-key
#    export GITHUB_ACCESS_TOKEN=your-github-access-token
#    export REPO_NAME=your-username/your-repo-name
#
# --------------------

import os
from agno.agent import Agent
from agno.models.google import Gemini

# Import the OFFICIAL Agno GitHub Tool
try:
    from agno.tools.github import GithubTools
except ImportError:
    raise ImportError("Could not import GithubTools. Please install agno with: pip install agno")

# --- CONFIGURATION ---
# Ensure these are set in your environment or replace with actual values
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
REPO_NAME = os.getenv("REPO_NAME", "your-username/your-repo-name") # e.g. "agno-agi/agno"

if not GOOGLE_API_KEY:
    print("⚠️  WARNING: GOOGLE_API_KEY is not set. The agent will fail to connect to Gemini.")

if not GITHUB_ACCESS_TOKEN:
    print("⚠️  WARNING: GITHUB_ACCESS_TOKEN is not set. The agent will fail to authenticate with GitHub.")

# --- DEFINE THE AGENT ---
# Heuristic-based PR labeling system for beginner-friendly contributions

# Instructions based on Stage 1 Heuristic Rules
agent_instructions = [
    "You are an autonomous GitHub PR Analysis Agent.",
    f"You are working with the repository: {REPO_NAME}",
    "Your goal is to analyze Pull Requests and label them 'beginner-friendly' based on heuristic rules.",
    "",
    "## STEP 1: GET PR DETAILS",
    "Use `get_pull_request_with_details` to fetch comprehensive PR data.",
    "- Pass parameters: repo_name (the repository name) and pr_number (the PR number).",
    "",
    "## STEP 2: GET CODE CHANGES",
    "Use `get_pull_request_changes` to fetch the actual code diff/changes.",
    "- Pass parameters: repo_name and pr_number.",
    "- This will show you the exact lines of code that were added, removed, or modified.",
    "",
    "## STEP 3: GUARD CLAUSES - Skip if:",
    "- The PR has `draft: true`",
    "- The title starts with 'WIP' or 'wip' (case-insensitive)",
    "If either condition is true, output 'PR is not ready for analysis. Skipping.' and STOP.",
    "",
    "## STEP 4: CALCULATE HEURISTIC SCORE (Threshold: 65 points)",
    "Calculate points based on these rules:",
    "",
    "### Lines of Code (LoC):",
    "- If (additions + deletions) ≤ 10: +40 points (reason: 'Tiny change')",
    "- Else if (additions + deletions) ≤ 40: +20 points (reason: 'Small change')",
    "",
    "### Number of Files:",
    "- If changed_files ≤ 2: +20 points (reason: 'Focused change')",
    "",
    "### Bot Authors:",
    "- If author/user contains 'dependabot' or 'renovate': +25 points (reason: 'Dependency update')",
    "",
    "### Commit Count:",
    "- If commits < 2: +20 points (reason: 'Single commit')",
    "",
    "### Documentation Keyword:",
    "- If 'docs' appears in title OR body (case-insensitive): +20 points (reason: 'Documentation change')",
    "",
    "### Cherry-Pick Keyword:",
    "- If 'cherry-pick' or 'cherry pick' appears in title OR body: +15 points (reason: 'Cherry-picked change')",
    "",
    "## STEP 5: DECISION & ACTION",
    "- If score < 65: Output the score and reasons, then say 'Score below threshold. Not suitable for beginner-friendly label.'",
    "- If score ≥ 65:",
    "  1. Use `label_issue` to add the label 'beginner-friendly'.",
    "     - Pass parameters: repo_name, issue_number (same as PR number), and labels=['beginner-friendly'].",
    "  2. IMMEDIATELY use `create_pull_request_comment` to post a helpful comment.",
    "     - Pass parameters: repo_name, pr_number, and body (the comment text).",
    "",
    "## STEP 6: CREATE HELPFUL COMMENT (only if score ≥ 65)",
    "First, use `get_repository` to fetch repository details (description, topics, language, README info) for project context.",
    "Then analyze the PR details AND code changes to create a professional, informative comment with this structure:",
    "",
    "## Beginner-Friendly PR",
    "",
    "This pull request has been automatically labeled as `beginner-friendly` based on its characteristics.",
    "",
    "### Summary",
    "[Provide a clear, concise summary of what this PR changes based on the title, description, and files modified]",
    "",
    "### Project Context",
    "[Use repository information to explain:",
    "- What this project is and its main purpose",
    "- What technology stack is being used (from repo languages/topics)",
    "- How this change fits into the bigger picture of the project",
    "- Which part of the codebase/architecture this touches]",
    "",
    "### Technical Details",
    "[Analyze the changed files and provide:",
    "- Key files modified and their purpose in the project",
    "- Technologies/frameworks involved in these files",
    "- Any important patterns or conventions being followed",
    "- Dependencies or related components affected]",
    "",
    "### Code Changes Analysis",
    "[Deep dive into the actual code changes from the diff:",
    "- What specific code was added, removed, or modified",
    "- The purpose of each significant change",
    "- Why these changes were made (based on PR description and code context)",
    "- What functions, classes, or components were affected",
    "- Any new dependencies, imports, or configurations introduced",
    "- How the changes relate to each other (if multiple files)",
    "- Potential impact or side effects of these changes]",
    "",
    "### Why This is Beginner-Friendly",
    "[List the objective scoring criteria that were met:",
    "- Change size: X additions, Y deletions",
    "- Number of files: Z",
    "- Other factors that contributed to the score]",
    "",
    "### Review Checklist",
    "[Provide specific, actionable review items based on the actual changes:",
    "- Item 1 relevant to the files changed",
    "- Item 2 relevant to the type of change",
    "- Item 3 about testing/documentation if applicable]",
    "",
    "### Additional Resources",
    "[If available, provide:",
    "- Links to relevant documentation (if docs exist in repo)",
    "- Related files or modules in the codebase",
    "- Contributing guidelines if mentioned in repository]",
    "",
    "---",
    "*This label was added automatically. Maintainers can remove it if they disagree.*",
    "",
    "## STEP 7: OUTPUT",
    "Summarize: the score, which rules were triggered, the final decision, and confirm the comment was posted."
]

# Initialize PR Analysis Agent
pr_agent = Agent(
    name="PR Analysis Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[GithubTools(access_token=GITHUB_ACCESS_TOKEN)],
    instructions=agent_instructions,
    debug_mode=True,
    markdown=True,
)

# --- RUN ---

if __name__ == "__main__":
    print(f"PR Analysis Agent - Repository: {REPO_NAME}")
    
    # Interactive prompt to test on a real PR
    pr_number = input("Enter PR number to analyze: ")
    
    if pr_number:
        print(f"\nAnalyzing PR #{pr_number}...")
        pr_agent.print_response(f"Analyze PR #{pr_number} in repository {REPO_NAME}", stream=True)
    else:
        print("No PR number entered. Exiting.")