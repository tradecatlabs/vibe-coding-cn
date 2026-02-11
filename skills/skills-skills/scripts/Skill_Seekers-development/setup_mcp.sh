#!/bin/bash
# Skill Seeker MCP Server - Quick Setup Script
# This script automates the MCP server setup for Claude Code

set -e  # Exit on error

echo "=================================================="
echo "Skill Seeker MCP Server - Quick Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: python3 not found${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
echo ""

# Step 2: Get repository path
REPO_PATH=$(pwd)
echo "Step 2: Repository location"
echo "Path: $REPO_PATH"
echo ""

# Step 3: Install dependencies
echo "Step 3: Installing Python dependencies..."

# Check if we're in a virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo -e "${GREEN}✓${NC} Virtual environment detected: $VIRTUAL_ENV"
    PIP_INSTALL_CMD="pip install"
elif [[ -d "venv" ]]; then
    echo -e "${YELLOW}⚠${NC} Virtual environment found but not activated"
    echo "Activating venv..."
    source venv/bin/activate
    PIP_INSTALL_CMD="pip install"
else
    echo -e "${YELLOW}⚠${NC} No virtual environment found"
    echo "It's recommended to use a virtual environment to avoid conflicts."
    echo ""
    read -p "Would you like to create one now? (y/n) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating virtual environment..."
        python3 -m venv venv || {
            echo -e "${RED}❌ Failed to create virtual environment${NC}"
            echo "Falling back to system install..."
            PIP_INSTALL_CMD="pip3 install --user --break-system-packages"
        }

        if [[ -d "venv" ]]; then
            source venv/bin/activate
            PIP_INSTALL_CMD="pip install"
            echo -e "${GREEN}✓${NC} Virtual environment created and activated"
        fi
    else
        echo "Proceeding with system install (using --user --break-system-packages)..."
        echo -e "${YELLOW}Note:${NC} This may override system-managed packages"
        PIP_INSTALL_CMD="pip3 install --user --break-system-packages"
    fi
fi

echo "This will install: mcp, requests, beautifulsoup4"
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing package in editable mode..."
    $PIP_INSTALL_CMD -e . || {
        echo -e "${RED}❌ Failed to install package${NC}"
        exit 1
    }

    echo -e "${GREEN}✓${NC} Dependencies installed successfully"
else
    echo "Skipping dependency installation"
fi
echo ""

# Step 4: Test MCP server
echo "Step 4: Testing MCP server..."
timeout 3 python3 src/skill_seekers/mcp/server.py 2>/dev/null || {
    if [ $? -eq 124 ]; then
        echo -e "${GREEN}✓${NC} MCP server starts correctly (timeout expected)"
    else
        echo -e "${YELLOW}⚠${NC} MCP server test inconclusive, but may still work"
    fi
}
echo ""

# Step 5: Optional - Run tests
echo "Step 5: Run test suite? (optional)"
read -p "Run MCP tests to verify everything works? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo "Installing pytest..."
        $PIP_INSTALL_CMD pytest || {
            echo -e "${YELLOW}⚠${NC} Could not install pytest, skipping tests"
        }
    fi

    if command -v pytest &> /dev/null; then
        echo "Running MCP server tests..."
        python3 -m pytest tests/test_mcp_server.py -v --tb=short || {
            echo -e "${RED}❌ Some tests failed${NC}"
            echo "The server may still work, but please check the errors above"
        }
    fi
else
    echo "Skipping tests"
fi
echo ""

# Step 6: Configure Claude Code
echo "Step 6: Configure Claude Code"
echo "=================================================="
echo ""
echo "You need to add this configuration to Claude Code:"
echo ""
echo -e "${YELLOW}Configuration file:${NC} ~/.config/claude-code/mcp.json"
echo ""
echo "Add this JSON configuration (paths are auto-detected for YOUR system):"
echo ""
echo -e "${GREEN}{"
echo "  \"mcpServers\": {"
echo "    \"skill-seeker\": {"
echo "      \"command\": \"python3\","
echo "      \"args\": ["
echo "        \"$REPO_PATH/src/skill_seekers/mcp/server.py\""
echo "      ],"
echo "      \"cwd\": \"$REPO_PATH\""
echo "    }"
echo "  }"
echo -e "}${NC}"
echo ""
echo -e "${YELLOW}Note:${NC} The paths above are YOUR actual paths (not placeholders!)"
echo ""

# Ask if user wants auto-configure
echo ""
read -p "Auto-configure Claude Code now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if config already exists
    if [ -f ~/.config/claude-code/mcp.json ]; then
        echo -e "${YELLOW}⚠ Warning: ~/.config/claude-code/mcp.json already exists${NC}"
        echo "Current contents:"
        cat ~/.config/claude-code/mcp.json
        echo ""
        read -p "Overwrite? (y/n) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping auto-configuration"
            echo "Please manually add the skill-seeker server to your config"
            exit 0
        fi
    fi

    # Create config directory
    mkdir -p ~/.config/claude-code

    # Write configuration with actual expanded path
    cat > ~/.config/claude-code/mcp.json << EOF
{
  "mcpServers": {
    "skill-seeker": {
      "command": "python3",
      "args": [
        "$REPO_PATH/src/skill_seekers/mcp/server.py"
      ],
      "cwd": "$REPO_PATH"
    }
  }
}
EOF

    echo -e "${GREEN}✓${NC} Configuration written to ~/.config/claude-code/mcp.json"
    echo ""
    echo "Configuration contents:"
    cat ~/.config/claude-code/mcp.json
    echo ""

    # Verify the path exists
    if [ -f "$REPO_PATH/src/skill_seekers/mcp/server.py" ]; then
        echo -e "${GREEN}✓${NC} Verified: MCP server file exists at $REPO_PATH/src/skill_seekers/mcp/server.py"
    else
        echo -e "${RED}❌ Warning: MCP server not found at $REPO_PATH/src/skill_seekers/mcp/server.py${NC}"
        echo "Please check the path!"
    fi
else
    echo "Skipping auto-configuration"
    echo "Please manually configure Claude Code using the JSON above"
    echo ""
    echo "IMPORTANT: Replace \$REPO_PATH with the actual path: $REPO_PATH"
fi
echo ""

# Step 7: Test the configuration
if [ -f ~/.config/claude-code/mcp.json ]; then
    echo "Step 7: Testing MCP configuration..."
    echo "Checking if paths are correct..."

    # Extract the configured path
    if command -v jq &> /dev/null; then
        CONFIGURED_PATH=$(jq -r '.mcpServers["skill-seeker"].args[0]' ~/.config/claude-code/mcp.json 2>/dev/null || echo "")
        if [ -n "$CONFIGURED_PATH" ] && [ -f "$CONFIGURED_PATH" ]; then
            echo -e "${GREEN}✓${NC} MCP server path is valid: $CONFIGURED_PATH"
        elif [ -n "$CONFIGURED_PATH" ]; then
            echo -e "${YELLOW}⚠${NC} Warning: Configured path doesn't exist: $CONFIGURED_PATH"
        fi
    else
        echo "Install 'jq' for config validation: brew install jq (macOS) or apt install jq (Linux)"
    fi
fi
echo ""

# Step 8: Final instructions
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "  1. ${YELLOW}Restart Claude Code${NC} (quit and reopen, don't just close window)"
echo "  2. In Claude Code, test with: ${GREEN}\"List all available configs\"${NC}"
echo "  3. You should see 9 Skill Seeker tools available"
echo ""
echo "Available MCP Tools:"
echo "  • generate_config   - Create new config files"
echo "  • estimate_pages    - Estimate scraping time"
echo "  • scrape_docs       - Scrape documentation"
echo "  • package_skill     - Create .zip files"
echo "  • list_configs      - Show available configs"
echo "  • validate_config   - Validate config files"
echo ""
echo "Example commands to try in Claude Code:"
echo "  • ${GREEN}List all available configs${NC}"
echo "  • ${GREEN}Validate configs/react.json${NC}"
echo "  • ${GREEN}Generate config for Tailwind at https://tailwindcss.com/docs${NC}"
echo ""
echo "Documentation:"
echo "  • MCP Setup Guide: ${YELLOW}docs/MCP_SETUP.md${NC}"
echo "  • Full docs: ${YELLOW}README.md${NC}"
echo ""
echo "Troubleshooting:"
echo "  • Check logs: ~/Library/Logs/Claude Code/ (macOS)"
echo "  • Test server: python3 src/skill_seekers/mcp/server.py"
echo "  • Run tests: python3 -m pytest tests/test_mcp_server.py -v"
echo ""
echo "Happy skill creating! 🚀"
