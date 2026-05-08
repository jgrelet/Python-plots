import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault('MPLBACKEND', 'Agg')

import plots


class SmokeTest(unittest.TestCase):
    def test_main_generates_one_profile_figure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            exit_code = plots.main([
                'netcdf/OS_AMAZOMIX_CTD.nc',
                '-t', 'CTD',
                '-p',
                '-k', 'PRES', 'TEMP',
                '-l', '101', '101',
                '-o', tmpdir,
                '--force',
            ])

            self.assertEqual(exit_code, 0)
            self.assertTrue(Path(tmpdir, 'AMAZOMIX-00101_CTD.png').exists())
