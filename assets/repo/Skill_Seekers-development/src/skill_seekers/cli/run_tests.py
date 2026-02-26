#!/usr/bin/env python3
"""
Test Runner for Skill Seeker
Runs all test suites and generates a comprehensive test report
"""

import sys
import unittest
import os
from io import StringIO
from pathlib import Path


class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result class with colored output"""

    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.append(('PASS', test))
        if self.showAll:
            self.stream.write(f"{self.GREEN}✓ PASS{self.RESET}\n")
        elif self.dots:
            self.stream.write(f"{self.GREEN}.{self.RESET}")
            self.stream.flush()

    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.append(('ERROR', test))
        if self.showAll:
            self.stream.write(f"{self.RED}✗ ERROR{self.RESET}\n")
        elif self.dots:
            self.stream.write(f"{self.RED}E{self.RESET}")
            self.stream.flush()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append(('FAIL', test))
        if self.showAll:
            self.stream.write(f"{self.RED}✗ FAIL{self.RESET}\n")
        elif self.dots:
            self.stream.write(f"{self.RED}F{self.RESET}")
            self.stream.flush()

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_results.append(('SKIP', test))
        if self.showAll:
            self.stream.write(f"{self.YELLOW}⊘ SKIP{self.RESET}\n")
        elif self.dots:
            self.stream.write(f"{self.YELLOW}s{self.RESET}")
            self.stream.flush()


class ColoredTextTestRunner(unittest.TextTestRunner):
    """Custom test runner with colored output"""
    resultclass = ColoredTextTestResult


def discover_tests(test_dir='tests'):
    """Discover all test files in the tests directory"""
    loader = unittest.TestLoader()
    start_dir = test_dir
    pattern = 'test_*.py'

    suite = loader.discover(start_dir, pattern=pattern)
    return suite


def run_specific_suite(suite_name):
    """Run a specific test suite"""
    loader = unittest.TestLoader()

    suite_map = {
        'config': 'tests.test_config_validation',
        'features': 'tests.test_scraper_features',
        'integration': 'tests.test_integration'
    }

    if suite_name not in suite_map:
        print(f"Unknown test suite: {suite_name}")
        print(f"Available suites: {', '.join(suite_map.keys())}")
        return None

    module_name = suite_map[suite_name]
    try:
        suite = loader.loadTestsFromName(module_name)
        return suite
    except Exception as e:
        print(f"Error loading test suite '{suite_name}': {e}")
        return None


def print_summary(result):
    """Print a detailed test summary"""
    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors) - len(result.skipped)
    failed = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    # Overall stats
    print(f"\n{ColoredTextTestResult.BOLD}Total Tests:{ColoredTextTestResult.RESET} {total}")
    print(f"{ColoredTextTestResult.GREEN}✓ Passed:{ColoredTextTestResult.RESET} {passed}")
    if failed > 0:
        print(f"{ColoredTextTestResult.RED}✗ Failed:{ColoredTextTestResult.RESET} {failed}")
    if errors > 0:
        print(f"{ColoredTextTestResult.RED}✗ Errors:{ColoredTextTestResult.RESET} {errors}")
    if skipped > 0:
        print(f"{ColoredTextTestResult.YELLOW}⊘ Skipped:{ColoredTextTestResult.RESET} {skipped}")

    # Success rate
    if total > 0:
        success_rate = (passed / total) * 100
        color = ColoredTextTestResult.GREEN if success_rate == 100 else \
                ColoredTextTestResult.YELLOW if success_rate >= 80 else \
                ColoredTextTestResult.RED
        print(f"\n{color}Success Rate: {success_rate:.1f}%{ColoredTextTestResult.RESET}")

    # Category breakdown
    if hasattr(result, 'test_results'):
        print(f"\n{ColoredTextTestResult.BOLD}Test Breakdown by Category:{ColoredTextTestResult.RESET}")

        categories = {}
        for status, test in result.test_results:
            test_name = str(test)
            # Extract test class name
            if '.' in test_name:
                class_name = test_name.split('.')[0].split()[-1]
                if class_name not in categories:
                    categories[class_name] = {'PASS': 0, 'FAIL': 0, 'ERROR': 0, 'SKIP': 0}
                categories[class_name][status] += 1

        for category, stats in sorted(categories.items()):
            total_cat = sum(stats.values())
            passed_cat = stats['PASS']
            print(f"  {category}: {passed_cat}/{total_cat} passed")

    print("\n" + "="*70)

    # Return status
    return failed == 0 and errors == 0


def main():
    """Main test runner"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Run tests for Skill Seeker',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--suite', '-s', type=str,
                       help='Run specific test suite (config, features, integration)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output (show each test)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet output (minimal output)')
    parser.add_argument('--failfast', '-f', action='store_true',
                       help='Stop on first failure')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all available tests')

    args = parser.parse_args()

    # Set verbosity
    verbosity = 1
    if args.verbose:
        verbosity = 2
    elif args.quiet:
        verbosity = 0

    print(f"\n{ColoredTextTestResult.BOLD}{'='*70}{ColoredTextTestResult.RESET}")
    print(f"{ColoredTextTestResult.BOLD}SKILL SEEKER TEST SUITE{ColoredTextTestResult.RESET}")
    print(f"{ColoredTextTestResult.BOLD}{'='*70}{ColoredTextTestResult.RESET}\n")

    # Discover or load specific suite
    if args.suite:
        print(f"Running test suite: {ColoredTextTestResult.BLUE}{args.suite}{ColoredTextTestResult.RESET}\n")
        suite = run_specific_suite(args.suite)
        if suite is None:
            return 1
    else:
        print(f"Running {ColoredTextTestResult.BLUE}all tests{ColoredTextTestResult.RESET}\n")
        suite = discover_tests()

    # List tests
    if args.list:
        print("\nAvailable tests:\n")
        for test_group in suite:
            for test in test_group:
                print(f"  - {test}")
        print()
        return 0

    # Run tests
    runner = ColoredTextTestRunner(
        verbosity=verbosity,
        failfast=args.failfast
    )

    result = runner.run(suite)

    # Print summary
    success = print_summary(result)

    # Return appropriate exit code
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
