# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re

import configo
import iamraw
import iamraw.toc
import utila

import elements.headline.level
import elements.headline.lookup


class InvalidTocItems(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def toc_flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result


def istoc(headline: str) -> bool:
    """\
    >>> istoc('Inhaltverzeichnis')
    True
    """
    if utila.similar(
            current=headline,
            expected=elements.headline.lookup.TOC,
            maxdiff=0.9,
    ):
        return True
    return False


def toc_style(
    toc: iamraw.TocLinkMixin,
    toc_length_min: int = 8,
) -> iamraw.TocStyle:
    """\
    >>> assert toc_style(iamraw.Toc()) is None
    """
    if not toc:
        return None
    if len(toc) < toc_length_min:
        return iamraw.TocStyle.NUMBERED
    if istocsections(toc):
        return iamraw.TocStyle.SECTIONED
    if istocstepped(toc):
        return iamraw.TocStyle.STEPPED
    if istocnolevel(toc):
        return iamraw.TocStyle.FIRSTLEVEL_ONLY
    return iamraw.TocStyle.NUMBERED


TOC_NUMBERED_MIN = configo.HolyRate(items=(
    (1, 1),
    (5, 3),
    (8, 4),
    (10, 5),
    (15, 10),
    (20, 15),
    (30, 22),
    (40, 30),
    (50, 40),
    (60, 50),
))


def istocnumbered(toc, rate_min: callable = TOC_NUMBERED_MIN) -> bool:
    """Decide if a toc contains headlines with numbered or steps pattern."""
    if not toc:
        return True
    levels = len([
        item for item in toc if item.level and
        elements.headline.level.level_numbered_dots(item.level)
    ])
    rate_min: float = rate_min(len(toc))
    rate = levels / len(toc)
    if rate < rate_min:
        return False
    return True


def istocnolevel(toc) -> bool:
    if not toc:
        return False
    levels = len([item for item in toc if item.level is None])
    rate = levels / len(toc)
    if rate < 0.65:  # TODO: HOLY VALUE
        return False
    return True


LEVEL_SECTIONS_SECTION = utila.compiles(r'^(SECTION)[ ]{1,3}\d{1,2}\:')
LEVEL_SECTIONS_PART = utila.compiles(r'^(PART)[ ]{1,3}\d{1,2}\:')


@utila.cacheme
def level_sections(raw: str) -> int:  # pylint:disable=R0911
    """Convert number to raw level.

    Example:

        Section 3: Data
        Section 4: Methodology
        Section 5: Results
            Part 1: Time series analysis
            Part 2: Looking for pair-wise cointegration
                Cointegrating pairs

    >>> level_sections('Section 1: Introduction')
    1
    >>> level_sections('Part 3:Was ist Sicherheit?')
    2
    >>> level_sections('Umwelt und Klimawandel')
    3
    """
    raw = raw.strip() if raw else None
    if not raw:
        return 3
    if LEVEL_SECTIONS_SECTION.match(raw):
        return 1
    if LEVEL_SECTIONS_PART.match(raw):
        return 2
    return 3


def istocsections(toc) -> bool:
    """Decide if a toc contains headlines with numbered or steps pattern."""
    if not toc:
        return False
    levels = len([
        item for item in toc
        if item.level and level_sections(item.level) in (1, 2)
    ])
    rate = levels / len(toc)
    if rate < 0.65:  # TODO: HOLY VALUE
        return False
    return True


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


def istocstepped(toc) -> bool:
    """Decide if a toc contains headlines with numbered or steps pattern."""
    if not toc:
        return False
    levels = len([item for item in toc if level_steps(item.level)])
    rate = levels / len(toc)
    if rate < 0.65:  # TODO: HOLY VALUE
        return False
    return True
