---
title: GitNexus
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# 🚀 GitNexus

**MCP-Enabled GitHub Automation for AI Agents**

## 👥 Project Team

| Name | Hugging Face Profile |
|------|----------------------|
| **Viraj Talathi** | [@Viraj77](https://huggingface.co/Viraj77) |
| **Pranjal Prakash** | [@pranjal00](https://huggingface.co/pranjal00) |
| **Karan Singh** | [@karansingh99](https://huggingface.co/karansingh99) |
| **Shriprasasd Patil** | [@Shriprasad-P](https://huggingface.co/Shriprasad-P) |
| **Bharath Nuthalapati** | [@bharath-nuthalapati](https://huggingface.co/bharath-nuthalapati) |

This Hugging Face Space demonstrates GitHub automation using MCP (Model Context Protocol) tools integrated with a Gradio UI. AI agents like Claude, Cursor, and Antigravity can discover and call GitHub functions via MCP, while humans can use the intuitive web interface.

## 🎯 Features

### GitHub Operations
- **Create Repository** - Create new public/private GitHub repositories
- **List Repositories** - View all repositories for the authenticated account
- **Create Issue** - Open issues in any repository
- **List Issues** - View issues filtered by state (open/closed/all)
- **Commit File** - Create or update files in repositories
- **Read File** - Read file contents from repositories

### MCP Tools for AI Agents
The following tools are exposed via MCP for AI agent automation:
- `github.create_repo`
- `github.list_repos`
- `github.create_issue`
- `github.list_issues`
- `github.commit_file`
- `github.read_file`
- `github.generate_docs_with_tts`

## 🔧 Tech Stack

- **Python** - Core language
- **Gradio** - Web UI framework with MCP server support
- **PyGithub** - GitHub API wrapper
- **MCP** - Model Context Protocol for AI agent integration
- **Gemini 2.5 Flash** - AI Code Analysis & Documentation
- **ElevenLabs** - Text-to-Speech Generation

## 📦 Project Structure

```
HF-Pro/
├── app.py              # Main Gradio application with MCP handlers
├── ghclient.py         # GitHub API client wrapper
├── ai_helper.py        # AI Documentation & TTS helper
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Deployment to Hugging Face Spaces

### Prerequisites
1. A Hugging Face account
2. A GitHub Personal Access Token (PAT) with repo permissions
3. A Google Gemini API Key
4. An ElevenLabs API Key


## 🎮 Usage

### For Humans (Web UI)

The Gradio interface has 3 tabs:

**📦 Repositories Tab**
- Create new repositories with name, privacy setting, and description
- List all repositories for the authenticated account

**📋 Issues Tab**
- Create issues in any repository (format: `username/repo`)
- List issues filtered by state (open/closed/all)

**📄 Custom Files Tab**
- Commit files to repositories (creates or updates)
- Read file contents from repositories

**🤖 Code Documentation Tab**
- Upload code files for AI analysis
- Generate comprehensive documentation
- Listen to 2-line audio summary
- Commit documentation to GitHub

## 🔒 Security Notes

- **No user authentication required** - The Space uses a server-side GitHub token
- **All repos are public by default** - Anyone can view created repositories
- **Repository name validation** - Input validation prevents malicious repo names
- **Token security** - GitHub token is stored securely in HF Spaces secrets (never in code)

## 🛠️ Local Development

To run locally:

1. **Clone the repository**
   ```bash
   git clone <your-space-url>
   cd HF-Pro
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   # Windows (PowerShell)
   $env:GITHUB_TOKEN="your_github_token"
   $env:GEMINI_API_KEY="your_gemini_key"
   $env:ELEVENLABS_API_KEY="your_elevenlabs_key"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:7860`

## 📄 License

MIT License - feel free to use this code for your own projects.


