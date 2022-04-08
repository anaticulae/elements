# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import re

import utila


@utila.cacheme
def level_numbered(raw: str) -> int:
    """Convert number to raw level.

    >>> level_numbered('0 Einleitung')
    1
    >>> level_numbered('5 Geology')
    1
    >>> level_numbered('2.1.3. Abschluss')
    3
    >>> level_numbered('a. Gesamtbewertung')
    4
    >>> level_numbered('Kapitel 1: Dies ist eine Überschrift')
    1
    >>> level_numbered('A. Gesamtbewertung')
    1
    """
    # TODO: SUPPORT LEVEL WITHOUT SPACE
    raw = raw.strip()
    if not raw:
        return None
    for strategy in (
            level_numbered_dots,
            level_numbered_chars,
            level_chapters,
    ):
        parsed = strategy(raw)
        if parsed is not None:
            return parsed
    return None


@utila.cacheme
def level_steps(raw: str) -> int:  # pylint:disable=R0911
    """Convert number to raw level.

    Example:
        A Lateinische Buchstaben
            I. Roman numbers
                1. Arabische Zahlen
                    a. Lateinische Kleinbuchstaben

    >>> level_steps('KAPITEL 1 WAS IST HUMAN SECURITY?')
    1
    >>> level_steps('A. Was ist Sicherheit?')
    2
    >>> level_steps('III. Umwelt und Klimawandel')
    3
    >>> level_steps('2. Politische und wenige(r) rechtliche Aspekte')
    4
    >>> level_steps('a) Konzepte')
    5
    >>> level_steps('dd) Bewertung')
    6
    """
    raw = raw.strip() if raw else None
    if not raw:
        return 1
    if re.match(r'^(KAPITEL)[ ]{1,3}\d{1,2}', raw, re.IGNORECASE):
        return 1
    if re.match(r'^(A|B|C|D|E|F|G|H)\.', raw, re.IGNORECASE):
        return 2
    if re.match(r'^(I|II|III|IIII|IV|V|VI|VII|VIII)\.?', raw, re.IGNORECASE):
        return 3
    if re.match(r'^\d{1,2}\.', raw, re.IGNORECASE):
        return 4
    if re.match(r'^[a-h]\)', raw, re.IGNORECASE):
        return 5
    if re.match(r'^[a-h]{2}\)', raw, re.IGNORECASE):
        return 6
    return None


def level_numbered_dots(raw: str) -> int:
    """\
    >>> assert level_numbered_dots('A.1.1.') is None
    >>> level_numbered_dots('6.0 Ausblick is')
    1
    """
    raw = raw.split()[0]
    try:
        splitted = [int(item) for item in raw.split('.') if item]
        if max(splitted) > 20:
            return False
    except ValueError:
        return None
    if len(splitted) > 1 and splitted[-1] == 0:  # pylint:disable=compare-to-zero
        # 6.0 Ausblick is
        splitted = splitted[:-1]
    return len(splitted)


CHAR_PATTERN = re.compile(r'^[A-Z]\.', re.IGNORECASE)

APPENDIX_PATTERN_FIRST = re.compile(r'^[A-Z](\.|[ ])')

APPENDIX_PATTERN_SECOND = re.compile(r'^[A-Z]\.\d{1,2}\.?')

APPENDIX_PATTERN_THIRD = re.compile(r'^[A-Z]\.\d{1,2}\.\d{1,2}\.?')


def level_numbered_chars(raw: str) -> int:
    """\
    >>> level_numbered_chars('d. Gesamtbewertung')
    4
    >>> level_numbered_chars('A.10.Vorgehen S-Funktionen')
    2
    >>> level_numbered_chars('A.1 Parameter')
    2
    """
    if not CHAR_PATTERN.match(raw):
        return None
    if APPENDIX_PATTERN_THIRD.match(raw):
        return 3
    if APPENDIX_PATTERN_SECOND.match(raw):
        return 2
    if APPENDIX_PATTERN_FIRST.match(raw):
        return 1
    return 4


CHAPTER_PATTERN = re.compile(r'^Kapitel[ ]{0,3}\d{1,2}[\:\.]', re.IGNORECASE)


def level_chapters(raw: str) -> int:
    """\
    >>> level_chapters('Kapitel 1: Dies ist eine Überschrift')
    1
    """
    if not CHAPTER_PATTERN.match(raw):
        return None
    return 1


CHAPTER = utila.compiles(r"""
    ^
    (KAPITEL|CHAPTER)
    [ ]{0,3}
    (\d{1,2})
""")


def determine_patch(raw: str) -> int:
    """\
    >>> determine_patch('1.4.2')
    2
    >>> determine_patch('1.0.')
    0
    >>> determine_patch('1.')
    1
    >>> determine_patch('b.')
    2
    >>> determine_patch('c.')
    3
    >>> determine_patch('d.')
    4
    >>> determine_patch('Kapitel 6:')
    6
    >>> determine_patch('CHAPTER 8:')
    8
    """
    if not raw:
        return None
    if matched := CHAPTER.match(raw):
        return int(matched[2])
    splitted = [item for item in raw.rsplit('.') if item]
    if not splitted:
        return None
    with contextlib.suppress(ValueError):
        last = splitted[-1]
        for index, char in enumerate('abcdefgh', start=1):
            last = last.replace(char, str(index))
        return int(last)
    return 0
