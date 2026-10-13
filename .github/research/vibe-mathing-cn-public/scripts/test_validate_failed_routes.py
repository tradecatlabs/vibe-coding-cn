#!/usr/bin/env python3
"""Regression tests for portable RFC3339 parsing in failed-route validation."""
from __future__ import annotations

import unittest

from validate_failed_routes import parse_recorded_at


class FailedRouteTimestampTests(unittest.TestCase):
    def test_accepts_utc_z_on_all_supported_python_versions(self) -> None:
        parsed = parse_recorded_at("2026-09-01T00:52:27Z")
        self.assertIsNotNone(parsed.tzinfo)
        self.assertEqual(parsed.utcoffset().total_seconds(), 0)

    def test_accepts_explicit_timezone_offset(self) -> None:
        parsed = parse_recorded_at("2026-09-01T08:52:27+08:00")
        self.assertEqual(parsed.utcoffset().total_seconds(), 8 * 3600)

    def test_rejects_naive_timestamp(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone"):
            parse_recorded_at("2026-09-01T00:52:27")

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(ValueError):
            parse_recorded_at(None)


if __name__ == "__main__":
    unittest.main()
