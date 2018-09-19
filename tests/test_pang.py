#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pang` package."""


import unittest
from click.testing import CliRunner

from pang import pang # noqa
from pang import cli


class TestPang(unittest.TestCase):
    """Tests for `pang` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
