import unittest
from unittest.mock import patch, MagicMock
import os
from virtmaker.runners.importers.isoboot import ISOBoot

class TestISOBoot(unittest.TestCase):

    @patch('shutil.move')
    @patch('os.path.isfile')
    @patch('virtmaker.utils.cmd.runCmd')
    @patch('shutil.which')
    def test_prep_file_http_url(self, mock_which, mock_runCmd, mock_isfile, mock_move):
        mock_which.return_value = 'pv'
        mock_runCmd.return_value = True
        mock_isfile.side_effect = [False, True]
        spec_config = MagicMock()
        isoboot = ISOBoot(spec_config)
        isoboot._cache_dir = '/tmp'
        url = 'http://example.com/test.iso'
        iso_filepath, retval = isoboot._prep_file(url)
        self.assertEqual(iso_filepath, '/tmp/test.iso')
        self.assertTrue(retval)
        mock_runCmd.assert_called_once()
        mock_move.assert_called_once_with('/tmp/test.iso_in-progress', '/tmp/test.iso')

    @patch('shutil.move')
    @patch('os.path.isfile')
    @patch('virtmaker.utils.cmd.runCmd')
    @patch('shutil.which')
    def test_prep_file_file_url(self, mock_which, mock_runCmd, mock_isfile, mock_move):
        mock_which.return_value = 'pv'
        mock_runCmd.return_value = True
        mock_isfile.side_effect = [False, True]
        spec_config = MagicMock()
        isoboot = ISOBoot(spec_config)
        isoboot._cache_dir = '/tmp'
        url = 'file:///path/to/test.iso'
        iso_filepath, retval = isoboot._prep_file(url)
        self.assertEqual(iso_filepath, '/tmp/test.iso')
        self.assertTrue(retval)
        mock_runCmd.assert_called_once()
        mock_move.assert_called_once_with('/tmp/test.iso_in-progress', '/tmp/test.iso')

    @patch('shutil.move')
    @patch('os.path.isfile')
    @patch('virtmaker.utils.cmd.runCmd')
    @patch('shutil.which')
    def test_prep_file_gz_file(self, mock_which, mock_runCmd, mock_isfile, mock_move):
        mock_which.return_value = 'pv'
        mock_runCmd.return_value = True
        mock_isfile.side_effect = [False, True]
        spec_config = MagicMock()
        isoboot = ISOBoot(spec_config)
        isoboot._cache_dir = '/tmp'
        url = 'http://example.com/test.iso.gz'
        iso_filepath, retval = isoboot._prep_file(url)
        self.assertEqual(iso_filepath, '/tmp/test.iso')
        self.assertTrue(retval)
        mock_runCmd.assert_called_once()
        mock_move.assert_called_once_with('/tmp/test.iso_in-progress', '/tmp/test.iso')

    @patch('os.path.isfile')
    def test_prep_file_already_exists(self, mock_isfile):
        mock_isfile.return_value = True
        spec_config = MagicMock()
        isoboot = ISOBoot(spec_config)
        isoboot._cache_dir = '/tmp'
        url = 'http://example.com/test.iso'
        iso_filepath, retval = isoboot._prep_file(url)
        self.assertEqual(iso_filepath, '/tmp/test.iso')
        self.assertTrue(retval)