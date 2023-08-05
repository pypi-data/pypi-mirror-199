#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''bibparse -- read and write BibTeX files.

  bibparse is a BibTeX parsing module for Python.

  NOTE: Some Python 2 incompatibilities exist since 1.2.0.dev2.

  Copyright © 2019–2022 Legisign.org
  Licensed under GNU General Public License version 3 or later.

  2023-03-24  1.2.0  Finally submitting two-year work of 1.2.0.

'''

import re
import enum

version = '1.2.0'

# Recognized BibTeX keys; these keys will appear in the order given
# when BibItem.__repr()__ is called. Any other keys in an entry will
# appear in random order tailing these ones.
bibkeys = ('key',
           'author',
           'title',
           'subtitle',              # semi-standard
           'origtitle',             # non-standard
           'translator',            # semi-standard
           'crossref',
           'editor',
           'booktitle',
           'booksubtitle',          # non-standard
           'origbooktitle',         # non-standard
           'journal',
           'series',
           'volume',
           'number',
           'edition',
           'organization',
           'institution',
           'school',
           'publisher',
           'address',
           'pubstate',              # semi-standard
           'howpublished',
           'url',                   # semi-standard
           'urldate',               # semi-standard
           'doi',                   # semi-standard
           'month',
           'year',
           'pubyear',
           'chapter',
           'pages',
           'isbn',                  # semi-standard
           'issn',                  # semi-standard
           'annote',
           'type',
           'note',
           'keywords')              # semi-standard
special_types = ('comment',
                 'preamble',
                 'string')

### HELPER FUNCTIONS

def to_bibtex(key, value):
    '''Convert Python list value to BibTeX string.'''
    if isinstance(value, list):
        if key.lower() == 'pages':
            value = '-'.join(value)
        elif key.lower() == 'keywords':
            value = ' '.join(value)
        else:
            value = ' and '.join(value)
    return value

def to_python(key, value):
    '''Convert BibTeX string to a Python value.'''
    if key.lower() in ('author', 'editor', 'publisher', 'translator'):
        value = value.split(' and ')
    elif key.lower() == 'pages':
        value = value.split('-')
    elif key.lower() == 'keywords':
        value = value.split()
    return value

### CLASSES

# Exceptions

class BibError(Exception):
    '''Base class of bibparse errors'''
    def __init__(self, lineno, msg):
        self.lineno = lineno
        self.err = msg

class ParseError(BibError):
    '''Parse error.'''
    pass

class MissingCommaError(ParseError):
    '''Parser missing a comma.'''
    pass

class DuplicateError(BibError):
    '''Duplicate ID or preamble'''
    pass

class NoIDError(BibError):
    '''No ID in an entry'''
    pass

# Helper class

class ParserState(enum.Enum):
    '''File-level parser states.'''
    AT = enum.auto()        # waiting for at sign (@)
    TYPE = enum.auto()      # reading bibtype string
    SKIP = enum.auto()      # skipping characters
    DATA = enum.auto()      # waiting field (either {...} or "...")

class ItemParserState(enum.Enum):
    '''Item-level parser states.'''
    SKIP = enum.auto()      # skipping whitespace
    ID = enum.auto()        # reading bibid
    COMMA = enum.auto()     # waiting comma (or end of record)
    KEY = enum.auto()       # reading key
    EQUALS = enum.auto()    # waiting equals sign (=)
    SEPAR = enum.auto()     # waiting value separator ({ or ")
    VALUE = enum.auto()     # reading value

# BibTeX classes

class BibItem(dict):
    '''BibItem is a dict containing one BibTeX entry.'''

    def __init__(self, bibid='', bibtype='', data=None, rawdata=None):
        self.bibid = bibid
        self.bibtype = bibtype
        self.preamble = None
        self.strings = {}
        if data:
            if not isinstance(data, dict):
                raise TypeError('data should be dict')
            self.update(data)
        if rawdata:
            if not isinstance(rawdata, str):
                raise TypeError('rawdata should be str')
            if bibtype == 'preamble':
                self.preamble = rawdata
            elif bibtype == 'string':
                pass
            elif bibtype == 'comment':
                pass
            else:
                self.bibid, entry = BibItem.parse(data)
                self.update(entry)

    def __lt__(self, entry):
        x = self.bibid if isinstance(self.bibid, str) else ''
        y = entry.bibid if isinstance(entry.bibid, str) else ''
        return x < y

    def __repr__(self):
        global bibkeys
        if self.bibtype == 'preamble':
            # print(f'BibItem.__repr__(): "{self.preamble}"')
            ret = f'@preamble{{{self.preamble}}}'
        else:
            buff = [f'@{self.bibtype}{{{self.bibid}'] + \
                   [f'    {key} = {{{to_bibtex(key, self[key])}}}' \
                       for key in bibkeys if key in self] + \
                   [f'    {key} = {{{val}}}' \
                       for key, val in self.items() if key not in bibkeys]
            ret = ',\n'.join(buff) + '\n}'
        return ret

    def __setitem__(self, key, val):
        '''Overloaded __setitem__() to ensure lowercase keys.'''
        super().__setitem__(key.lower(), val)

    def gets(self, key):
        '''Get key value as a BibTeX-formatted string, or the empty string.'''
        return to_bibtex(key, self.get(key, ''))

    def update(self, fields, overwrite=True):
        '''Update item using fields, overwriting old values by default.'''
        if not isinstance(fields, dict):
            raise TypeError
        if not overwrite:
            item = {key.lower(): val for key, val in fields.items() \
                    if key.lower() not in self}
        else:
            item = fields
        super().update({key.lower(): val  for key, val in item.items()})

    @staticmethod
    def parse(data, lineno=1):
        '''Parse BibItem data from a string.'''
        state = ItemParserState.SKIP
        next_state = ItemParserState.ID
        bibid = None
        curr_key = ''
        curr_value = ''
        brackets = 0
        item = {}
        for c in data:
            # print(c, end='')
            if c == '\n':
                lineno += 1
            if state == ItemParserState.SKIP:
                if c in '{"' and next_state == ItemParserState.VALUE:
                    # print(f'SKIP -> VALUE [-> COMMA]')
                    state = ItemParserState.VALUE
                    next_state = ItemParserState.COMMA
                elif not c.isspace():
                    # print(f'*SKIP -> {next_state.name} [-> SKIP]')
                    state = next_state
                    next_state = ItemParserState.SKIP
                    curr_key = c
            elif state == ItemParserState.ID:
                if c == ',':
                    state = ItemParserState.SKIP
                    next_state = ItemParserState.KEY
                    bibid = curr_key
                    curr_key = ''
                    # print(f'ID ("{bibid}") ->> SKIP [-> KEY]')
                elif not c.isspace():
                    curr_key += c
                else:
                    state = ItemParserState.COMMA
                    next_state = ItemParserState.KEY
                    bibid = curr_key
                    curr_key = ''
                    # print(f'ID ("{bibid}") -> COMMA [-> KEY]')
            elif state == ItemParserState.COMMA:
                if c == ',':
                    # print(f'COMMA -> SKIP [-> KEY]')
                    state = ItemParserState.SKIP
                    next_state = ItemParserState.KEY
                elif not c.isspace():
                    raise MissingCommaError(lineno, c)
            elif state == ItemParserState.KEY:
                if c.isspace():
                    # print(f'KEY ("{curr_key}") -> EQUALS [-> VALUE]')
                    state = ItemParserState.EQUALS
                    next_state = ItemParserState.VALUE
                elif c == '=':
                    # print(f'KEY ("{curr_key}") ->> SKIP [-> VALUE] ')
                    state = ItemParserState.SKIP
                    next_state = ItemParserState.VALUE
                else:
                    curr_key += c
            elif state == ItemParserState.EQUALS:
                if c == '=':
                    # print(f'EQUALS -> SKIP [-> VALUE]')
                    state = ItemParserState.SKIP
                    next_state = ItemParserState.VALUE
                elif not c.isspace():
                    raise ParseError(lineno, c)
            elif state == ItemParserState.VALUE:
                if c == '{':
                    brackets += 1
                elif c == '}' and brackets > 0:
                    brackets -= 1
                elif c == '"' or (c == '}' and brackets == 0):
                    # print(f'VALUE ("{curr_value}") -> COMMA [-> KEY]')
                    state = ItemParserState.COMMA
                    next_state = ItemParserState.KEY
                    item[curr_key] = curr_value
                    curr_key = ''
                    curr_value = ''
                else:
                    curr_value += c
        return BibItem(bibid=bibid, data=item)

class Biblio(dict):
    '''Biblio is a dict of BibEntries.'''

    def __init__(self, filename=None, entries=None):
        self.filename = filename
        if self.filename:
            self.read(filename)
        if entries:
            if isinstance(entries, dict):
                self.update(entries)
            elif isinstance(entries, (list, set)):
                for entry in entries:
                    if not isinstance(entry, BibItem):
                        raise ValueError(entry)
                    self[entry.bibid] = entry
            else:
                raise ValueError(entries)

    def __repr__(self):
        # return '\n\n'.join([repr(entry) for entry in self.values()])
        return '\n\n'.join([repr(entry) for entry in sorted(self.values())])

    def by_bibid(self, bibids):
        '''Fetch all entries whose bibid is in the given list.'''
        return Biblio(entries={k: v for k, v in self.items() if k in bibids})

    def by_regex(self, field, pattern):
        '''Fetch all entries where field matches pattern (a regex).'''
        match = lambda what, where: regex.search(what.gets(where.lower()))
        field = field.lower()
        # Search 'subtitle' field too if 'title' given as the target
        fields = [field] if field != 'title' else [field, 'subtitle']
        regex = re.compile(pattern)
        results = Biblio()
        for f in fields:
            results.update({k: v for k, v in self.items() if match(v, f)})
        return results

    def by_type(self, bibtypes, complement=False):
        '''Fetch all entries of given bibtype(s).'''
        if isinstance(bibtypes, str):
            bibtypes = {bibtypes}
        if complement:
            match = lambda item: item.bibtype not in bibtypes
        else:
            match = lambda item: item.bibtype in bibtypes
        return Biblio(entries={k: v for k, v in self.items() if match(v)})

    def get(self, key, default=None):
        '''Return self[key] if key in self, else return default.

        Provides special handling for key == 'bibid'.'''
        return super().get(key, default) if key != 'bibid' else self.bibid

    def parse(self, buff):
        '''Parse text buffer into a list of BibItems.'''
        global special_types
        state = ParserState.AT
        next_state = ParserState.TYPE
        curr_type = ''
        curr_data = ''
        line = 1
        for c in buff:
            # print(c, end='')
            if c == '\n':
                line += 1
            if state == ParserState.AT and c == '@':
                # print(f'AT -> {next_state.name} [-> SKIP]')
                state = next_state
                next_state = ParserState.SKIP
            elif state == ParserState.TYPE:
                if c.isalpha():
                    curr_type += c
                elif c.isspace():
                    # print(f'TYPE ("{curr_type}") -> {next_state.name} [-> DATA]')
                    state = next_state
                    next_state = ParserState.DATA
                elif c == '{':
                    # print(f'TYPE ("{curr_type}") ->> DATA [-> AT]')
                    brackets = 1
                    state = ParserState.DATA
                    next_state = ParserState.AT
                else:
                    raise ParseError(line, c)
            elif state == ParserState.SKIP and  c == '{':
                # print(f'SKIP -> DATA [-> AT]')
                brackets = 1
                state = ParserState.DATA
                next_state = ParserState.AT
            elif state == ParserState.DATA:
                if c == '}':
                    brackets -= 1
                    if brackets == 0:
                        # print(f'DATA -> {next_state.name} [-> TYPE]')
                        # print(f'data = "{curr_data}"')
                        if curr_type not in special_types:
                            item = BibItem.parse(curr_data, line)
                            item.bibtype = curr_type
                            self[item.bibid] = item
                        elif curr_type == 'preamble':
                            # print(f'curr_data = "{curr_data}"')
                            item = BibItem(bibtype='preamble', rawdata=curr_data)
                            # print(f'item.preamble = "{item.preamble}"')
                            self[item.bibid] = item
                        state = next_state
                        next_state = ParserState.TYPE
                        curr_type = ''
                        curr_data = ''
                    else:
                        curr_data += c
                else:
                    if c == '{':
                        brackets += 1
                    curr_data += c

    def read(self, filename):
        '''Read and parse a BibTeX file.'''
        self.filename = filename
        with open(filename, 'r') as f:
            buff = ''.join([line for line in f])
        self.parse(buff)

    # IS THIS NEEDED? We might just as well print() the bibliography and
    # use `with` context in the caller?
    #
    # def write(self, filename=None, unordered=False):
    #     '''Write the bibliography to a BibTeX file.'''
    #     if not filename and not self.filename:
    #         raise ValueError(filename)
    #     if not filename:
    #         filename = self.filename
    #     with open(filename, 'w') as f:
    #         if unordered:
    #             f.write(repr(self))
    #         # Ensure decent ordering: first preamble, then not-collections,
    #         # then collections—because sometimes BibTeX can’t find crossrefs
    #         # unless they *follow* the reference
    #         else:
    #             f.write(repr(self.by_type('preamble')))
    #             f.write(repr(sorted(self.by_type(['preamble', 'collection'], \
    #                 complement=True))))
    #             f.write(repr(sorted(self.by_type('collection'))))

# Basic test if run as a script
if __name__ == '__main__':
    import sys

    def die(msg):
        print(f'{msg}\n', file=sys.stderr)
        sys.exit(1)

    for name in sys.argv[1:]:
        try:
            db = Biblio(name)
        except FileNotFoundError:
            die(f'File not found: "{name}"')
        except PermissionError:
            die(f'Access denied: "{name}”')
        except IOError:
            die(f'I/O error: "{name}"')
        except ParseError as exc:
            die(f'Parse error on line {exc.lineno}: {exc.err}')
        except DuplicateError as exc:
            die(f'Duplicate ID on line {exc.lineno}: "{exc.err}"')
        except NoIDError as exc:
            die(f'Missing ID on line {exc.lineno}: "{exc.err}"')
        print(db)
