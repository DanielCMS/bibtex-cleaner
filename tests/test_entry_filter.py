from entry_filter import EntryFilter
from unittest import TestCase 
from mock import patch 

class TestUtils(TestCase):
    def test_get_response_for_suspicious_entry(self):
        with patch('__builtin__.print') as mock_print:
            with patch('utils.get_yes_no', return_value=True) as mock:
                subject = EntryFilter()
                assert subject.get_response_for_suspicious_entry({'test': 'foo'}, \
                        {'rule1': {'passed': False, 'error': 'you should like Caltech'}})
                mock_print.assert_called_with("test: foo")

    def test_should_retain_entry_in_harsh_mode(self):
        with patch('utils.load_configuration', return_value={'filterMode': 'harsh'}) as mock:
            subject = EntryFilter()
            dummy_entry = {
                'year': '1991',
                'title': 'foo'
            }
            good_entry = {
                'year': '1948',
                'title': 'A mathematical theory of communication',
                'journal': 'Bell system technical journal',
                'author': 'Shannon, C. E.',
                'volume': '27'
            }

            assert not subject.should_retain_entry(dummy_entry)
            assert subject.should_retain_entry(good_entry)
            assert mock.called

    def test_should_retain_entry_in_casual_mode(self):
        with patch('utils.load_configuration', return_value={'filterMode': 'casual'}) as mock:
            subject = EntryFilter()
            dummy_entry = {
                'year': '1991',
                'title': 'foo'
            }
            good_entry = {
                'year': '1948',
                'title': 'A mathematical theory of communication',
                'journal': 'Bell system technical journal',
                'author': 'Shannon, C. E.',
                'volume': '27'
            }

            assert subject.should_retain_entry(dummy_entry)
            assert subject.should_retain_entry(good_entry)

    def test_should_retain_entry_in_careful_mode(self):
        with patch('utils.load_configuration', return_value={'filterMode': 'careful'}) as mock:
            subject = EntryFilter()
            dummy_entry = {
                'year': '1991'
            }
            casual_entry = {
                'year': '1991',
                'title': 'foo'
            }
            good_entry = {
                'year': '1948',
                'title': 'A mathematical theory of communication',
                'journal': 'Bell system technical journal',
                'author': 'Shannon, C. E.',
                'volume': '27'
            }

            assert subject.should_retain_entry(good_entry)
            assert not subject.should_retain_entry(dummy_entry)

            with patch('utils.get_yes_no', return_value=True) as raw:
                assert subject.should_retain_entry(casual_entry)
            with patch('utils.get_yes_no', return_value=False) as raw:
                assert not subject.should_retain_entry(casual_entry)

    def test_should_retain_entry_in_manual_mode(self):
        with patch('utils.load_configuration', return_value={'filterMode': 'manual'}) as mock:
            subject = EntryFilter()
            dummy_entry = {
                'year': '1991'
            }
            good_entry = {
                'year': '1948',
                'title': 'A mathematical theory of communication',
                'journal': 'Bell system technical journal',
                'author': 'Shannon, C. E.',
                'volume': '27'
            }

            assert subject.should_retain_entry(good_entry)

            with patch('utils.get_yes_no', return_value=True) as raw:
                assert subject.should_retain_entry(dummy_entry)
            with patch('utils.get_yes_no', return_value=False) as raw:
                assert not subject.should_retain_entry(dummy_entry)

    def test_should_retain_entry_for_invalid_mode(self):
        with patch("utils.load_configuration", return_value={'filterMode': 'foo'}) as mock:
            subject = EntryFilter()
            dummy_entry = {
                'year': '1992'
            }

        with self.assertRaises(Exception) as context:
            subject.should_retain_entry(dummy_entry)

    def test_filter_entries(self):
        with patch('utils.load_configuration', return_value={'filterMode': 'harsh'}) as mock:
            subject = EntryFilter()
            dummy_entry = {
                'year': '1991'
            }
            casual_entry = {
                'year': '1991',
                'title': 'foo'
            }
            good_entry = {
                'year': '1948',
                'title': 'A mathematical theory of communication',
                'journal': 'Bell system technical journal',
                'author': 'Shannon, C. E.',
                'volume': '27'
            }

            entries = [dummy_entry, casual_entry, good_entry]
            to_retain, to_dump = subject.filter_entries(entries)
            self.assertEqual(to_retain, [good_entry])
            self.assertEqual(to_dump, [dummy_entry, casual_entry])
