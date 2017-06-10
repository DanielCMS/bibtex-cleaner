from __future__ import print_function
from rules import ascii_code_rule, no_short_title_rule, enforce_year_rule, no_super_long_title_rule
import utils


class DuplicationHandler:
    def __init__(self):
        self.resolve_mode = utils.load_configuration()['duplicationResolveMode']

    def remove_duplicates(self, entries):
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
                ret.append(self.resolve_duplicates(entries))
            else:
                ret.append(entries[0])

        return ret

    def resolve_duplicates(self, entries):
        if self.resolve_mode == 'primal':
            return self.resolve_duplicates_primal(entries)
        elif self.resolve_mode == 'first':
            return self.resolve_duplicates_first(entries)
        elif self.resolve_mode == 'manual':
            return self.resolve_duplicates_manual(entries)
        else:
            raise Exception("Invalid duplication resolve mode")

    def resolve_duplicates_primal(self, entries):
        for entry in entries:
            if self.is_in_journal(entry):
                return entry

        for entry in entries:
            if self.is_in_conference(entry):
                return entry

        for entry in entries:
            if self.is_in_arxiv(entry):
                return entry

        for entry in entries:
            if self.has_media(entry):
                return entry

        return entries[0]

    def resolve_duplicates_first(self, entries):
        return entries[0]

    def resolve_duplicates_manual(self, entries):
        print('Duplicate entries detected. Which one of the following you want to keep?\n')
        for i in range(len(entries)):
            print(str(i + 1) + '.' + '-' * 30)
            utils.print_entry(entries[i])

        answer = utils.get_answer_from(range(1, len(entries) + 1))
        return entries[int(answer) - 1]

    def is_in_journal(self, entry):
        if self.has_media(entry):
            media = self.get_media(entry).lower()
            return 'journal' in media or 'transaction' in media
        else:
            return False

    def is_in_conference(self, entry):
        if self.has_media(entry):
            media = self.get_media(entry).lower()
            return 'conference' in media or 'meeting' in media
        else:
            return False

    def is_in_arxiv(self, entry):
        if self.has_media(entry):
            media = self.get_media(entry).lower()
            return 'arxiv' in media
        else:
            return False

    def has_media(self, entry):
        return self.get_media(entry) != None 

    def get_media(self, entry):
        if 'booktitle' in entry:
            return entry['booktitle']
        elif 'journal' in entry:
            return entry['journal']
        else:
            return None
