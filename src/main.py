from rules import ascii_code_rule, no_short_title_rule, enforce_year_rule, no_super_long_title_rule
import utils
import pprint
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogeneize_latex_encoding

DEFAULT = 'default'
CONFIG = utils.load_configuration()
FILTER_MODE = CONFIG['filterMode'].lower().strip()
DUPLICATION_RESOLVE = CONFIG['duplicationResolve'].lower().strip()
SCHEMAS = {
    'ASCII_CODE_RULE': ascii_code_rule.test,
    'NO_SHORT_TITLE_RULE': no_short_title_rule.test,
    'ENFORCE_YEAR_RULE': enforce_year_rule.test,
    'NO_SUPER_LONG_TITLE_RULE': no_super_long_title_rule.test
}
CASUAL_SCHEMAS = ['ASCII_CODE_RULE', 'NO_SHORT_TITLE_RULE', 'NO_SUPER_LONG_TITLE_RULE']
CAREFUL_SCHEMAS = ['ASCII_CODE_RULE', 'NO_SUPER_LONG_TITLE_RULE']

def retain_after_matching_schemas(entry):
    results = {}

    for rule, tester in SCHEMAS.iteritems():
        results[rule] = tester(entry)

    if not all(results[rule]['passed'] for rule in results):
        if FILTER_MODE == 'harsh':
            return False
        elif FILTER_MODE == 'casual':
            for rule, result in results.iteritems():
                if not result['passed'] and rule in CASUAL_SCHEMAS:
                    return False

            return True
        elif FILTER_MODE == 'careful':
            for rule, result in results.iteritems():
                if not result['passed'] and rule in CAREFUL_SCHEMAS:
                    return False

            print 'The following item seems suspicious according to the following rule(s):'
            for rule, result in results.iteritems():
                if not result['passed']:
                    print rule + ': ' + result['error']

            print 'Do you want to keep it? (y/n)'
            print '-' * 32
            utils.print_entry(entry)

            return utils.get_yes_no()
        else:
            print 'The following item seems suspicious according to the following rule(s):'
            for rule, result in results.iteritems():
                if not result['passed']:
                    print rule + ': ' + result['error']

            print 'Do you want to keep it? (y/n)'
            print '-' * 32
            utils.print_entry(entry)

            return utils.get_yes_no()
    else:
        return True


def remove_duplicates(entries):
    ret = []
    entries_by_title = {}

    for entry in entries:
        key = entry['title'].lower().strip()
        if key in entries_by_title:
            entries_by_title[key].append(entry)
        else:
            entries_by_title[key] = [entry]

    for key, entries in entries_by_title.iteritems():
        if len(entries) > 1:
            print 'Duplicate entries detected. Which one of the following you want to keep?'
            for i in range(len(entries)):
                print str(i) + '.' + '-' * 30
                utils.print_entry(entries[i])

            answer = utils.get_answer_from(range(1, len(entries) + 1))
            ret.append(entries[int(answer) - 1])
        else:
            ret.append(entries[0])

    return ret


def main(file_name, output='default'):
    with open(file_name) as bibtex_file:
        parser = BibTexParser()
        parser.customization = homogeneize_latex_encoding
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    toRetain = []
    toDump = []

    # Filter out entries violating schemas
    for entry in bib_database.entries:
        if retain_after_matching_schemas(entry):
            toRetain.append(entry)
        else:
            toDump.append(entry)

    # Remove duplicates
    toRetain = remove_duplicates(toRetain)

    # Write to files
