import unittest
import os
import sys
from unittest.mock import patch
import numpy as np
from io import StringIO

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from parse_dynalog_pylinac import accumulate_fluence, main

class TestAccumulateFluence(unittest.TestCase):
    def test_accumulate_fluence_no_files(self):
        actual, expected = accumulate_fluence([])
        self.assertIsNone(actual)
        self.assertIsNone(expected)

    @patch('parse_dynalog_pylinac.load_log')
    def test_accumulate_fluence_single_file(self, mock_load_log):
        class MockFluenceMap:
            def calc_map(self):
                return np.ones((4,4))

        class MockFluence:
            @property
            def actual(self):
                return MockFluenceMap()

            @property
            def expected(self):
                return MockFluenceMap()

        class MockLog:
            @property
            def fluence(self):
                return MockFluence()

        mock_load_log.return_value = MockLog()
        fake_paths = ["fake_file.dlg"]
        actual, expected = accumulate_fluence(fake_paths)
        self.assertIsNotNone(actual)
        self.assertIsNotNone(expected)
        self.assertEqual(actual.shape, (4,4))
        self.assertEqual(expected.shape, (4,4))
        self.assertEqual(actual.sum(), 16.0)
        self.assertEqual(expected.sum(), 16.0)

    @patch('parse_dynalog_pylinac.load_log')
    def test_accumulate_fluence_multiple_files(self, mock_load_log):
        class MockFluenceMap:
            def calc_map(self):
                return np.ones((3,3))

        class MockFluence:
            @property
            def actual(self):
                return MockFluenceMap()

            @property
            def expected(self):
                return MockFluenceMap()

        class MockLog:
            @property
            def fluence(self):
                return MockFluence()

        mock_load_log.return_value = MockLog()
        fake_paths = ["file1.dlg", "file2.dlg"]
        actual, expected = accumulate_fluence(fake_paths)
        self.assertEqual(actual.shape, (3,3))
        self.assertEqual(expected.shape, (3,3))
        self.assertEqual(actual.sum(), 18.0)
        self.assertEqual(expected.sum(), 18.0)

class TestMainIntegration(unittest.TestCase):
    @patch('parse_dynalog_pylinac.accumulate_fluence')
    def test_main_output(self, mock_accumulate):
        mock_accumulate.return_value = (
            np.full((2, 2), 2.0),
            np.full((2, 2), 1.0),
        )
        original_stdout = sys.stdout
        try:
            buffer = StringIO()
            sys.stdout = buffer
            main()
        finally:
            sys.stdout = original_stdout
        
        output = buffer.getvalue()
        self.assertIn("=== FLUENCE RESULTS (multiple files) ===", output)
        self.assertIn("ACTUAL Fluence  - Total sum: ", output)
        self.assertIn("EXPECTED Fluence  - Total sum: ", output)
        self.assertIn("Error (total)  - Total sum: ", output)

if __name__ == '__main__':
    unittest.main()
