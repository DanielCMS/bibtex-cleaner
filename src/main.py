from entry_filter import EntryFilter
from duplication_handler import DuplicationHandler


def main(entries):
    bib_entry_filter = EntryFilter()    
    to_retain, to_dump = bib_entry_filter.filter_entries(entries)

    duplication_remover = DuplicationHandler()
    to_retain = duplication_remover.remove_duplicates(to_retain)

    return to_retain, to_dump
