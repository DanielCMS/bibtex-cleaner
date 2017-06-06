from rules import ascii_code_rule
import utils
import pprint
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogeneize_latex_encoding

DEFAULT = 'default'
pp = pprint.PrettyPrinter()

def main(file_name, output='default'):
    with open(file_name) as bibtex_file:
        parser = BibTexParser()
        parser.customization = homogeneize_latex_encoding
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    for entry in bib_database.entries:
        result = ascii_code_rule.test(entry)

        if not result["passed"]:
            print 'The following item seems suspicious according to the rule:'
            print result['error']
            print 'Do you want to keep it? (y/n)'
            print '-' * 32
            utils.print_entry(entry)
            print entry
            print '\n'
