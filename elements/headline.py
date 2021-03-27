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

import elements

HEADLINES = """\
Anhang
Anhangsverzeichnis
Bibliografie
Eidesstattliche Erklärung
Eidesstattliche Versicherung
Einleitung
Erklärung
Internetquellen
Literaturverzeichnis
Quellenverzeichnis
Vorwort
Zeitschriftenartikel"""
HEADLINES = utila.splitlines(HEADLINES)  # pylint:disable=R0204


def isheadline(line: str, strict: bool = True) -> bool:
    """\
    >>> isheadline('1. Einleitung', strict=False)
    True
    >>> isheadline('Eidesstattliche Versicherung')
    True
    """
    line = line.strip()
    if utila.similar(HEADLINES, line):
        return True
    if not strict and parse_headline(line):
        return True
    return False


def noheadline(  # pylint:disable=R0911
        line: str,
        length_min: int = 5,
        wordcount_max: int = 15,
        mean_words_length_min: float = 3.0,
        strict: bool = True,
) -> bool:
    """\
    >>> noheadline(' Anzahl der Transaktionen')
    True
    """
    line = line.strip()
    if issentence(line):
        # ignore extracted lists which are interpreted as headlines
        # TODO: CHECK THIS!
        return True
    if line.count('.') > 5:
        # filter table items
        # DISKUSSION ................ 36
        return True
    if len(line) < length_min:
        # remove numbers or very short text chunks
        return True
    if len(line.split()) > wordcount_max:
        return True
    if ' ' * 10 in line:
        # POTENZIALBESCHREIBUNG                 114
        # Do not count spaces to avoid ignoring `long` headlines
        return True
    wordslength = [len(word) for word in line.split()]
    mean_words_length = statistics.mean(wordslength)
    if mean_words_length < mean_words_length_min:
        return True
    # \uF0B7
    if '' in line:
        return True
    if isheadline(line, strict=strict):
        return False
    return False


def parse_headline(raw: str, before=None):  # pylint:disable=R0911
    """\
    >>> parse_headline('2. Einleitung')
    ('Einleitung', 1, '2.')
    >>> parse_headline('b. Ergebnisse und Schlussfolgerungen zu Unterfrage 1')
    ('Ergebnisse und Schlussfolgerungen zu Unterfrage 1', 4, 'b.')
    """
    parsed = parse_leveled_headline(raw)
    if parsed:
        rawlevel, title = parsed['level'], parsed['text']
        level = elements.level_numbered(rawlevel)
        if level is False:
            return None
        return title, level, rawlevel
    parsed = parse_chapter_level(raw)
    if parsed:
        title, rawlevel = parsed
        level = 1  # pylint:disable=R0204
        if 'anhang' in rawlevel.lower():
            # ANHANG
            #   ANHANG 1: ZUSAMMENFASSUNG
            #   ANHANG 2: SUMMARY
            level = 2
        return title, level, rawlevel
    if utila.similar(HEADLINES, raw):
        return raw, 1, ''
    if before:
        # look back and check for `Kapitel-X-Pattern`
        before = plain(before)
        chapter = noheadeline_pattern(before)
        if chapter:
            return raw, 1, ''
    if not utila.similar(HEADLINES, raw):
        return None
    return raw, None, ''


HEADLINE = re.compile(
    ('^'
     r'(?P<level>(\d{1,2}\.?)+\d{0,2})'
     r'[ ]{1,5}'
     r'(?P<text>.+?)'
     '$'),
    re.VERBOSE,
)

CHARACTER_HEADLINE = re.compile(
    ('^'
     r'(?P<level>([a-z]{1,2}\.)+[a-z\d]{0,2})'
     r'[ ]{1,5}'
     r'(?P<text>.+?)'
     '$'),
    re.VERBOSE | re.IGNORECASE,
)


def parse_leveled_headline(line):
    line = line.strip()
    matched = re.match(HEADLINE, line)
    if matched:
        return matched
    matched = re.match(CHARACTER_HEADLINE, line)
    if matched:
        return matched
    return None


HEADLINE_CHAPTER = re.compile(
    r"""
    ^
    (?P<rawlevel>
        (KAPITEL|CHAPTER|ANHANG|APPENDIX)
        [ ]{0,5}
        \d{1,2}
    [ ]{0,5}
    \:
    )
    [ ]{0,5}
    (?P<title>.+)
""",
    re.VERBOSE | re.I,
)


def parse_chapter_level(raw: str) -> tuple:
    """\
    >>> parse_chapter_level('KAPITEL 1: EINLEITUNG')
    ('EINLEITUNG', 'KAPITEL 1:')
    >>> parse_chapter_level('KAPITEL 5: FÜR EINE BÜRGERNAHE UND DEMOKRATISCH LEGITIMIERTE EUROPÄISCH')
    ('FÜR EINE BÜRGERNAHE UND DEMOKRATISCH LEGITIMIERTE EUROPÄISCH', 'KAPITEL 5:')
    """
    parsed = HEADLINE_CHAPTER.match(raw)
    if not parsed:
        return None
    title, rawlevel = parsed['title'], parsed['rawlevel']
    return title, rawlevel


NOHEADLINE_CHAPTER = re.compile(
    r'(Kapitel|Chapter|Anhang|Appendix)[ ]{0,5}\d{1,2}$',
    re.IGNORECASE,
)
NOHEADLINE_APPENDIX = re.compile(
    r'(Anhang|Appendix)[ ]{0,5}[A-Z]$',
    re.IGNORECASE,
)


def noheadeline_pattern(item: str) -> bool:
    """\
    >>> noheadeline_pattern('KAPITEL  1 ')
    True
    >>> noheadeline_pattern('Chapter 5 ')
    True
    >>> noheadeline_pattern('ANHANG A')
    True
    """
    item = item.strip()
    if NOHEADLINE_CHAPTER.match(item):
        return True
    if NOHEADLINE_APPENDIX.match(item):
        return True
    return False


def plain(items: list) -> str:
    # TODO: REPLACE WITH UTILA CODE
    raw = ' '.join([item.text.strip() for item in items])
    return raw


def issentence(line: str):
    # TODO: IMPROVE THIS
    # TODO: USE BIG FIVE FEATURES
    return line.strip().endswith('.')
