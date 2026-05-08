import os
import unittest

os.environ.setdefault('MPLBACKEND', 'Agg')

import plots


class CliHelpersTest(unittest.TestCase):
    def setUp(self):
        self.parser = plots.processArgs()

    def test_resolve_output_path_prefers_explicit_output(self):
        args = self.parser.parse_args([
            'netcdf/OS_PIRATA-FR31_CTD.nc',
            '-t', 'CTD',
            '-p',
            '-k', 'PRES', 'TEMP',
            '-o', 'custom/output',
        ])
        self.assertEqual(plots.resolve_output_path(args), 'custom/output')

    def test_resolve_output_path_uses_profile_default(self):
        args = self.parser.parse_args([
            'netcdf/OS_PIRATA-FR31_CTD.nc',
            '-t', 'CTD',
            '-p',
            '-k', 'PRES', 'TEMP',
        ])
        self.assertEqual(plots.resolve_output_path(args), 'plots/profiles')

    def test_validate_args_requires_a_plot_mode(self):
        args = self.parser.parse_args([
            'netcdf/OS_PIRATA-FR31_CTD.nc',
            '-t', 'CTD',
            '-k', 'PRES', 'TEMP',
        ])
        with self.assertRaises(SystemExit):
            plots.validate_args(args, self.parser)

    def test_validate_args_rejects_invalid_scatter_keys(self):
        args = self.parser.parse_args([
            'netcdf/OS_AMAZOMIX_TSG.nc',
            '-t', 'TSG',
            '--scatter',
            '-k', 'SSPS', 'SSTP', 'TEMP',
        ])
        with self.assertRaises(SystemExit):
            plots.validate_args(args, self.parser)

    def test_resolve_profile_range_without_selection_uses_dataset_bounds(self):
        start, end = plots.resolve_profile_range([1, 2, 3], None)
        self.assertEqual((start, end), (1, 3))

    def test_resolve_profile_range_with_single_value_uses_dataset_end(self):
        start, end = plots.resolve_profile_range([1, 2, 3, 4], [3])
        self.assertEqual((start, end), (3, 4))

    def test_resolve_profile_range_rejects_more_than_two_values(self):
        with self.assertRaises(ValueError):
            plots.resolve_profile_range([1, 2, 3], [1, 2, 3])

    def test_screen_requested_detects_flag(self):
        self.assertTrue(plots.screen_requested(['--screen', '-p']))

    def test_screen_requested_is_false_without_flag(self):
        self.assertFalse(plots.screen_requested(['-p']))

    def test_select_backend_defaults_to_agg_without_screen(self):
        self.assertEqual(plots.select_matplotlib_backend(['-p'], {}), 'Agg')

    def test_select_backend_keeps_existing_non_agg_backend_for_screen(self):
        self.assertEqual(
            plots.select_matplotlib_backend(['--screen', '-p'], {'MPLBACKEND': 'TkAgg'}),
            'TkAgg',
        )

    def test_select_backend_prefers_qtagg_for_screen_when_env_is_agg(self):
        self.assertEqual(
            plots.select_matplotlib_backend(['--screen', '-p'], {'MPLBACKEND': 'Agg'}),
            'QtAgg',
        )
