from django.conf import settings
from functools import reduce
import os
import sys
import icu

class Entry:
    """Single index entry and its subentries"""
    def __init__(self, main):
        self.main = main  # main entry part 
        self.subitems = []  # "dashed" subentries
        self.letter = self.main[0].upper()

    def add(self, subitem):
        self.subitems.append(subitem)

    def __repr__(self):
        return self.main

    def process(self):
        self._change_dashes()

    def _change_dashes(self):
        """Changing dashes to hyphens"""
        new_subitems = []
        for subitem in self.subitems:
            index = 0
            new_subitem = list(subitem)
            while subitem[index] == '-':
                new_subitem[index] = '–'
                index += 1
            new_subitems.append("".join(new_subitem))
        self.subitems = new_subitems

class IndexParser:
    """Index parsing utilities. Can be used as a context manager to cleanup old
    index file before proceeding
    """
    PATH = os.path.join(settings.MEDIA_ROOT, "index.txt")

    def __enter__(self):
        self.cleanup()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        initial = self.load_file()
        parsed = self.parse(initial)
        self.save_file(parsed)        

    def cleanup(self):
        # to overwrite index file
        if os.path.exists(self.PATH):
            os.remove(self.PATH) 

    def parse(self, initial):
        operations = [
            self._remove_spaces_from_between_dashes,
            self._add_dashes_at_begginning,
            self._sort_recursively,
            self._insert_spaces_between_dashes,
            self._remove_dashes_at_beginning,
            self._insert_empty_lines,
            self._strip_first_last_empty
        ]
        return reduce((lambda x, func: func(x)), operations, initial)

    def load_file(self):
        """Loads file contents"""
        with open(self.PATH, 'r') as file:
            lines = []
            for line in [line.strip() for line in file.readlines()]:
                if not line:
                    continue
                lines.append(line)
        return lines

    def save_file(self, lines):
        """Saves an output file"""
        with open(self.PATH, 'w') as outfile:
            for line in lines:
                outfile.write(line + "\n")

# PRIVATE 
    def _lines_to_entries(self, lines):
        """Groups lines into Entries"""
        items = list()
        current_item = None
        for line in lines:
            if not line:
                continue
            if line[0] in ('-', '–'):
                # subentry
                try:
                    current_item.add(line)
                except AttributeError:
                    print("\nError!!\n{}".format(line))
                    sys.exit()
            else:
                # entry
                if current_item:
                    current_item.process()
                    items.append(current_item)
                current_item = Entry(line)

        current_item.process()
        items.append(current_item)
        return items

    def _sort_entries_one_level(self, items):
        """
        Sorting entries with the key being the main entry part.
        Sorting is done with Polish locale comp. function
        """
        collator = icu.Collator.createInstance(icu.Locale('pl_PL.UTF-8'))
        return sorted(items, key=lambda item: collator.getSortKey(item.main))

    def _entries_to_lines(self, items):
        """Dumps Entries into lines"""
        lines = []
        for item in items:
            lines.append(item.main)
            for sub in item.subitems:
                lines.append(sub)
        return lines

    def _no_dashes(self, lines):
        """
        :returns: True is there are neither dashes nor hyphens in lines,
                False otherwise
        """
        return all([line[0] not in ('-', '–') for line in lines])


    def _sort_recursively(self, lines):
        """Recursively sort every tier of subentries"""
        if self._no_dashes(lines):
            return sorted(lines)
        # remove first dash
        lines = self._remove_dashes_at_beginning(lines)
        # make items
        entries = self._lines_to_entries(lines)
        for e in entries:
            e.subitems = self._sort_recursively(e.subitems)

        entries = self._sort_entries_one_level(entries)
        lines = self._entries_to_lines(entries)

        # add dashes to lines
        lines = self._add_dashes_at_begginning(lines)
        return lines

    def _remove_dashes_at_beginning(self, lines):
        """Removes first cher from the beginning of each line"""
        return [line[1:].strip() for line in lines]

    def _add_dashes_at_begginning(self, lines):
        """Makes each line begin with a dash and a space"""
        return ['–{}'.format(l) if l[0] == '–' else
                '– {}'.format(l) for l in lines]

    def _insert_spaces_between_dashes(self, lines):
        """Adds spaces between dashes, from --- to - - - """
        new_lines = []
        for line in lines:
            index = 0
            while line[index] == '–':
                index += 1
            dashes = line[:index]
            if not dashes:
                new_lines.append(line)
                continue
            dashes_spaces = []
            for dash in dashes:
                dashes_spaces.append(' ')
                dashes_spaces.append(dash)
            dashes_spaces = "".join(dashes_spaces).strip()
            full = list(dashes_spaces) + list(line[index:])
            new_lines.append("".join(full))
        return new_lines

    def _remove_spaces_from_between_dashes(self, lines):
        """Removes spaces from between dashes, from - - - to ---"""
        new_lines = []
        for line in lines:
            index = 0
            while line[index] in ('–', '-') or \
                    (line[index] == ' ' and line[index + 1] in ('–', '-')):
                index += 1
            dashes = line[:index]
            if not dashes:
                new_lines.append(line)
                continue

            cleared = dashes.replace(' ', '')
            full = list(cleared) + list(line[index:])
            new_lines.append("".join(full))
        return new_lines

    def _insert_empty_lines(self, lines):
        """
        Inserts empty line after each line of length 1 (which indicates a new 
        letter in index)
        """
        new_lines = []
        for line in lines:
            if len(line) == 1:
                new_lines.append('')
                new_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines

    def _strip_first_last_empty(self, lines):
        """Deletes first / last lines if these are ampty"""
        if not lines[0]:
            lines = lines[1:]
        if not lines[-1]:
            lines = lines[:-1]
        return lines

