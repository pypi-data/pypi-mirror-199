#!/usr/bin/env python

"""Tests for `create_doc` package."""

import unittest
from click.testing import CliRunner

from create_doc import cli
from create_doc import analyze_with_gpt as gpt
from create_doc import analyze_module_dependencies
import os


class TestCreate_doc(unittest.TestCase):
    """Tests for `create_doc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""

        # if file .create_doc.json does exist, delete it
        if os.path.exists('./.create_doc.json'):
            os.remove('./.create_doc.json')

        runner = CliRunner()
        result = runner.invoke(cli.init)
        assert result.exit_code == 0
        assert 'Initializing' in result.output
        help_result = runner.invoke(cli.init, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_os_environment(self):
        """Test the os environment."""
        result = cli.check_openapi_key()
        assert result

    def test_read_config_file(self):
        """Test reading config file."""
        result = cli.read_config_file()
        assert result

    def test_get_config(self):
        """Test getting config."""
        result = cli.get_config()
        assert result

    def test_gpt_init_env(self):
        """Test gpt init env."""
        result = gpt.init_env()
        assert result is not None

    def test_gpt_analyze_html_files(self):
        """Test gpt analyze html files."""
        config = cli.get_config()
        gpt.init_env()
        result = gpt.analyze_html_files(config['project_root_path'], config['project_forms_paths'][0],
                                        config['output_path'], config['gpt_model_id'], config['gpt_model_token_limit'],
                                        config['gpt_prompt_html'], config['gpt_skip_html_router_outlet'],
                                        config['html_router_outlet_message'], config['content_title'])
        assert result == 0

    def test_process_dependencies(self):
        """Test process dependencies."""
        config = cli.get_config()
        project_directory_path = config['project_root_path']
        webapp_paths = config['project_webapp_paths'][0]
        output_path = config['output_path']
        result = analyze_module_dependencies.process_directory_dependencies(project_directory_path, webapp_paths,
                                                                            output_path)
        assert result == 0
