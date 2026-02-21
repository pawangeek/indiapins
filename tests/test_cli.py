#!/usr/bin/env python

"""Exhaustive tests for `indiapins` CLI."""

import pytest
from click.testing import CliRunner

from indiapins import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestCLI:
    """Tests for the CLI entry point."""

    def test_cli_runs_successfully(self, runner):
        result = runner.invoke(cli.main)
        assert result.exit_code == 0

    def test_cli_output_contains_module_reference(self, runner):
        result = runner.invoke(cli.main)
        assert "indiapins.cli.main" in result.output

    def test_cli_help_flag(self, runner):
        result = runner.invoke(cli.main, ["--help"])
        assert result.exit_code == 0
        assert "--help" in result.output
        assert "Show this message and exit." in result.output

    def test_cli_help_contains_description(self, runner):
        result = runner.invoke(cli.main, ["--help"])
        assert "Console script for indiapins" in result.output

    def test_cli_no_exception(self, runner):
        result = runner.invoke(cli.main)
        assert result.exception is None

    def test_cli_help_no_exception(self, runner):
        result = runner.invoke(cli.main, ["--help"])
        assert result.exception is None

    def test_cli_output_mentions_click_docs(self, runner):
        result = runner.invoke(cli.main)
        assert "click" in result.output.lower()
