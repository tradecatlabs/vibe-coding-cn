"""Test suite for Python package structure.

Tests that the package structure is correct and imports work properly.
This ensures modern Python packaging (src/ layout, pyproject.toml) is successful.
"""

import pytest
import sys
from pathlib import Path


class TestCliPackage:
    """Test skill_seekers.cli package structure and imports."""

    def test_cli_package_exists(self):
        """Test that skill_seekers.cli package can be imported."""
        import skill_seekers.cli
        assert skill_seekers.cli is not None

    def test_cli_has_version(self):
        """Test that skill_seekers.cli package has __version__."""
        import skill_seekers.cli
        assert hasattr(skill_seekers.cli, '__version__')
        assert skill_seekers.cli.__version__ == '2.0.0'

    def test_cli_has_all(self):
        """Test that skill_seekers.cli package has __all__ export list."""
        import skill_seekers.cli
        assert hasattr(skill_seekers.cli, '__all__')
        assert isinstance(skill_seekers.cli.__all__, list)
        assert len(skill_seekers.cli.__all__) > 0

    def test_llms_txt_detector_import(self):
        """Test that LlmsTxtDetector can be imported from skill_seekers.cli."""
        from skill_seekers.cli import LlmsTxtDetector
        assert LlmsTxtDetector is not None

    def test_llms_txt_downloader_import(self):
        """Test that LlmsTxtDownloader can be imported from skill_seekers.cli."""
        from skill_seekers.cli import LlmsTxtDownloader
        assert LlmsTxtDownloader is not None

    def test_llms_txt_parser_import(self):
        """Test that LlmsTxtParser can be imported from skill_seekers.cli."""
        from skill_seekers.cli import LlmsTxtParser
        assert LlmsTxtParser is not None

    def test_open_folder_import(self):
        """Test that open_folder can be imported from skill_seekers.cli (if utils exists)."""
        try:
            from skill_seekers.cli import open_folder
            # If import succeeds, function should not be None
            assert open_folder is not None
        except ImportError:
            # If utils.py doesn't exist, that's okay for now
            pytest.skip("utils.py not found, skipping open_folder test")

    def test_cli_exports_match_all(self):
        """Test that exported items in __all__ can actually be imported."""
        import skill_seekers.cli as cli
        for item_name in cli.__all__:
            if item_name == 'open_folder' and cli.open_folder is None:
                # open_folder might be None if utils doesn't exist
                continue
            assert hasattr(cli, item_name), f"{item_name} not found in cli package"


class TestMcpPackage:
    """Test skill_seekers.mcp package structure and imports."""

    def test_mcp_package_exists(self):
        """Test that skill_seekers.mcp package can be imported."""
        import skill_seekers.mcp
        assert skill_seekers.mcp is not None

    def test_mcp_has_version(self):
        """Test that skill_seekers.mcp package has __version__."""
        import skill_seekers.mcp
        assert hasattr(skill_seekers.mcp, '__version__')
        assert skill_seekers.mcp.__version__ == '2.0.0'

    def test_mcp_has_all(self):
        """Test that skill_seekers.mcp package has __all__ export list."""
        import skill_seekers.mcp
        assert hasattr(skill_seekers.mcp, '__all__')
        assert isinstance(skill_seekers.mcp.__all__, list)

    def test_mcp_tools_package_exists(self):
        """Test that skill_seekers.mcp.tools subpackage can be imported."""
        import skill_seekers.mcp.tools
        assert skill_seekers.mcp.tools is not None

    def test_mcp_tools_has_version(self):
        """Test that skill_seekers.mcp.tools has __version__."""
        import skill_seekers.mcp.tools
        assert hasattr(skill_seekers.mcp.tools, '__version__')
        assert skill_seekers.mcp.tools.__version__ == '2.0.0'


class TestPackageStructure:
    """Test overall package structure integrity (src/ layout)."""

    def test_cli_init_file_exists(self):
        """Test that src/skill_seekers/cli/__init__.py exists."""
        init_file = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'cli' / '__init__.py'
        assert init_file.exists(), "src/skill_seekers/cli/__init__.py not found"

    def test_mcp_init_file_exists(self):
        """Test that src/skill_seekers/mcp/__init__.py exists."""
        init_file = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'mcp' / '__init__.py'
        assert init_file.exists(), "src/skill_seekers/mcp/__init__.py not found"

    def test_mcp_tools_init_file_exists(self):
        """Test that src/skill_seekers/mcp/tools/__init__.py exists."""
        init_file = Path(__file__).parent.parent / 'src' / 'skill_seekers' / 'mcp' / 'tools' / '__init__.py'
        assert init_file.exists(), "src/skill_seekers/mcp/tools/__init__.py not found"

    def test_cli_init_has_docstring(self):
        """Test that skill_seekers.cli/__init__.py has a module docstring."""
        import skill_seekers.cli
        assert skill_seekers.cli.__doc__ is not None
        assert len(skill_seekers.cli.__doc__) > 50  # Should have substantial documentation

    def test_mcp_init_has_docstring(self):
        """Test that skill_seekers.mcp/__init__.py has a module docstring."""
        import skill_seekers.mcp
        assert skill_seekers.mcp.__doc__ is not None
        assert len(skill_seekers.mcp.__doc__) > 50  # Should have substantial documentation


class TestImportPatterns:
    """Test that various import patterns work correctly."""

    def test_direct_module_import(self):
        """Test importing modules directly."""
        from skill_seekers.cli import llms_txt_detector
        from skill_seekers.cli import llms_txt_downloader
        from skill_seekers.cli import llms_txt_parser
        assert llms_txt_detector is not None
        assert llms_txt_downloader is not None
        assert llms_txt_parser is not None

    def test_class_import_from_package(self):
        """Test importing classes from package."""
        from skill_seekers.cli import LlmsTxtDetector, LlmsTxtDownloader, LlmsTxtParser
        assert LlmsTxtDetector.__name__ == 'LlmsTxtDetector'
        assert LlmsTxtDownloader.__name__ == 'LlmsTxtDownloader'
        assert LlmsTxtParser.__name__ == 'LlmsTxtParser'

    def test_package_level_import(self):
        """Test importing entire packages."""
        import skill_seekers
        import skill_seekers.cli
        import skill_seekers.mcp
        import skill_seekers.mcp.tools
        assert 'skill_seekers' in sys.modules
        assert 'skill_seekers.cli' in sys.modules
        assert 'skill_seekers.mcp' in sys.modules
        assert 'skill_seekers.mcp.tools' in sys.modules


class TestBackwardsCompatibility:
    """Test that existing code patterns still work."""

    def test_direct_file_import_still_works(self):
        """Test that direct file imports still work (backwards compatible)."""
        # This ensures we didn't break existing code
        from skill_seekers.cli.llms_txt_detector import LlmsTxtDetector
        from skill_seekers.cli.llms_txt_downloader import LlmsTxtDownloader
        from skill_seekers.cli.llms_txt_parser import LlmsTxtParser
        assert LlmsTxtDetector is not None
        assert LlmsTxtDownloader is not None
        assert LlmsTxtParser is not None

    def test_module_path_import_still_works(self):
        """Test that full module path imports still work."""
        import skill_seekers.cli.llms_txt_detector
        import skill_seekers.cli.llms_txt_downloader
        import skill_seekers.cli.llms_txt_parser
        assert skill_seekers.cli.llms_txt_detector is not None
        assert skill_seekers.cli.llms_txt_downloader is not None
        assert skill_seekers.cli.llms_txt_parser is not None


class TestRootPackage:
    """Test root skill_seekers package."""

    def test_root_package_exists(self):
        """Test that skill_seekers root package can be imported."""
        import skill_seekers
        assert skill_seekers is not None

    def test_root_has_version(self):
        """Test that skill_seekers root package has __version__."""
        import skill_seekers
        assert hasattr(skill_seekers, '__version__')
        assert skill_seekers.__version__ == '2.0.0'

    def test_root_has_metadata(self):
        """Test that skill_seekers root package has metadata."""
        import skill_seekers
        assert hasattr(skill_seekers, '__author__')
        assert hasattr(skill_seekers, '__license__')
        assert skill_seekers.__license__ == 'MIT'


class TestCLIEntryPoints:
    """Test that CLI entry points are properly configured."""

    def test_main_cli_module_exists(self):
        """Test that main.py module exists and can be imported."""
        from skill_seekers.cli import main
        assert main is not None
        assert hasattr(main, 'main')
        assert callable(main.main)

    def test_main_cli_has_parser(self):
        """Test that main.py has parser creation function."""
        from skill_seekers.cli.main import create_parser
        parser = create_parser()
        assert parser is not None
        # Test that main subcommands are configured
        assert parser.prog == 'skill-seekers'
