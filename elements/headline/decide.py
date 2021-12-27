# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import statistics

import utila

import elements.headline.lookup
import elements.headline.parser


@utila.cacheme
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
    """
    line = line.strip()
    if utila.similar(elements.HEADLINES, line):
        return True
    if not strict and elements.headline.parser.parse_headline(line):
        if noheadline(line):
            return False
        return True
    return False


@utila.cacheme
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
    >>> noheadline('2 background 9')
    True
    """
    line = line.strip()
    if issentence(line):
        # ignore extracted lists which are interpreted as headlines
        # TODO: CHECK THIS!
        return True
    if line.count('.') > dots_max:
        # filter table items
        # DISKUSSION ................ 36
        return True
    if len(line) < length_min:
        # remove numbers or very short text chunks
        return True
    if line[0] in LISTSTART:
        # just a list
        return True
    if singlechar(line):
        return False
    splitted = line.split()
    if len(splitted) > wordcount_max:
        return True
    if WHITELINE in line:
        # POTENZIALBESCHREIBUNG                 114
        # Do not count spaces to avoid ignoring `long` headlines
        return True
    wordslength = [len(word) for word in splitted]
    mean_words_length = statistics.mean(wordslength)
    if mean_words_length < mean_words_length_min:
        return True
    if TOCLINE.match(line):
        return True
    parsed = elements.headline.parser.parse_headline(line)
    if parsed:
        # title
        if utila.char_rate(parsed[0]) < 0.5:
            return True
    if isheadline(line, strict=strict):
        return False
    return False


# 2 background          9
TOCLINE = utila.compiles(r'^\d{1,2}.{3,}\d{1,3}$')
# \uF0B7
LISTSTART = '•'
WHITELINE = '          '


@utila.cacheme
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


@utila.cacheme
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
