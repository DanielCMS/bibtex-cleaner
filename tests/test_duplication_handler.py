from duplication_handler import DuplicationHandler
from unittest import TestCase 
from mock import patch 

class TestUtils(TestCase):
    def test_get_media(self):
        subject = DuplicationHandler()
        dummy_entry = {
            'booktitle': 'Dragon balls',
            'year': '1991'
        }
        casual_entry = {
            'journal': 'Dragon balls Z',
            'year': '1092'
        }
        oh_oh_entry = {
            'year': '1111'
        }

        assert subject.get_media(dummy_entry) == 'Dragon balls'
        assert subject.get_media(casual_entry) == 'Dragon balls Z'
        assert subject.get_media(oh_oh_entry) == None

    def test_has_media(self):
        subject = DuplicationHandler()
        dummy_entry = {
            'booktitle': 'Dragon balls',
            'year': '1991'
        }
        casual_entry = {
            'journal': 'Dragon ball Z',
            'year': '1092'
        }
        oh_oh_entry = {
            'year': '1111'
        }

        assert subject.has_media(dummy_entry)
        assert subject.has_media(casual_entry)
        assert not subject.has_media(oh_oh_entry)

    def test_is_in_journal(self):
        subject = DuplicationHandler()
        dummy_entry = {
            'booktitle': 'Dragon balls',
            'year': '1991'
        }
        casual_entry = {
            'journal': 'IEEE Transactions Dragon balls',
            'year': '1092'
        }
        oh_oh_entry = {
            'year': '1111'
        }
        good_entry = {
            'year': '1948',
            'title': 'A mathematical theory of communication',
            'journal': 'Bell system technical journal',
            'author': 'Shannon, C. E.',
            'volume': '27'
        }


        assert not subject.is_in_journal(dummy_entry)
        assert subject.is_in_journal(casual_entry)
        assert not subject.is_in_journal(oh_oh_entry)
        assert subject.is_in_journal(good_entry)

    def test_is_in_conference(self):
        subject = DuplicationHandler()
        dummy_entry = {
            'booktitle': 'Dragon balls conference',
            'year': '1991'
        }
        casual_entry = {
            'journal': 'Universe meeting about Dragon balls',
            'year': '1092'
        }
        oh_oh_entry = {
            'year': '1111'
        }
        good_entry = {
            'year': '1948',
            'title': 'A mathematical theory of communication',
            'journal': 'Bell system technical journal',
            'author': 'Shannon, C. E.',
            'volume': '27'
        }


        assert subject.is_in_conference(dummy_entry)
        assert subject.is_in_conference(casual_entry)
        assert not subject.is_in_conference(oh_oh_entry)
        assert not subject.is_in_conference(good_entry)

    def test_is_in_arxiv(self):
        subject = DuplicationHandler()
        dummy_entry = {
            'booktitle': 'arxiv: Dragon balls',
            'year': '1991'
        }
        casual_entry = {
            'journal': 'IEEE Transactions Dragon balls',
            'year': '1092'
        }
        oh_oh_entry = {
            'year': '1111'
        }
        good_entry = {
            'year': '1948',
            'title': 'A mathematical theory of communication',
            'journal': 'Bell system technical journal',
            'author': 'Shannon, C. E.',
            'volume': '27'
        }


        assert subject.is_in_arxiv(dummy_entry)
        assert not subject.is_in_arxiv(casual_entry)
        assert not subject.is_in_arxiv(oh_oh_entry)
        assert not subject.is_in_arxiv(good_entry)

    def test_resolve_duplicates_in_primal_mode(self):
        with patch("utils.load_configuration", return_value={"duplicationResolveMode": "primal"}) as mock:
            subject = DuplicationHandler()
            dummy_entry = {
                'booktitle': 'arxiv: Dragon balls',
                'year': '1991'
            }
            casual_entry = {
                'journal': 'IEEE Transactions Dragon balls',
                'year': '1092'
            }
            oh_oh_entry = {
                'year': '1111'
            }
            conf_entry = {
                'journal': 'Blizzard diablo conference',
                'year': '1992',
                'title': 'Diablo 1 will be remade, no diablo 4'
            }
            hmm_entry = {
                'journal': 'random wording'
            }

            assert subject.resolve_duplicates([dummy_entry, casual_entry, oh_oh_entry]) == casual_entry
            assert subject.resolve_duplicates([dummy_entry, oh_oh_entry]) == dummy_entry
            assert subject.resolve_duplicates([oh_oh_entry]) == oh_oh_entry
            assert subject.resolve_duplicates([conf_entry, dummy_entry]) == conf_entry
            assert subject.resolve_duplicates([hmm_entry, oh_oh_entry]) == hmm_entry

    def test_resolve_duplicates_in_first_mode(self):
        with patch("utils.load_configuration", return_value={"duplicationResolveMode": "first"}) as mock:
            subject = DuplicationHandler()
            dummy_entry = {
                'booktitle': 'arxiv: Dragon balls',
                'year': '1991'
            }
            casual_entry = {
                'journal': 'IEEE Transactions Dragon balls',
                'year': '1092'
            }
            oh_oh_entry = {
                'year': '1111'
            }
            conf_entry = {
                'journal': 'Blizzard diablo conference',
                'year': '1992',
                'title': 'Diablo 1 will be remade, no diablo 4'
            }
            hmm_entry = {
                'journal': 'random wording'
            }

            assert subject.resolve_duplicates([dummy_entry, casual_entry, oh_oh_entry]) == dummy_entry
            assert subject.resolve_duplicates([dummy_entry, oh_oh_entry]) == dummy_entry
            assert subject.resolve_duplicates([oh_oh_entry]) == oh_oh_entry
            assert subject.resolve_duplicates([conf_entry, dummy_entry]) == conf_entry
            assert subject.resolve_duplicates([hmm_entry, oh_oh_entry]) == hmm_entry

    def test_resolve_duplicates_in_manual_mode(self):
        with patch("utils.load_configuration", return_value={"duplicationResolveMode": "manual"}) as mock:
            with patch("utils.get_answer_from", side_effect=['1', '2', '1']) as another_mock:
                subject = DuplicationHandler()
                dummy_entry = {
                    'booktitle': 'arxiv: Dragon balls',
                    'year': '1991'
                }
                casual_entry = {
                    'journal': 'IEEE Transactions Dragon balls',
                    'year': '1092'
                }
                oh_oh_entry = {
                    'year': '1111'
                }

                assert subject.resolve_duplicates([dummy_entry, casual_entry, oh_oh_entry]) == dummy_entry
                assert subject.resolve_duplicates([dummy_entry, oh_oh_entry]) == oh_oh_entry
                assert subject.resolve_duplicates([oh_oh_entry]) == oh_oh_entry

    def test_resolve_duplicates_in_invalid_mode(self):
        with patch("utils.load_configuration", return_value={"duplicationResolveMode": "invalid"}) as mock:
            subject = DuplicationHandler()
            dummy_entry = {
                'booktitle': 'arxiv: Dragon balls',
                'year': '1991'
            }

            with self.assertRaises(Exception) as context:
                assert subject.resolve_duplicates([dummy_entry])

    def test_remove_duplicates(self):
        with patch("utils.load_configuration", return_value={"duplicationResolveMode": "primal"}) as mock:
            subject = DuplicationHandler()
            dummy_entry = {
                'booktitle': 'arxiv: Dragon balls',
                'year': '1991',
                'title': 'Diablo 3: Rise of Necromancer'
            }
            casual_entry = {
                'journal': 'IEEE Transactions Dragon balls',
                'year': '1092',
                'title': 'Diablo 3: Reaper of Souls'
            }
            oh_oh_entry = {
                'year': '1111',
                'title': 'Odyssey'
            }
            conf_entry = {
                'journal': 'Blizzard diablo conference',
                'year': '1992',
                'title': 'Diablo 3: Reaper of Souls'
            }
            to_test = [dummy_entry, casual_entry, oh_oh_entry, conf_entry]
            expected = [dummy_entry, oh_oh_entry, casual_entry]

            assert subject.remove_duplicates(to_test) == expected

