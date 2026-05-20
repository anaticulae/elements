# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import configos
import iamraw
import iamraw.toc
import utilo

import elements.headline.level
import elements.headline.lookup

TOC_NUMBERED_RATE_MIN = configos.HolyRate(items=(
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

TOC_SECTIONS_RATE_MIN = configos.HV_PERCENT_PLUS(default=65)

TOC_STEPPED_RATE_MIN = configos.HV_PERCENT_PLUS(default=65)

TOC_NOLEVEL_RATE_MIN = configos.HV_PERCENT_PLUS(default=65)


class InvalidTocItems(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def toc_flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        if not hasattr(item, '__getitem__'):
            return
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
    if utilo.similar(
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


def istocnumbered(toc, rate_min: callable = TOC_NUMBERED_RATE_MIN) -> bool:
    """Decide if a toc contains headlines with numbered pattern."""
    if not toc:
        return True
    toc = toc_flat(toc)
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
    toc = toc_flat(toc)
    levels = len([item for item in toc if item.level is None])
    rate = levels / len(toc)
    if rate < TOC_NOLEVEL_RATE_MIN:
        return False
    return True


LEVEL_SECTIONS_SECTION = utilo.compiles(r'^(SECTION)[ ]{1,3}\d{1,2}\:')
LEVEL_SECTIONS_PART = utilo.compiles(r'^(PART)[ ]{1,3}\d{1,2}\:')


@configos.cache_large
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
    """Decide if a toc contains headlines with sections pattern."""
    if not toc:
        return False
    toc = toc_flat(toc)
    levels = len([
        item for item in toc
        if item.level and level_sections(item.level) in {1, 2}
    ])
    rate = levels / len(toc)
    if rate < TOC_SECTIONS_RATE_MIN:
        return False
    return True


def istocstepped(toc) -> bool:
    """Decide if a toc contains headlines with stepped pattern."""
    if not toc:
        return False
    toc = toc_flat(toc)
    levels = [
        item for item in toc if elements.headline.level.level_steps(item.level)
    ]
    rate = utilo.rate_rel(
        levels,
        toc,
    )
    if rate < TOC_STEPPED_RATE_MIN:
        return False
    return True
