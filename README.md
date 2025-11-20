# 🎩 The Sorting Hat - AI-Powered PR Analysis Agent

An autonomous AI agent that automatically analyzes GitHub Pull Requests and labels them as "beginner-friendly" based on intelligent heuristic scoring. When you point it at a PR, the Sorting Hat evaluates complexity, provides detailed code analysis, identifies potential issues, and helps maintainers understand what makes a PR suitable for new contributors.

## 🎯 What Does It Do?

The Sorting Hat follows a comprehensive workflow to evaluate and label PRs:

1. **Fetches PR Details** - Retrieves complete PR information including metadata, author, title, and description
2. **Analyzes Code Changes** - Examines the actual code diff to understand what was modified
3. **Searches Related Work** - Finds similar PRs and issues to provide helpful context
4. **Calculates Heuristic Score** - Uses multiple criteria to determine if the PR is beginner-friendly (threshold: 65 points)
5. **Performs Code Review** - Critically analyzes the code for bugs, security issues, edge cases, and quality problems
6. **Labels the PR** - Automatically adds the "beginner-friendly" label if score ≥ 65
7. **Posts Comprehensive Comment** - Creates a detailed analysis with project context, technical details, potential issues, review checklist, and related work

## 🏆 Scoring System

The agent uses a points-based heuristic system (threshold: 65 points):

| Criteria | Points | Description |
|----------|--------|-------------|
| **Tiny Change** | +40 | ≤10 lines of code changed |
| **Small Change** | +20 | ≤40 lines of code changed |
| **Focused Change** | +20 | ≤2 files modified |
| **Dependency Update** | +25 | Author is dependabot/renovate |
| **Single Commit** | +20 | Less than 2 commits |
| **Documentation** | +20 | "docs" keyword in title/body |
| **Cherry-Pick** | +15 | "cherry-pick" keyword in title/body |

## 🚀 Quick Start

### Prerequisites

* Python 3.8 or higher
* A GitHub account with a Personal Access Token
* A Google API key (for Gemini AI)

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd the-sorting-hat
```

2. **Set up virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install agno google-generativeai PyGithub
```

### Configuration

#### 1. Create a GitHub Personal Access Token

Go to [GitHub Settings > Tokens](https://github.com/settings/tokens) and create a token with:

* **Classic Token**: Select `repo` scope (or `public_repo` for public repos only)
* **Fine-grained Token**: Set "Issues" and "Pull requests" to "Read and write"

#### 2. Get a Google API Key

Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create an API key for Gemini.

#### 3. Set Environment Variables

```bash
export GOOGLE_API_KEY="your-google-api-key"
export GITHUB_ACCESS_TOKEN="your-github-access-token"
export REPO_NAME="username/repository-name"
```

Or create a `.env` file:

```env
GOOGLE_API_KEY=your-google-api-key
GITHUB_ACCESS_TOKEN=your-github-access-token
REPO_NAME=username/repository-name
```

## 📖 Usage

### Interactive Mode

Run the agent and enter a PR number when prompted:

```bash
python main.py
```

```
PR Analysis Agent - Repository: username/repo-name

Enter PR number to analyze: 42

Analyzing PR #42...
```

### Example Workflow

Let's say PR #42 is a small documentation fix with 15 lines changed in 1 file:

**Scoring Breakdown:**
- Small change (≤40 lines): +20 points
- Focused change (≤2 files): +20 points
- Documentation keyword in title: +20 points
- Single commit: +20 points
- **Total: 80 points** ✅ (threshold: 65)

**Agent Actions:**
1. ✅ Adds "beginner-friendly" label to PR #42
2. 📝 Posts comprehensive analysis comment (see example below)

## 🛠️ How It Works

The agent uses:

- **Agno Framework** - For building autonomous AI agents
- **Google Gemini 2.0 Flash** - Advanced AI model for code analysis and natural language understanding
- **GitHub Tools** - Official GitHub integration for fetching PRs, posting comments, and managing labels

### Agent Workflow

```
PR Number Provided
        ↓
Get PR Details & Metadata
        ↓
Get Code Changes (Diff)
        ↓
Search Related Issues/PRs
        ↓
Guard Clauses Check
(Draft or WIP?) → Yes → Stop
        ↓ No
Calculate Heuristic Score
        ↓
Score < 65? → Yes → Report & Stop
        ↓ No (Score ≥ 65)
Add "beginner-friendly" Label
        ↓
Get Repository Context
        ↓
Analyze Code for Issues
        ↓
Post Comprehensive Comment
        ↓
Done ✓
```

## 🎨 Features

- ✅ **Objective Scoring** - Heuristic-based evaluation for consistent labeling
- ✅ **Deep Code Analysis** - Identifies bugs, security issues, edge cases, and code quality problems
- ✅ **Context-Aware** - Fetches repository details to understand the bigger picture
- ✅ **Related Work Discovery** - Finds similar PRs and issues for helpful context
- ✅ **Critical Review** - Questions assumptions and looks for what could go wrong
- ✅ **Automated Labeling** - Adds labels and comments automatically
- ✅ **Guard Clauses** - Skips draft PRs and WIP changes
- ✅ **Actionable Feedback** - Provides specific review checklists based on actual changes

## 📝 Example Output

When the agent analyzes a PR with score ≥ 65, it posts a detailed comment like:

```markdown
## Beginner-Friendly PR

This pull request has been automatically labeled as `beginner-friendly` based on its characteristics.

### Summary
This PR updates the installation documentation to include clearer instructions for setting up the development environment.

### Project Context
This project is a Python-based web application using Flask and SQLAlchemy. The change affects the documentation which helps new contributors get started with the project. This touches the developer onboarding experience, which is critical for open-source contributions.

### Technical Details
**Key files modified:**
- `docs/installation.md` - Main installation guide
- Located in the documentation directory
- Uses Markdown formatting
- Part of the user-facing documentation

### Code Changes Analysis
**Changes made:**
- Added 3 lines explaining prerequisite software
- Removed 2 outdated references to Python 2.7
- Modified the virtual environment setup command to be more explicit
- Added a troubleshooting section with 5 common issues

The changes are purely documentation-focused with no code logic modifications.

### Potential Issues to Watch For
**Documentation Quality:**
- Verify that all commands are tested and work on different platforms (macOS, Linux, Windows)
- Check that links are not broken
- Ensure formatting renders correctly in GitHub's markdown viewer

**Edge Cases:**
- Users with Python 2.7 still installed might get confused
- Windows users might need different commands

No obvious bugs or security issues detected since this is documentation only.

### Why This is Beginner-Friendly
- **Change size:** 15 additions, 12 deletions (Small change: +20 points)
- **Number of files:** 1 file (Focused change: +20 points)
- **Documentation change:** "docs" in title (+20 points)
- **Single commit:** Only 1 commit (+20 points)
- **Total Score:** 80 points (Threshold: 65)

### Review Checklist
- [ ] Verify all installation commands work on macOS
- [ ] Test commands on Linux
- [ ] Check that Windows users have alternative instructions
- [ ] Ensure all links are valid
- [ ] Confirm formatting displays correctly
- [ ] Verify Python version requirements match package.json/requirements.txt

### Related Work
You might find these helpful:
- #38 - Similar documentation update to README.md
- #12 - Discussion about improving contributor onboarding
- #67 - Fixed broken installation instructions

Previous documentation PRs typically also updated the contributing guide when installation steps changed.

### Additional Resources
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Development Setup Guide](../docs/development.md)

---
*This label was added automatically. Maintainers can remove it if they disagree.*
```

## 🔧 Customization

You can customize the agent's behavior by modifying the `agent_instructions` list in `main.py`:

### Adjust Scoring Thresholds

Change the point values to make labeling more or less strict:

```python
# Make it stricter (higher bar)
"- If (additions + deletions) ≤ 10: +30 points",  # Was +40

# Make it more lenient (lower bar)
"## STEP 5: CALCULATE HEURISTIC SCORE (Threshold: 50 points)",  # Was 65
```

### Add Custom Criteria

Add your own scoring rules:

```python
"### Bug Fix Keyword:",
"- If 'fix' or 'bug' appears in title: +15 points (reason: 'Bug fix')",
```

### Customize Comment Format

Modify the comment structure in STEP 7 to match your project's needs:

```python
"### Summary",
"[Add your custom sections here]",
```

### Change AI Model

Switch to a different Gemini model:

```python
pr_agent = Agent(
    name="PR Analysis Agent",
    model=Gemini(id="gemini-1.5-pro"),  # More powerful but slower
    # ...
)
```

## 🤖 Guard Clauses

The agent automatically skips PRs that are:

- **Draft PRs** - PRs with `draft: true`
- **Work in Progress** - Title starts with "WIP" or "wip" (case-insensitive)

This prevents premature labeling and respects contributor workflows.

## 💡 Use Cases

### For Maintainers
- **Automate PR Triage** - Quickly identify PRs suitable for first-time contributors
- **Scale Code Review** - Get detailed analysis of potential issues before human review
- **Improve Onboarding** - Provide comprehensive context to help reviewers understand changes

### For Contributors
- **Learn from Analysis** - Understand what makes PRs beginner-friendly
- **Get Quick Feedback** - Receive detailed code review comments automatically
- **Discover Related Work** - Find similar PRs and issues for context

### For Open Source Projects
- **Encourage Contributions** - Make it easy to identify beginner-friendly issues
- **Maintain Quality** - Automated checks for bugs, security, and code quality
- **Build Community** - Help new contributors succeed with detailed guidance

## 🐛 Troubleshooting

### "GOOGLE_API_KEY is not set"

Make sure you've exported the environment variable:

```bash
export GOOGLE_API_KEY="your-actual-api-key"
```

### "GITHUB_ACCESS_TOKEN is not set"

Create a Personal Access Token and export it:

```bash
export GITHUB_ACCESS_TOKEN="your-github-token"
```

### "Could not import GithubTools"

Install the required packages:

```bash
pip install agno google-generativeai PyGithub
```

### Agent is labeling PRs incorrectly

Adjust the scoring thresholds or criteria in `agent_instructions` to better match your project's needs.

### Rate Limiting Issues

If you hit GitHub API rate limits:
- Use a GitHub App instead of Personal Access Token for higher limits
- Add delays between PR analyses
- Cache repository information

## 🎓 How It Helps New Contributors

The Sorting Hat doesn't just label PRs - it creates a learning experience:

1. **Transparent Criteria** - Shows exactly why a PR is beginner-friendly
2. **Educational Comments** - Explains project context and technical details
3. **Code Review Practice** - Points out potential issues to consider
4. **Related Resources** - Links to similar work and documentation
5. **Actionable Checklists** - Provides specific items to verify

## 🚀 Future Enhancements

Potential improvements (contributions welcome!):

- [ ] Machine learning model to supplement heuristics
- [ ] Support for multi-repo analysis
- [ ] Integration with Discord/Slack for notifications
- [ ] Historical tracking of labeled PRs
- [ ] Custom scoring profiles per repository
- [ ] Automated testing of PR suggestions
- [ ] Integration with CI/CD pipelines

## 🤝 Contributing

Contributions are welcome! Feel free to:

* Report bugs
* Suggest features
* Submit pull requests
* Improve documentation
* Share your scoring criteria

The Sorting Hat can analyze its own PRs! 🎩✨

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Built with:
- [Agno](https://github.com/agno-agi/agno) - AI Agent Framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) - Advanced AI Model
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API Wrapper

Inspired by the need to make open source contribution more accessible to beginners.

## 💬 Questions?

- **What if I disagree with the label?** - Maintainers can remove the label at any time. The agent adds a note that labels can be removed.
- **Does it work on private repos?** - Yes! Just ensure your GitHub token has access to private repositories.
- **Can I run it on multiple PRs?** - Currently it's interactive. You could modify the code to batch process or run as a webhook.
- **How accurate is the scoring?** - Heuristics work well but aren't perfect. You can tune the criteria for your project.

---

🎩 *The Sorting Hat: Sorting PRs, not students* ✨

Built with ❤️ using Agno and Google Gemini

