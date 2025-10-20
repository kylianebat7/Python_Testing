import pytest
import subprocess
import sys
from unittest.mock import patch, MagicMock
from check_coverage import check_coverage, main


class TestCheckCoverage:
    @patch('subprocess.run')
    def test_check_coverage_success(self, mock_run):
        # Simuler un succès avec couverture de 80%
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "TOTAL                          80%  80%\n"
        mock_run.return_value = mock_result

        result = check_coverage(60)
        assert result == True

    @patch('subprocess.run')
    def test_check_coverage_failure_returncode(self, mock_run):
        # Simuler un échec des tests
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "Tests failed"
        mock_run.return_value = mock_result

        result = check_coverage(60)
        assert result == False

    @patch('subprocess.run')
    def test_check_coverage_insufficient_coverage(self, mock_run):
        # Simuler une couverture insuffisante
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "TOTAL                          50%  50%\n"
        mock_run.return_value = mock_result

        result = check_coverage(60)
        assert result == False

    @patch('subprocess.run')
    def test_check_coverage_no_coverage_line(self, mock_run):
        # Simuler absence de ligne de couverture
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "No coverage info"
        mock_run.return_value = mock_result

        result = check_coverage(60)
        assert result == False

    @patch('check_coverage.check_coverage')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_args, mock_check):
        mock_check.return_value = True
        mock_args.return_value = MagicMock(minimum=60)
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0

    @patch('check_coverage.check_coverage')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_failure(self, mock_args, mock_check):
        mock_check.return_value = False
        mock_args.return_value = MagicMock(minimum=60)
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
