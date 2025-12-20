#!/usr/bin/env python3
"""
Comprehensive test suite for Skill Seeker MCP Server
Tests all MCP tools and server functionality
"""

import sys
import os
import unittest
import json
import tempfile
import shutil
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock

# CRITICAL: Import MCP package BEFORE adding project to path
# to avoid shadowing the installed mcp package with our local mcp/ directory

# WORKAROUND for shadowing issue: Temporarily change to /tmp to import external mcp
# This avoids our local mcp/ directory being in the import path
_original_dir = os.getcwd()
try:
    os.chdir('/tmp')  # Change away from project directory
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP package not available, skipping MCP tests")
finally:
    os.chdir(_original_dir)  # Restore original directory

# NOW add parent directory to path for importing our local modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our local MCP server module
if MCP_AVAILABLE:
    # Import from installed package (new src/ layout)
    try:
        from skill_seekers.mcp import server as skill_seeker_server
    except ImportError as e:
        print(f"Warning: Could not import skill_seeker server: {e}")
        skill_seeker_server = None


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestMCPServerInitialization(unittest.TestCase):
    """Test MCP server initialization"""

    def test_server_import(self):
        """Test that server module can be imported"""
        from mcp import server as mcp_server_module
        self.assertIsNotNone(mcp_server_module)

    def test_server_initialization(self):
        """Test server initializes correctly"""
        import mcp.server
        app = mcp.server.Server("test-skill-seeker")
        self.assertEqual(app.name, "test-skill-seeker")


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestListTools(unittest.IsolatedAsyncioTestCase):
    """Test list_tools functionality"""

    async def test_list_tools_returns_tools(self):
        """Test that list_tools returns all expected tools"""
        tools = await skill_seeker_server.list_tools()

        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)

        # Check all expected tools are present
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "generate_config",
            "estimate_pages",
            "scrape_docs",
            "package_skill",
            "list_configs",
            "validate_config"
        ]

        for expected in expected_tools:
            self.assertIn(expected, tool_names, f"Missing tool: {expected}")

    async def test_tool_schemas(self):
        """Test that all tools have valid schemas"""
        tools = await skill_seeker_server.list_tools()

        for tool in tools:
            self.assertIsInstance(tool.name, str)
            self.assertIsInstance(tool.description, str)
            self.assertIn("inputSchema", tool.__dict__)

            # Verify schema has required structure
            schema = tool.inputSchema
            self.assertEqual(schema["type"], "object")
            self.assertIn("properties", schema)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestGenerateConfigTool(unittest.IsolatedAsyncioTestCase):
    """Test generate_config tool"""

    async def asyncSetUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    async def asyncTearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_generate_config_basic(self):
        """Test basic config generation"""
        args = {
            "name": "test-framework",
            "url": "https://test-framework.dev/",
            "description": "Test framework skill"
        }

        result = await skill_seeker_server.generate_config_tool(args)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], TextContent)
        self.assertIn("✅", result[0].text)

        # Verify config file was created
        config_path = Path("configs/test-framework.json")
        self.assertTrue(config_path.exists())

        # Verify config content
        with open(config_path) as f:
            config = json.load(f)
            self.assertEqual(config["name"], "test-framework")
            self.assertEqual(config["base_url"], "https://test-framework.dev/")
            self.assertEqual(config["description"], "Test framework skill")

    async def test_generate_config_with_options(self):
        """Test config generation with custom options"""
        args = {
            "name": "custom-framework",
            "url": "https://custom.dev/",
            "description": "Custom skill",
            "max_pages": 200,
            "rate_limit": 1.0
        }

        result = await skill_seeker_server.generate_config_tool(args)

        # Verify config has custom options
        config_path = Path("configs/custom-framework.json")
        with open(config_path) as f:
            config = json.load(f)
            self.assertEqual(config["max_pages"], 200)
            self.assertEqual(config["rate_limit"], 1.0)

    async def test_generate_config_defaults(self):
        """Test that default values are applied correctly"""
        args = {
            "name": "default-test",
            "url": "https://test.dev/",
            "description": "Test defaults"
        }

        result = await skill_seeker_server.generate_config_tool(args)

        config_path = Path("configs/default-test.json")
        with open(config_path) as f:
            config = json.load(f)
            self.assertEqual(config["max_pages"], 100)  # Default
            self.assertEqual(config["rate_limit"], 0.5)  # Default


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestEstimatePagesTool(unittest.IsolatedAsyncioTestCase):
    """Test estimate_pages tool"""

    async def asyncSetUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create a test config
        os.makedirs("configs", exist_ok=True)
        self.config_path = Path("configs/test.json")
        config_data = {
            "name": "test",
            "base_url": "https://example.com/",
            "selectors": {
                "main_content": "article",
                "title": "h1",
                "code_blocks": "pre"
            },
            "rate_limit": 0.5,
            "max_pages": 50
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f)

    async def asyncTearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_estimate_pages_success(self, mock_streaming):
        """Test successful page estimation"""
        # Mock successful subprocess run with streaming
        # Returns (stdout, stderr, returncode)
        mock_streaming.return_value = ("Estimated 50 pages", "", 0)

        args = {
            "config_path": str(self.config_path)
        }

        result = await skill_seeker_server.estimate_pages_tool(args)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], TextContent)
        self.assertIn("50 pages", result[0].text)
        # Should also have progress message
        self.assertIn("Estimating page count", result[0].text)

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_estimate_pages_with_max_discovery(self, mock_streaming):
        """Test page estimation with custom max_discovery"""
        # Mock successful subprocess run with streaming
        mock_streaming.return_value = ("Estimated 100 pages", "", 0)

        args = {
            "config_path": str(self.config_path),
            "max_discovery": 500
        }

        result = await skill_seeker_server.estimate_pages_tool(args)

        # Verify subprocess was called with correct args
        mock_streaming.assert_called_once()
        call_args = mock_streaming.call_args[0][0]
        self.assertIn("--max-discovery", call_args)
        self.assertIn("500", call_args)

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_estimate_pages_error(self, mock_streaming):
        """Test error handling in page estimation"""
        # Mock failed subprocess run with streaming
        mock_streaming.return_value = ("", "Config file not found", 1)

        args = {
            "config_path": "nonexistent.json"
        }

        result = await skill_seeker_server.estimate_pages_tool(args)

        self.assertIn("Error", result[0].text)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestScrapeDocsTool(unittest.IsolatedAsyncioTestCase):
    """Test scrape_docs tool"""

    async def asyncSetUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create test config
        os.makedirs("configs", exist_ok=True)
        self.config_path = Path("configs/test.json")
        config_data = {
            "name": "test",
            "base_url": "https://example.com/",
            "selectors": {
                "main_content": "article",
                "title": "h1",
                "code_blocks": "pre"
            }
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f)

    async def asyncTearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_scrape_docs_basic(self, mock_streaming):
        """Test basic documentation scraping"""
        # Mock successful subprocess run with streaming
        mock_streaming.return_value = ("Scraping completed successfully", "", 0)

        args = {
            "config_path": str(self.config_path)
        }

        result = await skill_seeker_server.scrape_docs_tool(args)

        self.assertIsInstance(result, list)
        self.assertIn("success", result[0].text.lower())

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_scrape_docs_with_skip_scrape(self, mock_streaming):
        """Test scraping with skip_scrape flag"""
        # Mock successful subprocess run with streaming
        mock_streaming.return_value = ("Using cached data", "", 0)

        args = {
            "config_path": str(self.config_path),
            "skip_scrape": True
        }

        result = await skill_seeker_server.scrape_docs_tool(args)

        # Verify --skip-scrape was passed
        call_args = mock_streaming.call_args[0][0]
        self.assertIn("--skip-scrape", call_args)

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_scrape_docs_with_dry_run(self, mock_streaming):
        """Test scraping with dry_run flag"""
        # Mock successful subprocess run with streaming
        mock_streaming.return_value = ("Dry run completed", "", 0)

        args = {
            "config_path": str(self.config_path),
            "dry_run": True
        }

        result = await skill_seeker_server.scrape_docs_tool(args)

        call_args = mock_streaming.call_args[0][0]
        self.assertIn("--dry-run", call_args)

    @patch('skill_seekers.mcp.server.run_subprocess_with_streaming')
    async def test_scrape_docs_with_enhance_local(self, mock_streaming):
        """Test scraping with local enhancement"""
        # Mock successful subprocess run with streaming
        mock_streaming.return_value = ("Scraping with enhancement", "", 0)

        args = {
            "config_path": str(self.config_path),
            "enhance_local": True
        }

        result = await skill_seeker_server.scrape_docs_tool(args)

        call_args = mock_streaming.call_args[0][0]
        self.assertIn("--enhance-local", call_args)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestPackageSkillTool(unittest.IsolatedAsyncioTestCase):
    """Test package_skill tool"""

    async def asyncSetUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create a mock skill directory
        self.skill_dir = Path("output/test-skill")
        self.skill_dir.mkdir(parents=True)
        (self.skill_dir / "SKILL.md").write_text("# Test Skill")
        (self.skill_dir / "references").mkdir()
        (self.skill_dir / "references/index.md").write_text("# Index")

    async def asyncTearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('subprocess.run')
    async def test_package_skill_success(self, mock_run):
        """Test successful skill packaging"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Package created: test-skill.zip"
        mock_run.return_value = mock_result

        args = {
            "skill_dir": str(self.skill_dir)
        }

        result = await skill_seeker_server.package_skill_tool(args)

        self.assertIsInstance(result, list)
        self.assertIn("test-skill", result[0].text)

    @patch('subprocess.run')
    async def test_package_skill_error(self, mock_run):
        """Test error handling in skill packaging"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Directory not found"
        mock_run.return_value = mock_result

        args = {
            "skill_dir": "nonexistent-dir"
        }

        result = await skill_seeker_server.package_skill_tool(args)

        self.assertIn("Error", result[0].text)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestListConfigsTool(unittest.IsolatedAsyncioTestCase):
    """Test list_configs tool"""

    async def asyncSetUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create test configs
        os.makedirs("configs", exist_ok=True)

        configs = [
            {
                "name": "test1",
                "description": "Test 1 skill",
                "base_url": "https://test1.dev/"
            },
            {
                "name": "test2",
                "description": "Test 2 skill",
                "base_url": "https://test2.dev/"
            }
        ]

        for config in configs:
            path = Path(f"configs/{config['name']}.json")
            with open(path, 'w') as f:
                json.dump(config, f)

    async def asyncTearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_list_configs_success(self):
        """Test listing all configs"""
        result = await skill_seeker_server.list_configs_tool({})

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], TextContent)
        self.assertIn("test1", result[0].text)
        self.assertIn("test2", result[0].text)
        self.assertIn("https://test1.dev/", result[0].text)
        self.assertIn("https://test2.dev/", result[0].text)

    async def test_list_configs_empty(self):
        """Test listing configs when directory is empty"""
        # Remove all configs
        for config_file in Path("configs").glob("*.json"):
            config_file.unlink()

        result = await skill_seeker_server.list_configs_tool({})

        self.assertIn("No config files found", result[0].text)

    async def test_list_configs_no_directory(self):
        """Test listing configs when directory doesn't exist"""
        # Remove configs directory
        shutil.rmtree("configs")

        result = await skill_seeker_server.list_configs_tool({})

        self.assertIn("No configs directory", result[0].text)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestValidateConfigTool(unittest.IsolatedAsyncioTestCase):
    """Test validate_config tool"""

    async def asyncSetUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        os.makedirs("configs", exist_ok=True)

    async def asyncTearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_validate_valid_config(self):
        """Test validating a valid config"""
        # Create valid config
        config_path = Path("configs/valid.json")
        valid_config = {
            "name": "valid-test",
            "base_url": "https://example.com/",
            "selectors": {
                "main_content": "article",
                "title": "h1",
                "code_blocks": "pre"
            },
            "rate_limit": 0.5,
            "max_pages": 100
        }
        with open(config_path, 'w') as f:
            json.dump(valid_config, f)

        args = {
            "config_path": str(config_path)
        }

        result = await skill_seeker_server.validate_config_tool(args)

        self.assertIsInstance(result, list)
        self.assertIn("✅", result[0].text)
        self.assertIn("valid", result[0].text.lower())

    async def test_validate_invalid_config(self):
        """Test validating an invalid config"""
        # Create invalid config (missing required fields)
        config_path = Path("configs/invalid.json")
        invalid_config = {
            "description": "Missing name field",
            "sources": [
                {"type": "invalid_type", "url": "https://example.com"}  # Invalid source type
            ]
        }
        with open(config_path, 'w') as f:
            json.dump(invalid_config, f)

        args = {
            "config_path": str(config_path)
        }

        result = await skill_seeker_server.validate_config_tool(args)

        # Should show error for invalid source type
        self.assertIn("❌", result[0].text)

    async def test_validate_nonexistent_config(self):
        """Test validating a nonexistent config"""
        args = {
            "config_path": "configs/nonexistent.json"
        }

        result = await skill_seeker_server.validate_config_tool(args)

        self.assertIn("Error", result[0].text)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestCallToolRouter(unittest.IsolatedAsyncioTestCase):
    """Test call_tool routing"""

    async def test_call_tool_unknown(self):
        """Test calling an unknown tool"""
        result = await skill_seeker_server.call_tool("unknown_tool", {})

        self.assertIsInstance(result, list)
        self.assertIn("Unknown tool", result[0].text)

    async def test_call_tool_exception_handling(self):
        """Test that exceptions are caught and returned as errors"""
        # Call with invalid arguments that should cause an exception
        result = await skill_seeker_server.call_tool("generate_config", {})

        self.assertIsInstance(result, list)
        self.assertIn("Error", result[0].text)


@unittest.skipUnless(MCP_AVAILABLE, "MCP package not installed")
class TestMCPServerIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests for MCP server"""

    async def test_full_workflow_simulation(self):
        """Test complete workflow: generate config -> validate -> estimate"""
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Step 1: Generate config using skill_seeker_server
            generate_args = {
                "name": "workflow-test",
                "url": "https://workflow-test.dev/",
                "description": "Workflow test skill"
            }
            result1 = await skill_seeker_server.generate_config_tool(generate_args)
            self.assertIn("✅", result1[0].text)

            # Step 2: Validate config
            validate_args = {
                "config_path": "configs/workflow-test.json"
            }
            result2 = await skill_seeker_server.validate_config_tool(validate_args)
            self.assertIn("✅", result2[0].text)

            # Step 3: List configs
            result3 = await skill_seeker_server.list_configs_tool({})
            self.assertIn("workflow-test", result3[0].text)

        finally:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
