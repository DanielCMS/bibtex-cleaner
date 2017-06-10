import main
from unittest import TestCase
from mock import MagicMock
from mock import patch

class TestUtils(TestCase):
    @patch("main.EntryFilter", return_value=MagicMock(filter_entries = lambda x: (x, x)))
    @patch("main.DuplicationHandler", return_value=MagicMock(remove_duplicates = lambda x: x))
    def test_main(self, mock1, mock2):
        entries = "foo"
        to_retain, to_dump = main.main(entries)

        assert to_retain == "foo"
        assert to_dump == "foo"
