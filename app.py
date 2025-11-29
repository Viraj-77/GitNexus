"""
GitHub Automation Space - MCP-Enabled Gradio Application
Demonstrates GitHub automation with MCP tool discovery for AI agents
"""

import gradio as gr
import os
from ghclient import GitHubClient
from ai_helper import AIDocumentationGenerator
from typing import Dict, List


# Initialize GitHub client
def get_github_client(token: str = None):
    """Get or create GitHub client instance"""
    try:
        return GitHubClient(token)
    except ValueError as e:
        return None


# MCP Handler Functions
def mcp_create_repo(name: str, description: str = "", token: str = None) -> Dict:
    """MCP handler for creating a GitHub repository (always public)"""
    client = get_github_client(token)
    if not client:
        return {"error": "GitHub token not configured"}
    return client.create_repo(name, private=False, description=description)


def mcp_list_repos(token: str = None) -> List[Dict]:
    """MCP handler for listing GitHub repositories"""
    client = get_github_client(token)
    if not client:
        return [{"error": "GitHub token not configured"}]
    return client.list_repos()


def mcp_create_issue(repo_full_name: str, title: str, body: str = "", token: str = None) -> Dict:
    """MCP handler for creating a GitHub issue"""
    client = get_github_client(token)
    if not client:
        return {"error": "GitHub token not configured"}
    return client.create_issue(repo_full_name, title, body)


def mcp_list_issues(repo_full_name: str, state: str = "open", token: str = None) -> List[Dict]:
    """MCP handler for listing GitHub issues"""
    client = get_github_client(token)
    if not client:
        return [{"error": "GitHub token not configured"}]
    return client.list_issues(repo_full_name, state)


def mcp_commit_file(repo_full_name: str, path: str, content: str, message: str, token: str = None) -> Dict:
    """MCP handler for committing a file to GitHub"""
    client = get_github_client(token)
    if not client:
        return {"error": "GitHub token not configured"}
    return client.commit_file(repo_full_name, path, content, message)


def mcp_read_file(repo_full_name: str, path: str, token: str = None) -> Dict:
    """MCP handler for reading a file from GitHub"""
    client = get_github_client(token)
    if not client:
        return {"error": "GitHub token not configured"}
    return client.read_file(repo_full_name, path)


# Initialize AI helper
def get_ai_helper(user_gemini_key: str = None):
    """Get or create AI documentation generator instance"""
    try:
        return AIDocumentationGenerator(user_gemini_key)
    except ValueError as e:
        return None


def mcp_generate_docs_with_tts(code_content: str, language: str, filename: str) -> Dict:
    """MCP handler for generating documentation with TTS"""
    ai_helper = get_ai_helper()
    if not ai_helper:
        return {"error": "AI services not configured. Set GEMINI_API_KEY and ELEVENLABS_API_KEY."}
    
    try:
        result = ai_helper.generate_documentation(code_content, language, filename)
        audio = ai_helper.text_to_speech(result["summary"])
        
        return {
            "documentation": result["documentation"],
            "summary": result["summary"],
            "audio_generated": True,
            "filename": f"{filename}_summary.mp3"
        }
    except Exception as e:
        return {"error": str(e)}


# MCP Handlers Configuration
mcp_handlers = {
    "github.create_repo": {
        "handler": mcp_create_repo,
        "description": "Create a new GitHub repository (always public)",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Repository name"
                },
                "description": {
                    "type": "string",
                    "description": "Repository description",
                    "default": ""
                }
            },
            "required": ["name"]
        }
    },
    "github.list_repos": {
        "handler": mcp_list_repos,
        "description": "List all repositories for the authenticated user",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "github.create_issue": {
        "handler": mcp_create_issue,
        "description": "Create an issue in a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_full_name": {
                    "type": "string",
                    "description": "Full repository name (e.g., 'username/repo')"
                },
                "title": {
                    "type": "string",
                    "description": "Issue title"
                },
                "body": {
                    "type": "string",
                    "description": "Issue body/description",
                    "default": ""
                }
            },
            "required": ["repo_full_name", "title"]
        }
    },
    "github.list_issues": {
        "handler": mcp_list_issues,
        "description": "List issues in a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_full_name": {
                    "type": "string",
                    "description": "Full repository name (e.g., 'username/repo')"
                },
                "state": {
                    "type": "string",
                    "description": "Issue state filter: 'open', 'closed', or 'all'",
                    "default": "open",
                    "enum": ["open", "closed", "all"]
                }
            },
            "required": ["repo_full_name"]
        }
    },
    "github.commit_file": {
        "handler": mcp_commit_file,
        "description": "Create or update a file in a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_full_name": {
                    "type": "string",
                    "description": "Full repository name (e.g., 'username/repo')"
                },
                "path": {
                    "type": "string",
                    "description": "File path in repository"
                },
                "content": {
                    "type": "string",
                    "description": "File content"
                },
                "message": {
                    "type": "string",
                    "description": "Commit message"
                }
            },
            "required": ["repo_full_name", "path", "content", "message"]
        }
    },
    "github.read_file": {
        "handler": mcp_read_file,
        "description": "Read a file from a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_full_name": {
                    "type": "string",
                    "description": "Full repository name (e.g., 'username/repo')"
                },
                "path": {
                    "type": "string",
                    "description": "File path in repository"
                }
            },
            "required": ["repo_full_name", "path"]
        }
    },
    "github.generate_docs_with_tts": {
        "handler": mcp_generate_docs_with_tts,
        "description": "Generate code documentation and audio summary using AI (Gemini + ElevenLabs)",
        "parameters": {
            "type": "object",
            "properties": {
                "code_content": {
                    "type": "string",
                    "description": "The code to analyze and document"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language (python, javascript, java, cpp, go, rust, typescript, etc.)"
                },
                "filename": {
                    "type": "string",
                    "description": "Original filename for context"
                }
            },
            "required": ["code_content", "language", "filename"]
        }
    }
}


# UI Handler Functions
def ui_create_repo(name: str, description: str, token: str = "") -> str:
    """UI handler for creating a repository"""
    try:
        result = mcp_create_repo(name, description, token if token.strip() else None)
        if "error" in result:
            return f"❌ Error: {result['error']}"
        return f"✅ Repository created!\n\n📦 Name: {result['name']}\n🔗 URL: {result['url']}\n📝 Description: {result.get('description', 'N/A')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_list_repos(token: str = "") -> str:
    """UI handler for listing repositories"""
    try:
        repos = mcp_list_repos(token if token.strip() else None)
        if not repos:
            return "No repositories found."
        if isinstance(repos, list) and len(repos) > 0 and "error" in repos[0]:
            return f"❌ Error: {repos[0]['error']}"
        
        output = f"📚 Found {len(repos)} repositories:\n\n"
        for repo in repos:
            output += f"📦 {repo['name']}\n"
            output += f"   🔗 {repo['url']}\n"
            output += f"   🔒 {'Private' if repo['private'] else 'Public'}\n"
            if repo.get('description'):
                output += f"   📝 {repo['description']}\n"
            output += "\n"
        return output
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_create_issue(repo_full_name: str, title: str, body: str, token: str = "") -> str:
    """UI handler for creating an issue"""
    try:
        result = mcp_create_issue(repo_full_name, title, body, token if token.strip() else None)
        if "error" in result:
            return f"❌ Error: {result['error']}"
        return f"✅ Issue created!\n\n🔢 Number: #{result['number']}\n📌 Title: {result['title']}\n🔗 URL: {result['url']}\n📊 State: {result['state']}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_list_issues(repo_full_name: str, state: str, token: str = "") -> str:
    """UI handler for listing issues"""
    try:
        issues = mcp_list_issues(repo_full_name, state, token if token.strip() else None)
        if not issues:
            return f"No {state} issues found."
        if isinstance(issues, list) and len(issues) > 0 and "error" in issues[0]:
            return f"❌ Error: {issues[0]['error']}"
        
        output = f"📋 Found {len(issues)} {state} issues:\n\n"
        for issue in issues:
            output += f"🔢 #{issue['number']} - {issue['title']}\n"
            output += f"   🔗 {issue['url']}\n"
            output += f"   📊 {issue['state']}\n\n"
        return output
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_commit_file(repo_full_name: str, path: str, content: str, message: str, token: str = "") -> str:
    """UI handler for committing a file"""
    try:
        result = mcp_commit_file(repo_full_name, path, content, message, token if token.strip() else None)
        if "error" in result:
            return f"❌ Error: {result['error']}"
        return f"✅ File {result['action']}!\n\n📄 Path: {result['path']}\n🔗 URL: {result['url']}\n📝 Commit: {result['commit_sha'][:7]}\n⚡ Action: {result['action'].upper()}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_read_file(repo_full_name: str, path: str, token: str = "") -> tuple:
    """UI handler for reading a file"""
    try:
        result = mcp_read_file(repo_full_name, path, token if token.strip() else None)
        if "error" in result:
            return f"❌ Error: {result['error']}", ""
        
        info = f"✅ File read successfully!\n\n📄 Path: {result['path']}\n🔗 URL: {result['url']}\n📊 Size: {result['size']} bytes"
        return info, result['content']
    except Exception as e:
        return f"❌ Error: {str(e)}", ""


def ui_generate_docs(file, language: str, user_key: str = "") -> tuple:
    """UI handler for AI documentation generation with TTS"""
    try:
        if file is None:
            return "❌ Please upload a file", "", None
        
        # Read uploaded file
        if hasattr(file, 'name'):
            filename = os.path.basename(file.name)
            with open(file.name, 'r', encoding='utf-8') as f:
                code_content = f.read()
        else:
            return "❌ Invalid file upload", "", None
        
        # Generate documentation and TTS
        # Use user key if provided, otherwise fallback to env var
        ai_helper = get_ai_helper(user_key if user_key.strip() else None)
        if not ai_helper or not ai_helper.gemini_model:
            return "❌ AI services not configured. Please set GEMINI_API_KEY (env) or provide your own key.", "", None
        
        docs, summary, audio = ai_helper.process_file(code_content, language, filename)
        
        # Save audio to temporary file for Gradio
        import tempfile
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
        with open(audio_path, 'wb') as f:
            f.write(audio)
        
        return docs, summary, audio_path
        
    except Exception as e:
        return f"❌ Error: {str(e)}", "", None


def ui_commit_docs(repo_full_name: str, path: str, documentation: str, token: str = "") -> str:
    """UI handler for committing generated documentation"""
    try:
        if not documentation or documentation.startswith("❌"):
            return "❌ No documentation to commit. Generate documentation first."
        
        result = mcp_commit_file(repo_full_name, path, documentation, "Add AI-generated documentation", token if token.strip() else None)
        if "error" in result:
            return f"❌ Error: {result['error']}"
        return f"✅ Documentation committed!\n\n📄 Path: {result['path']}\n🔗 URL: {result['url']}\n📝 Commit: {result['commit_sha'][:7]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_commit_code_file(file, repo_full_name: str, path: str, token: str = "") -> str:
    """UI handler for committing the uploaded code file"""
    try:
        if file is None:
            return "❌ No file uploaded. Please upload a code file first."
        
        # Read uploaded file
        if hasattr(file, 'name'):
            with open(file.name, 'r', encoding='utf-8') as f:
                code_content = f.read()
        else:
            return "❌ Invalid file upload"
        
        result = mcp_commit_file(repo_full_name, path, code_content, f"Add {os.path.basename(file.name)}", token if token.strip() else None)
        if "error" in result:
            return f"❌ Error: {result['error']}"
        return f"✅ Code file committed!\n\n📄 Path: {result['path']}\n🔗 URL: {result['url']}\n📝 Commit: {result['commit_sha'][:7]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def ui_commit_both(file, repo_full_name: str, code_path: str, docs_path: str, documentation: str, token: str = "") -> str:
    """UI handler for committing both code file and documentation"""
    try:
        results = []
        token_val = token if token.strip() else None
        
        # Commit code file
        if file is not None:
            if hasattr(file, 'name'):
                with open(file.name, 'r', encoding='utf-8') as f:
                    code_content = f.read()
                
                result = mcp_commit_file(repo_full_name, code_path, code_content, f"Add {os.path.basename(file.name)}", token_val)
                if "error" in result:
                    results.append(f"❌ Code file error: {result['error']}")
                else:
                    results.append(f"✅ Code file committed: {result['url']}")
        else:
            results.append("⚠️ No code file uploaded, skipping")
        
        # Commit documentation
        if documentation and not documentation.startswith("❌"):
            result = mcp_commit_file(repo_full_name, docs_path, documentation, "Add AI-generated documentation", token_val)
            if "error" in result:
                results.append(f"❌ Documentation error: {result['error']}")
            else:
                results.append(f"✅ Documentation committed: {result['url']}")
        else:
            results.append("⚠️ No documentation generated, skipping")
        
        return "\n\n".join(results)
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Build Gradio UI
def build_ui():
    """Build the Gradio interface"""
    
    with gr.Blocks(title="GitNexus") as demo:
        gr.Markdown("""
        # 🚀 GitNexus
        
        **MCP-Enabled GitHub Automation for AI Agents**
        
        🔗 **Demo GitHub Account**: [https://github.com/DemoAcc4HF](https://github.com/DemoAcc4HF)  
        👤 **Username**: `DemoAcc4HF`
        """)
        
        # Global GitHub Token Input
        with gr.Row():
            user_github_token = gr.Textbox(
                label="Optional: Your GitHub Token (Classic)",
                placeholder="ghp_... (Leave empty to use default system token)",
                type="password"
            )
        
        with gr.Tabs():
            # TAB 1: Repositories
            with gr.Tab("📦 Repositories"):
                gr.Markdown("### Create Repository")
                repo_name = gr.Textbox(label="Repository Name", placeholder="my-awesome-repo")
                repo_description = gr.Textbox(label="Description", placeholder="A cool project")
                create_repo_btn = gr.Button("Create Repository", variant="primary")
                create_repo_output = gr.Textbox(label="Result", lines=6)
                
                gr.Markdown("### List Repositories")
                list_repos_btn = gr.Button("List All Repositories")
                list_repos_output = gr.Textbox(label="Repositories", lines=10)
                
                create_repo_btn.click(
                    ui_create_repo,
                    inputs=[repo_name, repo_description, user_github_token],
                    outputs=create_repo_output
                )
                list_repos_btn.click(
                    ui_list_repos,
                    inputs=[user_github_token],
                    outputs=list_repos_output
                )
            
            # TAB 2: Issues
            with gr.Tab("📋 Issues"):
                gr.Markdown("### Create Issue")
                issue_repo = gr.Textbox(label="Repository (username/repo)", placeholder="octocat/Hello-World")
                issue_title = gr.Textbox(label="Issue Title", placeholder="Bug: Something is broken")
                issue_body = gr.Textbox(label="Issue Body", placeholder="Detailed description...", lines=4)
                create_issue_btn = gr.Button("Create Issue", variant="primary")
                create_issue_output = gr.Textbox(label="Result", lines=6)
                
                gr.Markdown("### List Issues")
                list_issue_repo = gr.Textbox(label="Repository (username/repo)", placeholder="octocat/Hello-World")
                list_issue_state = gr.Radio(["open", "closed", "all"], label="State", value="open")
                list_issues_btn = gr.Button("List Issues")
                list_issues_output = gr.Textbox(label="Issues", lines=10)
                
                create_issue_btn.click(
                    ui_create_issue,
                    inputs=[issue_repo, issue_title, issue_body, user_github_token],
                    outputs=create_issue_output
                )
                list_issues_btn.click(
                    ui_list_issues,
                    inputs=[list_issue_repo, list_issue_state, user_github_token],
                    outputs=list_issues_output
                )
            
            # TAB 3: Custom Files
            with gr.Tab("📄 Custom Files"):
                gr.Markdown("### Commit File")
                commit_repo = gr.Textbox(label="Repository (username/repo)", placeholder="octocat/Hello-World")
                commit_path = gr.Textbox(label="File Path", placeholder="src/main.py")
                commit_content = gr.Textbox(label="File Content", placeholder="print('Hello, World!')", lines=6)
                commit_message = gr.Textbox(label="Commit Message", placeholder="Add main.py")
                commit_file_btn = gr.Button("Commit File", variant="primary")
                commit_file_output = gr.Textbox(label="Result", lines=6)
                
                gr.Markdown("### Read File")
                read_repo = gr.Textbox(label="Repository (username/repo)", placeholder="octocat/Hello-World")
                read_path = gr.Textbox(label="File Path", placeholder="README.md")
                read_file_btn = gr.Button("Read File")
                read_file_info = gr.Textbox(label="File Info", lines=4)
                read_file_content = gr.Textbox(label="File Content", lines=10)
                
                commit_file_btn.click(
                    ui_commit_file,
                    inputs=[commit_repo, commit_path, commit_content, commit_message, user_github_token],
                    outputs=commit_file_output
                )
                read_file_btn.click(
                    ui_read_file,
                    inputs=[read_repo, read_path, user_github_token],
                    outputs=[read_file_info, read_file_content]
                )
            
            # TAB 4: Code Documentation
            with gr.Tab("🤖 Code Documentation"):
                gr.Markdown("""
                ### Upload Code for AI-Powered Documentation
                Upload your code file and get comprehensive documentation + audio summary!
                """)
                
                with gr.Row():
                    file_upload = gr.File(
                        label="📁 Upload Code File",
                        file_types=[".py", ".js", ".java", ".cpp", ".go", ".rs", ".ts", ".jsx", ".tsx", ".c", ".h"]
                    )
                    with gr.Column():
                        language_select = gr.Dropdown(
                            choices=["python", "javascript", "java", "cpp", "go", "rust", "typescript", "c"],
                            label="Programming Language",
                            value="python"
                        )
                        user_gemini_key = gr.Textbox(
                            label="Optional: Your Gemini API Key",
                            placeholder="AIzaSy... (Leave empty to use default key)",
                            type="password"
                        )
                
                generate_btn = gr.Button("🚀 Generate Documentation + Audio Summary", variant="primary", size="lg")
                
                gr.Markdown("### 📚 Generated Documentation")
                docs_output = gr.Markdown(label="Full Documentation")
                
                gr.Markdown("### 📝 2-Line Summary")
                summary_output = gr.Textbox(label="Summary", lines=2, max_lines=2, interactive=False)
                
                gr.Markdown("### 🔊 Audio Summary (Text-to-Speech)")
                audio_output = gr.Audio(label="Listen to Summary", type="filepath")
                
                gr.Markdown("### 💾 Commit to Repository")
                gr.Markdown("Upload both the code file and generated documentation to GitHub")
                with gr.Row():
                    commit_repo = gr.Textbox(label="Repository (username/repo)", placeholder="DemoAcc4HF/my-repo")
                with gr.Row():
                    commit_code_path = gr.Textbox(label="Code File Path", placeholder="src/main.py")
                    commit_docs_path = gr.Textbox(label="Documentation Path", value="DOCUMENTATION.md")
                with gr.Row():
                    commit_code_btn = gr.Button("Commit Code File", variant="secondary")
                    commit_docs_btn = gr.Button("Commit Documentation", variant="secondary")
                    commit_both_btn = gr.Button("Commit Both Files", variant="primary")
                commit_output = gr.Textbox(label="Result", lines=6)
                
                # Event handlers
                generate_btn.click(
                    ui_generate_docs,
                    inputs=[file_upload, language_select, user_gemini_key],
                    outputs=[docs_output, summary_output, audio_output]
                )
                
                commit_code_btn.click(
                    ui_commit_code_file,
                    inputs=[file_upload, commit_repo, commit_code_path, user_github_token],
                    outputs=commit_output
                )
                
                commit_docs_btn.click(
                    ui_commit_docs,
                    inputs=[commit_repo, commit_docs_path, docs_output, user_github_token],
                    outputs=commit_output
                )
                
                commit_both_btn.click(
                    ui_commit_both,
                    inputs=[file_upload, commit_repo, commit_code_path, commit_docs_path, docs_output, user_github_token],
                    outputs=commit_output
                )
        
        
        gr.Markdown("""
        ---
        💡 All repositories are created as **public**.
        """)
    
    return demo


if __name__ == "__main__":
    # Check if GitHub token is available
    if not os.environ.get("GITHUB_TOKEN"):
        print("⚠️  WARNING: GITHUB_TOKEN environment variable not set!")
        print("   The application will not function without a valid GitHub token.")
        print("   Set it in Hugging Face Space secrets or your environment.")
    
    # Build and launch the app
    app = build_ui()
    
    # Try to launch with MCP support if available, otherwise launch normally
    try:
        app.launch(
            mcp_server=True,
            mcp_handlers=mcp_handlers,
            share=False
        )
    except TypeError:
        # MCP not supported in this Gradio version, launch normally
        print("ℹ️  Note: MCP server support not available in this Gradio version.")
        print("   The UI will work, but MCP handlers won't be exposed.")
        print("   For full MCP support, this will work when deployed to HF Spaces.")
        app.launch(share=False)

