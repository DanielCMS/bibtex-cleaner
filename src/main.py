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
        answer = raw_input('\n')
        if answer.lower().strip() in ['y', 'yes', 'n', 'no']:
            print ''
            return answer.lower().strip() in ['y', 'yes']
        else:
            print "Please enter either y or n"


def get_answer_from(options):
    normalized_options = [str(option).lower().strip() for option in options]

    while True:
        answer = raw_input('\n')
        if answer.lower().strip() in normalized_options:
            print ''
            return answer.lower().strip()
        else:
            print "Please choose from: " + str(options)


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

        return get_yes_no()
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

            answer = get_answer_from(range(len(entries)))
            ret.append(entries[int(answer)])
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
