# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re


def level_numbered(raw: str) -> int:
    """Convert number to raw level.

    >>> level_numbered('5 Geology')
    1
    >>> level_numbered('2.1.3. Abschluss')
    3
    >>> level_numbered('a. Gesamtbewertung')
    4
    >>> level_numbered('Kapitel 1: Dies ist eine Überschrift')
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


def level_numbered_dots(raw: str) -> int:
    raw = raw.split()[0]
    try:
        splitted = [int(item) for item in raw.split('.') if item]
        if max(splitted) > 20:
            return False
    except ValueError:
        return None
    return len(splitted)


CHAR_PATTERN = re.compile(r'^[A-Z]\.', re.IGNORECASE)
APPENDIX_PATTERN = re.compile(r'^[A-Z]\.\d{1,2}\.?', re.IGNORECASE)


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
    if APPENDIX_PATTERN.match(raw):
        return 2
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
