# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Page order validator
====================

There are two different types of page numbers. The common **Arabic
Numbers (0,1,3,...)** and **Roman Numbers (I, II, III, ...)**. Arabic
numbers are mainly used for page content and Roman numbers for tables
etc.

In some works Roman numbers are nor used anymore cause there are a
relict of old times. Arabic numbers are used for the whole document.
"""

import dataclasses

import configo
import iamraw
import iamraw.toc
import utila

import elements


@dataclasses.dataclass
class InvalidPage:
    current: str
    before: str
    text: str
    raw_location: int = None


@dataclasses.dataclass
class InvalidRomanPageNumber(InvalidPage):
    pass


InvalidPages = list[InvalidPage]


def validate_toc(toc: iamraw.Toc) -> InvalidPages:
    toc = elements.toc_flat(toc)
    items = [(item.page, item.title, item.raw_location) for item in toc]
    result = validate_pageorder(items)
    return result


def validate_pageorder(items) -> InvalidPages:
    """Validate list of (page number, page number raw/description). The
    number can contain roman and arabic numbers.

    >>> validate_pageorder([('1', 'Einleitung 1', 1), ('2', 'Beschreibung 2', 1)])
    []
    >>> validate_pageorder([('II', 'Anhang II', 1), ('I', 'Inhaltsverzeichnis I', 1)])
    [InvalidPage(current='I', before='II', text='Inhaltsverzeichnis I', raw_location=1)]
    """
    # TODO: MOVE TO A MORE GENERAL PLACE/NAME
    result = []
    arabic = 0
    roman = 'I'
    for pagenumber, title, raw_location in items:
        if pagenumber is None:
            utila.error(f'missing {pagenumber} {title} {raw_location}')
            continue
        if raw_location is None:
            utila.error(f'no `raw_location` for toc: `{title}`')
            raw_location = 0  # TODO: REMOVE LATER
        raw_location = int(raw_location)
        try:
            current_arabic = int(pagenumber)
            if current_arabic < arabic:
                # invald
                result.append(
                    InvalidPage(
                        current_arabic,
                        arabic,
                        title,
                        raw_location=raw_location,
                    ))
            arabic = current_arabic
        except ValueError:
            current_roman = utila.arabic(pagenumber)
            if current_roman is None:
                # invalid roman number `ixx` correct is `xix`
                result.append(
                    InvalidRomanPageNumber(
                        pagenumber,
                        roman,
                        title,
                        raw_location=raw_location,
                    ))
                continue
            if current_roman < utila.arabic(roman):
                result.append(
                    InvalidPage(
                        pagenumber,
                        roman,
                        title,
                        raw_location=raw_location,
                    ))
            roman = pagenumber
    return result


@configo.cache_large
def ispagenumber(number: str) -> bool:  # pylint:disable=R0911
    """Determine if passed `number` is a page number.

    Empty `number` is not a page number.

    Args:
        number(str): string to check if it is a number
    Returns:
        True if roman or numeric number is given

    >>> ispagenumber('99')
    True
    >>> ispagenumber('-1-')
    True
    >>> ispagenumber('iv')
    True
    >>> ispagenumber('32/54')
    True
    >>> ispagenumber('0.5')
    False
    >>> ispagenumber('080315015325')
    False
    >>> ispagenumber('204-06')
    False
    >>> ispagenumber('Page 6 of 16')
    True
    >>> ispagenumber('Page 733')
    True
    >>> ispagenumber('733 von 999')
    True
    >>> ispagenumber('Page 3 sur 19')
    True
    """
    # - 1 -, -2-,
    number = str(number).strip('- ')
    if not number:
        return False
    if number.isnumeric():
        if len(number) > 5:
            return False
        return True
    if utila.isroman(number):
        return True
    if SEPARATED_PAGENUMBERS.match(number):
        return True
    if isnumber_withgaps(number):
        return True
    if COMPLEX_PAGENUMBER.match(number):
        return True
    return False


COMPLEX_PAGENUMBER = utila.compiles(r"""
    ^
    \d{0,3}             # TODO: WHY?
    [ ]{0,3}
    (
        (Seite|Page)
        [ ]{0,3}
        (
            \d{1,3}
        )
        (
            [ ]{0,3}
            (von|of|sur)
            [ ]{0,3}
            \d{1,3}
        )?
    )
    |
    (
        (
            \d{1,3}
        )
        [ ]{0,3}
        (von|of|sur)
        [ ]{0,3}
        \d{1,3}
    )
""")

SEPARATED_PAGENUMBERS = utila.compiles(r'^\d{1,3}/\d{1,3}')


def isnumber_withgaps(text: str, maxgaps: int = 1) -> bool:
    """\
    >>> isnumber_withgaps('11 4')
    True
    >>> isnumber_withgaps('1337')
    True
    """
    text = text.strip()
    if not text:
        return False
    if text.count(' ') > maxgaps:
        return False
    text = text.replace(' ', '')
    if text.isnumeric():
        return True
    return False
