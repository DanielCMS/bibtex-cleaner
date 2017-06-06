from rules import ascii_code_rule, no_short_title_rule, enforce_year_rule, no_super_long_title_rule
import utils
import pprint
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogeneize_latex_encoding

DEFAULT = 'default'
SCHEMAS = {
    'ASCII_CODE_RULE': ascii_code_rule.test,
    'NO_SHORT_TITLE_RULE': no_short_title_rule.test,
    'ENFORCE_YEAR_RULE': enforce_year_rule.test,
    'NO_SUPER_LONG_TITLE_RULE': no_super_long_title_rule.test
}


def get_yes_no():
    while True:
        answer = raw_input()
        if answer.lower() in ['y', 'yes', 'n', 'no']:
            return answer.lower() in ['y', 'yes']
        else:
            print "Please enter either y or n"


def retain_after_matching_schemas(entry):
    results = {}

    for rule, tester in SCHEMAS.iteritems():
        results[rule] = tester(entry)

    if not all(results[rule]['passed'] for rule in results):
        print 'The following item seems suspicious according to the following rule(s):'
        for rule, result in results.iteritems():
            if not result['passed']:
                print rule + ': ' + result['error']

        print 'Do you want to keep it? (y/n)'
        print '-' * 32
        utils.print_entry(entry)
        print '\n'

        return get_yes_no()
    else:
        return True


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



    print toDump
