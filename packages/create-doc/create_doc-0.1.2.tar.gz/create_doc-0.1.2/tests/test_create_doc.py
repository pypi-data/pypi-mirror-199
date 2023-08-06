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

    def test_init_app(self):
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

    def test_gpt_process_all(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.gpt_process, ['all'])
        assert result.exit_code == 0

    def test_gpt_process_forms(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.gpt_process, ['forms'])
        assert result.exit_code == 0

    def test_gpt_process_modules(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.gpt_process, ['modules'])
        assert result.exit_code == 0

    def test_gpt_process_unknown(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.gpt_process, ['unknown'])
        assert 'Processor unknown not found' in result.output

    def test_process_dependencies(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.analyze_dependencies)
        assert result.exit_code == 0

    def test_process_dependencies_typescript(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.analyze_dependencies, ['typescript'])
        assert result.exit_code == 0

    def test_process_dependencies_unknown(self):
        """Test the CLI."""

        runner = CliRunner()
        if not os.path.exists('./.create_doc.json'):
            result = runner.invoke(cli.init)

        runner = CliRunner()
        result = runner.invoke(cli.analyze_dependencies, ['unknown'])
        assert 'Processor unknown not found' in result.output

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

    def test_gpt_analyze_forms_files(self):
        """Test gpt analyze html files."""
        config = cli.get_config()
        processor = config['gpt_processors'][0]
        gpt.init_env()
        path = processor['input_paths'][0]
        output_path = config['output_path'] + '/' + processor['output_sub_path']
        result = gpt.analyze_files(config['project_root_path'], path, output_path,
                                   processor['gpt_model_id'],
                                   processor['gpt_model_token_limit'], processor['gpt_prompts'],
                                   processor['angular_skip_html_router_outlet'],
                                   processor['angular_router_outlet_message'],
                                   processor['content_title'], processor['file_extensions'],
                                   processor['add_dependency_links'], processor['add_file_path'],
                                   processor['dependency_link_text']
                                   )
        assert result == 0

    def test_process_dependencies(self):
        """Test process dependencies."""
        config = cli.get_config()
        processor = config['dependency_processors'][0]
        project_directory_path = config['project_root_path']
        output_path = config['output_path'] + '/' + processor['output_sub_path']
        path = processor['input_paths'][0]
        result = analyze_module_dependencies.process_directory_dependencies(config['project_root_path'], path,
                                                                            output_path,
                                                                            processor['summary_depth'],
                                                                            processor['include_only'])
        assert result == 0

    def test_gpt_get_all_files_in_directory_and_subdirectories(self):
        """Test gpt get all files in directory and subdirectories."""
        config = cli.get_config()
        result = gpt.get_all_files_in_directory_and_subdirectories(config['project_root_path'],
                                                                   ['.html', '.ts'])
        assert result is not None
