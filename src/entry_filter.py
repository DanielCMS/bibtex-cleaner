from __future__ import print_function
from rules import ascii_code_rule, no_short_title_rule, enforce_year_rule, no_super_long_title_rule
import utils

SCHEMAS = {
    'ASCII_CODE_RULE': ascii_code_rule.test,
    'NO_SHORT_TITLE_RULE': no_short_title_rule.test,
    'ENFORCE_YEAR_RULE': enforce_year_rule.test,
    'NO_SUPER_LONG_TITLE_RULE': no_super_long_title_rule.test
}
MAND_SCHEMAS = ['ASCII_CODE_RULE', 'NO_SUPER_LONG_TITLE_RULE']

class EntryFilter:
    def __init__(self):
        self.filter_mode = utils.load_configuration()['filterMode']

    def filter_entries(self, entries):
        to_retain = []
        to_dump = []

        for entry in entries:
            if self.should_retain_entry(entry):
                to_retain.append(entry)
            else:
                to_dump.append(entry)

        return to_retain, to_dump

    def should_retain_entry(self, entry):
        results = {}

        for rule, tester in SCHEMAS.iteritems():
            results[rule] = tester(entry)

        if self.filter_mode == 'harsh':
            return all(results[rule]['passed'] for rule in results)
        elif self.filter_mode == 'casual':
            return all(results[rule]['passed'] for rule in MAND_SCHEMAS)
        elif self.filter_mode == 'careful':
            if all(results[rule]['passed'] for rule in results):
                return True
            elif all(results[rule]['passed'] for rule in MAND_SCHEMAS):
                return self.get_response_for_suspicious_entry(entry, results)
            else:
                return False
        elif self.filter_mode == 'manual':
            if all(results[rule]['passed'] for rule in results):
                return True
            else:
                return self.get_response_for_suspicious_entry(entry, results)
        else:
            raise Exception("Invalid filter mode")

    def get_response_for_suspicious_entry(self, entry, results):
        print('\nThe following item seems suspicious according to the following rule(s):')
        for rule, result in results.iteritems():
            if not result['passed']:
                print(rule + ': ' + result['error'])

        print('Do you want to keep it? (y/n)')
        print('-' * 32)
        utils.print_entry(entry)

        return utils.get_yes_no()
