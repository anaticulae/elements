# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import statistics

import configo
import utila

import elements
import elements.headline.lookup
import elements.headline.parser


@configo.cache_large
def isheadline(line: str, strict: bool = True) -> bool:
    """\
    >>> isheadline('1. Einleitung', strict=False)
    True
    >>> isheadline('Eidesstattliche Versicherung')
    True
    >>> isheadline('A B S T R A C T')
    True
    >>> isheadline('H a l l o w i e')
    False
    >>> isheadline('Integrationstest Einlesen', strict=True)
    False
    >>> isheadline('4 https://github.com/prometheus/node_exporter')
    False
    >>> isheadline('12. Literaturverzeichnis:')
    True
    """
    line = line.strip()
    if utila.verysimilar(current=line, expected=elements.HEADLINES):
        return True
    if not strict and elements.headline.parser.parse_headline(line):
        if noheadline(line):
            return False
        return True
    return False


@configo.cache_large
def noheadline(  # pylint:disable=R0911,R1260
    line: str,
    length_min: int = 5,
    wordcount_max: int = 15,
    dots_max: int = 5,
    mean_words_length_min: float = 3.0,
    strict: bool = True,
) -> bool:
    """\
    >>> noheadline(' Anzahl der Transaktionen')
    True
    >>> noheadline('• count')
    True
    >>> noheadline('u.u.a 10')
    True
    >>> noheadline('A B S T R A C T')
    False
    >>> noheadline('[77] Alexander Keller. Methods and Apparatus for Topology Discovery')
    True
    >>> noheadline('risk_total_kons = b0 + b1   sex + b2   age + b3    v_total_r')
    True
    >>> noheadline('z.B.  sogenannte  "Patentboxen"  gegenüber')
    True

    # TODO: THATS CONFUSING, THINK ABOUT SOLVING THIS ISSUE
    # IS WITHOUT SPACES TO STRICT?
    >>> noheadline('2 background 9') # tocline
    True
    >>> noheadline('2  Methode3') # highnote
    False
    >>> noheadline('Wirtschaftsforschung 82 (1), S.61-75.')
    True
    >>> noheadline('4 https://github.com/prometheus/node_exporter')
    True
    """
    line = line.strip()
    if len(line) < length_min:
        # remove numbers or very short text chunks
        return True
    if line.count('.') > dots_max:
        # filter table items
        # DISKUSSION ................ 36
        return True
    if (returnvalue := noheadline_simple(line)) is not None:
        return returnvalue
    splitted = line.split()
    if len(splitted) > wordcount_max:
        return True
    wordslength = [len(word) for word in splitted]
    mean_words_length = statistics.mean(wordslength)
    if mean_words_length < mean_words_length_min:
        return True
    parsed = elements.headline.parser.parse_headline(line)
    if parsed:
        # title
        if utila.char_rate(parsed[0]) < 0.5:
            return True
    if elements.isquote(line):
        return True
    if isheadline(line, strict=strict):
        return False
    return False


def noheadline_simple(line: str) -> bool:  # pylint:disable=R0911,R1260
    """\
    >>> noheadline_simple('[Fos10] FOSTER, Elvis C.: Software Engineering - A Methodical Approach. Xlibris')
    True
    >>> noheadline_simple('8. Auflage, Springer-Verlag, Heidelberg (2010)')
    True
    """
    if issentence(line):
        # ignore extracted lists which are interpreted as headlines
        # TODO: CHECK THIS!
        return True
    if line[0] in LISTSTART:
        # just a list
        return True
    if singlechar(line):
        return False
    if ABBR_START.match(line):
        return True
    if WHITELINE in line:
        # POTENZIALBESCHREIBUNG                 114
        # Do not count spaces to avoid ignoring `long` headlines
        return True
    for pattern in (TOCLINE, BIBLINE, BIBLINE_AUFLAGE):
        if pattern.match(line):
            return True
    if HTTP.search(line):
        return True
    if PERSON.search(line):
        return True
    if too_many_invalid_headline_chars(line):
        return True
    # NONE SIGNALS THAT NO PATTERN WAS DETECTED
    return None


def too_many_invalid_headline_chars(text: str) -> bool:
    """\
    >>> too_many_invalid_headline_chars('risk_total_kons = b0 + b1   sex + b2   age + b3    v_total_r')
    True
    """
    special = 0
    for char in '+-=_!@#$%^&*':
        special += text.count(char)
    special += len(utila.parse_numbers(text))
    if special > 5:
        return True
    return False


HTTP = utila.compiles(r"""
    http
    [s]{0,1}
    \:
    //
""")
# 2 background          9
TOCLINE = utila.compiles(r"""
    ^
    \d{1,2}
    .{3,120}
    [ ]{1,45}
    \d{1,3}
    $
""")
# [77] Alexander Keller. Methods and Apparatus for Topology Discovery
# [Fos10] FOSTER, Elvis C.: Software Engineering
BIBLINE = utila.compiles(r"""
    ^
    \[
        \s{0,2}
        (
            \d{1,3}|
            [\w\d\.]{1,6}
        )
        \s{0,2}
    \]
""")
# 8. Auflage, Springer-Verlag, Heidelberg (2010)
BIBLINE_AUFLAGE = utila.compiles(r"""
    ^
    \d{1,2}\.
    [ ]{0,2}
    Auflage
    .{0,90}
    \(\d{4}\)
""")
# \uF0B7
LISTSTART = '•\uf0a7\uf0b7'
WHITELINE = '          '
ABBR_START = utila.compiles(r"""
    ^
    (
        d\.h\.|
        e\.v\.|
        i\.o\.|
        k\.j\.|
        o\.s\.|
        u\.a\.|
        z\.b\.|
        \d{2}\.\d{2}\.\d{2} # TODO: MOVE THIS DATE
    )
""")
PERSON = utila.compiles(r"""
    (
        prof\.[ ]{1,3}dr\.|
        dr\.(\-|[ ]{1,3})ing\.
    )
""")


@configo.cache_large
def noheadline_pattern(item: str) -> bool:
    """\
    >>> noheadline_pattern('KAPITEL  1 ')
    True
    >>> noheadline_pattern('Chapter 5 ')
    True
    >>> noheadline_pattern('ANHANG A')
    True
    >>> noheadline_pattern('KAPITEL 1: EINLEITUNG')
    False
    """
    item = item.strip()
    if NOHEADLINE_CHAPTER.match(item):
        return True
    if NOHEADLINE_APPENDIX.match(item):
        return True
    return False


@configo.cache_large
def singlechar(text: str) -> bool:
    """\
    >>> singlechar('A B S T R A C T')
    True
    >>> singlechar('  ')
    False
    >>> singlechar('2 background 9')
    False
    """
    if not text:
        return False
    splitted = [len(token) for token in text.strip().split()]
    if not splitted:
        return False
    median = statistics.mean(splitted)
    if median == 1:
        return True
    return False


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')


NOHEADLINE_CHAPTER = re.compile(
    r'(Kapitel|Chapter|Anhang|Appendix)[ ]{0,5}\d{1,2}$',
    re.IGNORECASE,
)
NOHEADLINE_APPENDIX = re.compile(
    r'(Anhang|Appendix)[ ]{0,5}[A-Z]$',
    re.IGNORECASE,
)
