import unittest
from types import SimpleNamespace
from unittest import mock

from panoramix import __main__


class MainTests(unittest.TestCase):
    @mock.patch("panoramix.__main__.coloredlogs.install")
    @mock.patch("panoramix.__main__.print_decompilation")
    @mock.patch("panoramix.__main__.cProfile.Profile")
    @mock.patch("panoramix.__main__.parse_args")
    def test_profile_is_used_for_comma_separated_inputs(
        self, parse_args, profile_cls, print_decompilation, coloredlogs_install
    ):
        parse_args.return_value = SimpleNamespace(
            v="20",
            profile=True,
            address_or_bytecode="first,second",
            function="",
        )
        profile = profile_cls.return_value.__enter__.return_value

        __main__.main()

        coloredlogs_install.assert_called_once()
        print_decompilation.assert_has_calls(
            [
                mock.call("first", parse_args.return_value),
                mock.call("second", parse_args.return_value),
            ]
        )
        self.assertEqual(print_decompilation.call_count, 2)
        profile.dump_stats.assert_called_once_with("panoramix.prof")

    @mock.patch("panoramix.__main__.coloredlogs.install")
    @mock.patch("panoramix.__main__.print_decompilation")
    @mock.patch("panoramix.__main__.cProfile.Profile")
    @mock.patch("panoramix.__main__.parse_args")
    def test_profile_still_works_for_single_input(
        self, parse_args, profile_cls, print_decompilation, coloredlogs_install
    ):
        parse_args.return_value = SimpleNamespace(
            v="20",
            profile=True,
            address_or_bytecode="single",
            function="",
        )
        profile = profile_cls.return_value.__enter__.return_value

        __main__.main()

        coloredlogs_install.assert_called_once()
        print_decompilation.assert_called_once_with("single", parse_args.return_value)
        profile.dump_stats.assert_called_once_with("panoramix.prof")


if __name__ == "__main__":
    unittest.main()
