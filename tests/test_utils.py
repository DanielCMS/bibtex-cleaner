from utils import load_configuration, print_entry, get_yes_no, get_answer_from
from unittest import TestCase 
from mock import patch 

class TestUtils(TestCase):
    def test_load_configuration(self):
        assert load_configuration()

    def test_print_entry(self):
        with patch('__builtin__.print') as mock_print:
            print_entry({"Test": "foo"})
            mock_print.assert_called_with("test: foo")

    def test_get_yes_no(self):
        with patch("__builtin__.raw_input", return_value="yes") as raw:
            assert get_yes_no()

        with patch("__builtin__.raw_input", return_value="y") as raw:
            assert get_yes_no()

        with patch("__builtin__.raw_input", return_value="no") as raw:
            assert not get_yes_no()

        with patch("__builtin__.raw_input", return_value="n") as raw:
            assert not get_yes_no()

    def test_get_yes_no_regardless_uppercase(self):
        with patch("__builtin__.raw_input", return_value="Yes") as raw:
            assert get_yes_no()

        with patch("__builtin__.raw_input", return_value="Y") as raw:
            assert get_yes_no()

        with patch("__builtin__.raw_input", return_value="No") as raw:
            assert not get_yes_no()

        with patch("__builtin__.raw_input", return_value="N") as raw:
            assert not get_yes_no()

    def test_get_yes_no_strips_space(self):
        with patch("__builtin__.raw_input", return_value=" Yes") as raw:
            assert get_yes_no()

        with patch("__builtin__.raw_input", return_value="Y ") as raw:
            assert get_yes_no()

        with patch("__builtin__.raw_input", return_value=" No") as raw:
            assert not get_yes_no()

        with patch("__builtin__.raw_input", return_value="N ") as raw:
            assert not get_yes_no()

    def test_get_yes_no_for_invalid_input(self):
        with patch("__builtin__.raw_input", side_effect=['foo', 'y']) as raw:
            assert get_yes_no()

    def test_get_answer_from(self):
        with patch("__builtin__.raw_input", return_value="yes") as raw:
            assert get_answer_from(["yes", "no"]) == "yes"

        with patch("__builtin__.raw_input", return_value="YeS") as raw:
            assert get_answer_from(["yes", "no"]) == "yes"

        with patch("__builtin__.raw_input", return_value=" YeS ") as raw:
            assert get_answer_from(["yes", "no"]) == "yes"

    def test_get_answer_from_for_invalid_input(self):
        with patch("__builtin__.raw_input", side_effect=['foo', 'yes']) as raw:
            assert get_answer_from(["yes", "no"]) == "yes"
