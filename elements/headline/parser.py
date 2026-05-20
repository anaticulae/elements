# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import utilo

import elements
import elements.headline
import elements.headline.lookup


def parse_headline(raw: str, before=None) -> tuple:
    """\
    >>> parse_headline('2. Einleitung')
    ('Einleitung', 1, '2.')

    >>> parse_headline('b. Ergebnisse und Schlussfolgerungen zu Unterfrage 1')
    ('Ergebnisse und Schlussfolgerungen zu Unterfrage 1', 4, 'b.')

    >>> parse_headline('Durchführung der Untersuchung', before='Kapitel 3')  # chapter level
    ('Durchführung der Untersuchung', 1, '')

    >>> parse_headline('2.6.1.1. Hypoxia Inducible Factor')
    ('Hypoxia Inducible Factor', 4, '2.6.1.1.')
    """
    parsed = parse_leveled_headline(raw)
    if parsed:
        rawlevel, title = parsed['level'], parsed['text']
        level = elements.level_numbered(rawlevel)
        if level is False:  # pylint:disable=C2001
            return None
        return title, level, rawlevel
    parsed = parse_chapter_level(raw)
    if parsed:
        title, rawlevel = parsed
        level = 1
        if 'anhang' in rawlevel.lower():
            # ANHANG
            #   ANHANG 1: ZUSAMMENFASSUNG
            #   ANHANG 2: SUMMARY
            level = 2
        return title, level, rawlevel
    if utilo.similar(elements.HEADLINES, raw):
        return raw, 1, ''
    if before:
        # look back and check for `Kapitel-X-Pattern`
        before = utilo.normalize_text(before, normalize_spaces=True)
        chapter = elements.noheadline_pattern(before)
        if chapter:
            return raw, 1, ''
    return None


@configos.cache_large
def parse_leveled_headline(line: str):
    line = line.strip()
    matched = HEADLINE.match(line)
    if matched:
        return matched
    matched = CHARACTER_HEADLINE.match(line)
    if matched:
        return matched
    return None


@configos.cache_large
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


HEADLINE = utilo.compiles(r"""
    ^
    (?P<level>(\d{1,2}\.?){1,4}\d{0,2})
    [ ]{1,5}
    (?P<text>.+?)
    $
""")

CHARACTER_HEADLINE = utilo.compiles(r"""
    ^
    (?P<level>([a-z]{1,2}\.){1,4}[a-z\d]{0,2})
    [ ]{1,5}
    (?P<text>.+?)
    $
""")

HEADLINE_CHAPTER = utilo.compiles(r"""
    ^
    (?P<rawlevel>
        (KAPITEL|CHAPTER|ANHANG|APPENDIX)
        [ ]{0,5}
        (1?\d)      # 0-19  # TODO: MAY INCREASE TO 0-29?
    [ ]{0,5}
    \:
    )
    [ ]{0,5}
    (?P<title>.+)       # TODO: CHECK LAZY `?` OF HEADLINES BEFORE
""")
