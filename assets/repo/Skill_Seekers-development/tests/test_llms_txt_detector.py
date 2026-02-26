import pytest
from unittest.mock import patch, Mock
from skill_seekers.cli.llms_txt_detector import LlmsTxtDetector

def test_detect_llms_txt_variants():
    """Test detection of llms.txt file variants"""
    detector = LlmsTxtDetector("https://hono.dev/docs")

    with patch('skill_seekers.cli.llms_txt_detector.requests.head') as mock_head:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        variants = detector.detect()

        assert variants is not None
        assert variants['url'] == 'https://hono.dev/llms-full.txt'
        assert variants['variant'] == 'full'
        mock_head.assert_called()

def test_detect_no_llms_txt():
    """Test detection when no llms.txt file exists"""
    detector = LlmsTxtDetector("https://example.com/docs")

    with patch('skill_seekers.cli.llms_txt_detector.requests.head') as mock_head:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response

        variants = detector.detect()

        assert variants is None
        assert mock_head.call_count == 3  # Should try all three variants

def test_url_parsing_with_complex_paths():
    """Test URL parsing handles non-standard paths correctly"""
    detector = LlmsTxtDetector("https://example.com/docs/v2/guide")

    with patch('skill_seekers.cli.llms_txt_detector.requests.head') as mock_head:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        variants = detector.detect()

        assert variants is not None
        assert variants['url'] == 'https://example.com/llms-full.txt'
        mock_head.assert_called_with(
            'https://example.com/llms-full.txt',
            timeout=5,
            allow_redirects=True
        )

def test_detect_all_variants():
    """Test detecting all llms.txt variants"""
    detector = LlmsTxtDetector("https://hono.dev/docs")

    with patch('skill_seekers.cli.llms_txt_detector.requests.head') as mock_head:
        # Mock responses for different variants
        def mock_response(url, **kwargs):
            response = Mock()
            # All 3 variants exist for Hono
            if 'llms-full.txt' in url or 'llms.txt' in url or 'llms-small.txt' in url:
                response.status_code = 200
            else:
                response.status_code = 404
            return response

        mock_head.side_effect = mock_response

        variants = detector.detect_all()

        assert len(variants) == 3
        assert any(v['variant'] == 'full' for v in variants)
        assert any(v['variant'] == 'standard' for v in variants)
        assert any(v['variant'] == 'small' for v in variants)
        assert all('url' in v for v in variants)
