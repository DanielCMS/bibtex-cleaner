from rules import enforce_year_rule, no_short_title_rule, no_super_long_title_rule, ascii_code_rule
from unittest import TestCase
import pytest

class TeseRules(TestCase):
    def test_enforce_year_rule(self):
        dummy_entry = {
            'year': '1991',
            'title': 'A good paper',
            'author': 'Dummies'
        }

        assert enforce_year_rule.test(dummy_entry)['passed']

        dummy_entry.pop('year')

        assert not enforce_year_rule.test(dummy_entry)['passed']

    def test_no_short_title_rule_when_no_title_supplied(self):
        dummy_entry = {
            'year': '1991',
            'author': 'Dummies'
        }

        assert not no_short_title_rule.test(dummy_entry)['passed'] 

    def test_no_short_title_rule(self):
        dummy_entry = {
            'year': '1991',
            'title': 'A bed paper',
            'author': 'Dummies'
        }

        assert no_short_title_rule.test(dummy_entry)['passed'] 

        dummy_entry = {
            'year': '1991',
            'title': 'bed paper',
            'author': 'Dummies'
        }

        assert not no_short_title_rule.test(dummy_entry)['passed'] 

    def test_no_super_long_title_rule_when_no_title_supplied(self):
        dummy_entry = {
            'year': '1991',
            'author': 'Dummies'
        }

        assert not no_super_long_title_rule.test(dummy_entry)['passed'] 

    def test_no_super_long_title_rule(self):
        dummy_entry = {
            'year': '1991',
            'title': 'A bed paper',
            'author': 'Dummies'
        }

        assert no_super_long_title_rule.test(dummy_entry)['passed'] 

        dummy_entry = {
            'year': '1991',
            'title': 'This is a super super super super super super \
                    super super super super super super super super \
                    super super super super long and boring paper',
            'author': 'Dummies'
        }

        assert not no_super_long_title_rule.test(dummy_entry)['passed'] 

    def test_ascii_code_rule(self):
        dummy_entry = {
            'year': '1992',
            'title': 'A nice paper',
            'author': 'Dummies'
        }

        assert ascii_code_rule.test(dummy_entry)['passed']

        dummy_entry = {
            'year': '1992',
            'title': u'A nice paper\ua000\u1111',
            'author': 'Dummies'
        }

        assert not ascii_code_rule.test(dummy_entry)['passed']

        dummy_entry = {
            'year': '1992',
            'title': u'A nice paper',
            'author': u'Dummies\ua000'
        }

        assert not ascii_code_rule.test(dummy_entry)['passed']
