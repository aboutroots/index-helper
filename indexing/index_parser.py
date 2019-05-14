import copy
import os
import re
import sys
from functools import reduce

from django.conf import settings
from docx import Document


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
    DOCX_PATH = os.path.join(settings.MEDIA_ROOT, "index.docx")

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
        if os.path.exists(self.DOCX_PATH):
            os.remove(self.DOCX_PATH)

    def parse(self, initial):
        operations = [
            self._check_tier_growth,
            self._remove_spaces_from_between_dashes,
            self._add_dashes_at_begginning,
            self._sort_recursively,
            self._insert_spaces_between_dashes,
            self._remove_dashes_at_beginning,
            self._change_dashes_between_digits,
            self._insert_empty_lines,
            self._strip_first_last_empty
        ]
        return reduce((lambda x, func: func(x)), operations, initial)

    def load_file(self, docx=False):
        """Loads file contents"""
        if docx:
            lines = self._load_docx()
        else:
            with open(self.PATH, 'r', encoding="windows-1250") as file:
                lines = []
                for line in [line.strip() for line in file.readlines()]:
                    if not line:
                        continue
                    lines.append(line)
        return lines

    def save_file(self, lines, docx=False):
        """Saves an output file"""
        if docx:
            self._save_docx(lines)
        else:
            with open(self.PATH, 'w') as outfile:
                for line in lines:
                    outfile.write(line + "\n")

    # PRIVATE
    @staticmethod
    def _raise_to_user(e, exc_info, file_ln):
        """Raises exception with html message"""
        exc_type, exc_obj, exc_tb = exc_info
        code_ln = exc_tb.tb_lineno
        raise type(e)(
            'Some problem occurred in index with line:\n<pre style="font-weight: bold;"><code id="bad-line">{}</code></pre>\nPlease make sure that your input file is correct. If this error repeats, check line {} in parser code. <span style="font-style: italic;"> (Click to copy line to clipboard and dismiss this message) </span>'.format(
                file_ln, code_ln))

    def _check_tier_growth(self, lines):
        """
        Raises error if there is more then one tier growing at the same time
        """
        last_dashes = 0
        for file_ln in lines:
            temp = copy.deepcopy(file_ln).replace(' ', '')
            i = 0
            while temp[i] in ('–', '-'):
                i += 1
            try:
                assert i <= last_dashes + 1
            except AssertionError as e:
                exc_info = sys.exc_info()
                self._raise_to_user(e, exc_info, file_ln)
            last_dashes = i

        return lines

    def _load_docx(self):
        doc = Document(self.DOCX_PATH)
        lines = []
        for para in doc.paragraphs:
            line = []
            for r in para.runs:
                text = r.text
                if r.italic and r.bold:
                    text = "&&{}&&".format(text)
                elif r.italic:
                    text = "##{}##".format(text)
                elif r.bold:
                    text = "$${}$$".format(text)
                line.append(text)
            lines.append(''.join(line))
        return lines

    def _save_docx(self, lines):
        pass
        # TODO: encode lines into document and save it
        # TODO: handle docx in context manager
        # TODO: enable docx on frontend and pass parameter to IndexHelper

    def _lines_to_entries(self, lines):
        """Groups lines into Entries"""
        items = list()
        current_item = None
        for file_ln in lines:
            if not file_ln:
                continue
            if file_ln[0] in ('-', '–'):
                # subentry
                try:
                    current_item.add(file_ln)
                except AttributeError as e:
                    exc_info = sys.exc_info()
                    self._raise_to_user(e, exc_info, file_ln)
            else:
                # entry
                if current_item:
                    current_item.process()
                    items.append(current_item)
                current_item = Entry(file_ln)

        current_item.process()
        items.append(current_item)
        return items

    def _sort_entries_one_level(self, items):
        """
        Sorting entries with the key being the main entry part.
        Sorting is done with Polish locale comp. function
        """
        return sorted(items, key=lambda item: self._get_sort_key(item.main))

    def _get_sort_key(self, phrase):
        """Custom key function. Polish alphabetical case insensitive"""
        alphabet = [
            ' ', ',', '’', '.', ':', '!', '@', '_', '|', '\\', '?', '„', '”',
            '"', "'", '~', '+', '=', '(', ')', '[', ']', '{', '}', '-', '‒',
            '–', '—', '―', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'Ł', 'M', 'N', 'Ń', 'O', 'Ó', 'P', 'Q', 'R', 'S', 'Ś',
            'T', 'U', 'Ü', 'V', 'W', 'X', 'Y', 'Z', 'Ź', 'Ż'
        ]
        result = []
        for c in phrase:
            try:
                result.append(alphabet.index(c.upper()))
            except (IndexError, ValueError):
                if c in ['$', '#', '&']:  # bold and italic indicators
                    result.append(0)
                else:
                    result.append(999)
        return result

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

    def _change_dashes_between_digits(self, lines):
        """Changes hyphens to dashes between page nubers"""
        return [re.sub(r'(\d)-(\d)', r'\1–\2', line) for line in lines]

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
        """Deletes first / last lines if these are empty"""
        if not lines[0]:
            lines = lines[1:]
        if not lines[-1]:
            lines = lines[:-1]
        return lines
