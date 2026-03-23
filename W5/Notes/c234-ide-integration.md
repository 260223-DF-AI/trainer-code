# IDE Integration

## Learning Objectives

- Set up AI coding tools in VS Code and other IDEs
- Configure AI tool settings for optimal productivity
- Understand keyboard shortcuts and workflows for AI assistance
- Manage AI tool settings for privacy and performance

## Why This Matters

An AI tool is only useful if it is properly integrated into your workflow. A well-configured IDE with AI assistance becomes a productivity powerhouse. A poorly configured one creates friction and frustration. This topic ensures you can set up, configure, and optimize AI tools in your development environment.

## The Concept

### Setting Up Copilot in VS Code

#### Installation Steps

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "GitHub Copilot"
4. Install the "GitHub Copilot" extension
5. Install the "GitHub Copilot Chat" extension
6. Sign in with your GitHub account
7. Authorize the extension

#### Verifying Installation

Once installed, you should see:

- A Copilot icon in the status bar (bottom of VS Code)
- Ghost text suggestions when typing code
- A Copilot Chat panel available in the sidebar

### Key Keyboard Shortcuts

| Shortcut (Windows/Linux) | Action |
| ------------------------ | ------ |
| Tab | Accept inline suggestion |
| Esc | Dismiss suggestion |
| Alt+] | Next suggestion |
| Alt+[ | Previous suggestion |
| Ctrl+Enter | Open Copilot completions panel |
| Ctrl+I | Open inline chat |
| Ctrl+Shift+I | Open Copilot Chat panel |

### Configuring Copilot Settings

Access settings through: File > Preferences > Settings > Search "Copilot"

Key settings to configure:

```json
{
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "sql": true,
    "python": true
  },
  "github.copilot.advanced": {
    "inlineSuggestCount": 3
  }
}
```

#### Language-Specific Configuration

Enable or disable Copilot for specific languages:

```json
{
  "github.copilot.enable": {
    "python": true,
    "sql": true,
    "markdown": true,
    "yaml": false,
    "plaintext": false
  }
}
```

Disabling Copilot for plaintext and YAML can prevent suggestions when editing configuration files or sensitive documents.

### Other IDE Support

#### JetBrains IDEs (IntelliJ, PyCharm, DataGrip)

1. Go to Settings > Plugins
2. Search for "GitHub Copilot"
3. Install and restart the IDE
4. Sign in via GitHub

#### Visual Studio

1. Go to Extensions > Manage Extensions
2. Search for "GitHub Copilot"
3. Install and restart Visual Studio

#### Neovim

```lua
-- Using Lazy plugin manager
{
  "github/copilot.vim",
  config = function()
    vim.g.copilot_enabled = true
  end
}
```

### Setting Up Alternative Tools

#### Codeium

1. Install the Codeium extension from VS Code marketplace
2. Create a free account at codeium.com
3. Sign in through the extension
4. Codeium begins providing suggestions immediately

#### Cursor IDE

Cursor is a standalone IDE (fork of VS Code) with AI built in:

1. Download from cursor.sh
2. Import VS Code settings and extensions
3. AI features work immediately with no additional extensions needed

### Optimizing Your AI-Enhanced Workflow

#### Tip 1: Write Descriptive Comments

AI tools use comments as context:

```python
# BAD: No comment context
def process():
    pass

# GOOD: Clear comment guides the AI
# Connect to BigQuery, run the daily sales summary 
# query, and return results as a DataFrame
def process_daily_sales():
    pass  # AI now has context to suggest implementation
```

#### Tip 2: Use Meaningful File and Variable Names

```python
# BAD: Generic names
def func(x, y):
    return x + y

# GOOD: Descriptive names guide AI suggestions
def calculate_total_revenue(unit_price, quantity):
    return unit_price * quantity
```

#### Tip 3: Keep Related Files Open

Many AI tools consider open tabs as context. When working on a data pipeline:

- Keep your schema definitions open
- Keep your configuration file open
- Keep related utility modules open

#### Tip 4: Use .copilotignore

Create a `.copilotignore` file to prevent Copilot from reading sensitive files:

```
# .copilotignore
.env
credentials.json
secrets/
config/production.yaml
```

## Key Takeaways

- Setting up AI tools in VS Code takes minutes: install extension, sign in, start coding
- Keyboard shortcuts (Tab to accept, Esc to dismiss, Alt+]/[ to cycle) are essential
- Configure language-specific settings to control where AI suggestions appear
- Write descriptive comments and use meaningful names to improve AI suggestion quality
- Use .copilotignore to exclude sensitive files from AI context

## Additional Resources

- [VS Code Copilot Setup Guide](https://docs.github.com/en/copilot/using-github-copilot/getting-code-suggestions-in-your-ide-with-github-copilot)
- [Copilot Keyboard Shortcuts](https://docs.github.com/en/copilot/using-github-copilot/getting-started-with-github-copilot)
- [Codeium - Getting Started](https://codeium.com/vscode_tutorial)
