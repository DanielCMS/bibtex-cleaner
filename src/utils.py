import os
import json

def load_configuration():
    util_dir = os.path.dirname(os.path.realpath(__file__))
    config_dir = os.path.realpath(os.path.join(util_dir, "../config"))

    with open(os.path.join(config_dir, 'config.json')) as config_file:
        return json.load(config_file)

def print_entry(entry):
    for key, value in entry.iteritems():
        print key.lower() + ': ' + value

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
