"""
Tests for terminal detection functionality in enhance_skill_local.py

This module tests the detect_terminal_app() function and terminal launching logic
to ensure correct terminal selection across different environments.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_seekers.cli.enhance_skill_local import detect_terminal_app, LocalSkillEnhancer


class TestDetectTerminalApp(unittest.TestCase):
    """Test the detect_terminal_app() function."""

    original_skill_seeker: str | None = None
    original_term_program: str | None = None

    def setUp(self):
        """Save original environment variables."""
        self.original_skill_seeker = os.environ.get('SKILL_SEEKER_TERMINAL')
        self.original_term_program = os.environ.get('TERM_PROGRAM')

    def tearDown(self):
        """Restore original environment variables."""
        # Remove test env vars
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']
        if 'TERM_PROGRAM' in os.environ:
            del os.environ['TERM_PROGRAM']

        # Restore originals if they existed
        if self.original_skill_seeker is not None:
            os.environ['SKILL_SEEKER_TERMINAL'] = self.original_skill_seeker
        if self.original_term_program is not None:
            os.environ['TERM_PROGRAM'] = self.original_term_program

    # HIGH PRIORITY TESTS

    def test_detect_terminal_with_skill_seeker_env(self):
        """Test that SKILL_SEEKER_TERMINAL env var takes highest priority."""
        os.environ['SKILL_SEEKER_TERMINAL'] = 'Ghostty'

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'Ghostty')
        self.assertEqual(detection_method, 'SKILL_SEEKER_TERMINAL')

    def test_detect_terminal_with_term_program_known(self):
        """Test detection from TERM_PROGRAM with known terminal (iTerm)."""
        # Ensure SKILL_SEEKER_TERMINAL is not set
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']

        os.environ['TERM_PROGRAM'] = 'iTerm.app'

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'iTerm')
        self.assertEqual(detection_method, 'TERM_PROGRAM')

    def test_detect_terminal_with_term_program_ghostty(self):
        """Test detection from TERM_PROGRAM with Ghostty terminal."""
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']

        os.environ['TERM_PROGRAM'] = 'ghostty'

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'Ghostty')
        self.assertEqual(detection_method, 'TERM_PROGRAM')

    def test_detect_terminal_with_term_program_apple_terminal(self):
        """Test detection from TERM_PROGRAM with Apple Terminal."""
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']

        os.environ['TERM_PROGRAM'] = 'Apple_Terminal'

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'Terminal')
        self.assertEqual(detection_method, 'TERM_PROGRAM')

    def test_detect_terminal_with_term_program_wezterm(self):
        """Test detection from TERM_PROGRAM with WezTerm."""
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']

        os.environ['TERM_PROGRAM'] = 'WezTerm'

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'WezTerm')
        self.assertEqual(detection_method, 'TERM_PROGRAM')

    def test_detect_terminal_with_term_program_unknown(self):
        """Test fallback behavior when TERM_PROGRAM is unknown (e.g., IDE terminals)."""
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']

        os.environ['TERM_PROGRAM'] = 'zed'

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'Terminal')
        self.assertEqual(detection_method, 'unknown TERM_PROGRAM (zed)')

    def test_detect_terminal_default_fallback(self):
        """Test default fallback when no environment variables are set."""
        # Remove both env vars
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']
        if 'TERM_PROGRAM' in os.environ:
            del os.environ['TERM_PROGRAM']

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'Terminal')
        self.assertEqual(detection_method, 'default')

    def test_detect_terminal_priority_order(self):
        """Test that SKILL_SEEKER_TERMINAL takes priority over TERM_PROGRAM."""
        os.environ['SKILL_SEEKER_TERMINAL'] = 'Ghostty'
        os.environ['TERM_PROGRAM'] = 'iTerm.app'

        terminal_app, detection_method = detect_terminal_app()

        # SKILL_SEEKER_TERMINAL should win
        self.assertEqual(terminal_app, 'Ghostty')
        self.assertEqual(detection_method, 'SKILL_SEEKER_TERMINAL')

    @patch('subprocess.Popen')
    def test_subprocess_popen_called_with_correct_args(self, mock_popen):
        """Test that subprocess.Popen is called with correct arguments on macOS."""
        # Only test on macOS
        if sys.platform != 'darwin':
            self.skipTest("This test only runs on macOS")

        # Setup
        os.environ['SKILL_SEEKER_TERMINAL'] = 'Ghostty'

        # Create a test skill directory with minimal setup
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / 'test_skill'
            skill_dir.mkdir()

            # Create references directory (required by LocalSkillEnhancer)
            (skill_dir / 'references').mkdir()
            (skill_dir / 'references' / 'test.md').write_text('# Test')

            # Create SKILL.md (required)
            (skill_dir / 'SKILL.md').write_text('---\nname: test\n---\n# Test')

            # Mock Popen to prevent actual terminal launch
            mock_popen.return_value = MagicMock()

            # Run enhancer in interactive mode (not headless)
            enhancer = LocalSkillEnhancer(skill_dir)
            result = enhancer.run(headless=False)

            # Verify Popen was called
            self.assertTrue(mock_popen.called)

            # Verify call arguments
            call_args = mock_popen.call_args[0][0]
            self.assertEqual(call_args[0], 'open')
            self.assertEqual(call_args[1], '-a')
            self.assertEqual(call_args[2], 'Ghostty')
            # call_args[3] should be the script file path
            self.assertTrue(call_args[3].endswith('.sh'))

    # MEDIUM PRIORITY TESTS

    def test_detect_terminal_whitespace_handling(self):
        """Test that whitespace is stripped from environment variables."""
        os.environ['SKILL_SEEKER_TERMINAL'] = '  Ghostty  '

        terminal_app, detection_method = detect_terminal_app()

        self.assertEqual(terminal_app, 'Ghostty')
        self.assertEqual(detection_method, 'SKILL_SEEKER_TERMINAL')

    def test_detect_terminal_empty_string_env_vars(self):
        """Test that empty string env vars fall through to next priority."""
        os.environ['SKILL_SEEKER_TERMINAL'] = ''
        os.environ['TERM_PROGRAM'] = 'iTerm.app'

        terminal_app, detection_method = detect_terminal_app()

        # Should skip empty SKILL_SEEKER_TERMINAL and use TERM_PROGRAM
        self.assertEqual(terminal_app, 'iTerm')
        self.assertEqual(detection_method, 'TERM_PROGRAM')

    def test_detect_terminal_empty_string_both_vars(self):
        """Test that empty strings on both vars falls back to default."""
        os.environ['SKILL_SEEKER_TERMINAL'] = ''
        os.environ['TERM_PROGRAM'] = ''

        terminal_app, detection_method = detect_terminal_app()

        # Should fall back to default
        self.assertEqual(terminal_app, 'Terminal')
        # Empty TERM_PROGRAM should be treated as not set
        self.assertEqual(detection_method, 'default')

    @patch('subprocess.Popen')
    def test_terminal_launch_error_handling(self, mock_popen):
        """Test error handling when terminal launch fails."""
        # Only test on macOS
        if sys.platform != 'darwin':
            self.skipTest("This test only runs on macOS")

        # Setup Popen to raise exception
        mock_popen.side_effect = Exception("Terminal not found")

        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / 'test_skill'
            skill_dir.mkdir()
            (skill_dir / 'references').mkdir()
            (skill_dir / 'references' / 'test.md').write_text('# Test')
            (skill_dir / 'SKILL.md').write_text('---\nname: test\n---\n# Test')

            enhancer = LocalSkillEnhancer(skill_dir)

            # Capture stdout to check error message
            from io import StringIO
            captured_output = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured_output

            # Run in interactive mode (not headless) to test terminal launch
            result = enhancer.run(headless=False)

            # Restore stdout
            sys.stdout = old_stdout

            # Should return False on error
            self.assertFalse(result)

            # Should print error message
            output = captured_output.getvalue()
            self.assertIn('Error launching', output)

    def test_output_message_unknown_terminal(self):
        """Test that unknown terminal prints warning message."""
        if sys.platform != 'darwin':
            self.skipTest("This test only runs on macOS")

        os.environ['TERM_PROGRAM'] = 'vscode'
        if 'SKILL_SEEKER_TERMINAL' in os.environ:
            del os.environ['SKILL_SEEKER_TERMINAL']

        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / 'test_skill'
            skill_dir.mkdir()
            (skill_dir / 'references').mkdir()
            (skill_dir / 'references' / 'test.md').write_text('# Test')
            (skill_dir / 'SKILL.md').write_text('---\nname: test\n---\n# Test')

            enhancer = LocalSkillEnhancer(skill_dir)

            # Capture stdout
            from io import StringIO
            captured_output = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured_output

            # Mock Popen to prevent actual launch
            with patch('subprocess.Popen') as mock_popen:
                mock_popen.return_value = MagicMock()
                # Run in interactive mode (not headless) to test terminal detection
                enhancer.run(headless=False)

            # Restore stdout
            sys.stdout = old_stdout

            output = captured_output.getvalue()

            # Should contain warning about unknown terminal
            self.assertIn('⚠️', output)
            self.assertIn('unknown TERM_PROGRAM', output)
            self.assertIn('vscode', output)
            self.assertIn('Using Terminal.app as fallback', output)


class TestTerminalMapCompleteness(unittest.TestCase):
    """Test that TERMINAL_MAP covers all documented terminals."""

    def test_terminal_map_has_all_documented_terminals(self):
        """Verify TERMINAL_MAP contains all terminals mentioned in documentation."""
        from skill_seekers.cli.enhance_skill_local import detect_terminal_app

        # Get the TERMINAL_MAP from the function's scope
        # We need to test this indirectly by checking each known terminal

        known_terminals = [
            ('Apple_Terminal', 'Terminal'),
            ('iTerm.app', 'iTerm'),
            ('ghostty', 'Ghostty'),
            ('WezTerm', 'WezTerm'),
        ]

        for term_program_value, expected_app_name in known_terminals:
            # Set TERM_PROGRAM and verify detection
            os.environ['TERM_PROGRAM'] = term_program_value
            if 'SKILL_SEEKER_TERMINAL' in os.environ:
                del os.environ['SKILL_SEEKER_TERMINAL']

            terminal_app, detection_method = detect_terminal_app()

            self.assertEqual(
                terminal_app,
                expected_app_name,
                f"TERM_PROGRAM='{term_program_value}' should map to '{expected_app_name}'"
            )
            self.assertEqual(detection_method, 'TERM_PROGRAM')


if __name__ == '__main__':
    unittest.main()
