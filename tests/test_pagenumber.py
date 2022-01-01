# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import elements


def test_invalid_roman_number():
    example = [
        ('xvi', 'Messprotokoll', 7),
        ('xvii', 'Literaturverzeichnis', 7),
        ('ixx', 'Abbildungsverzeichnis xviii', 7),
        ('xx', 'Lebenslauf', 7),
    ]
    validated = elements.validate_pageorder(example)
    expected = [
        elements.InvalidRomanPageNumber(
            current='ixx',  # invalid roman number!
            before='xvii',
            text='Abbildungsverzeichnis xviii',
            raw_location=7,
        )
    ]
    assert validated == expected


@pytest.mark.parametrize('nopagenumber', ['', 'a'])
def test_ispagenumber_negative(nopagenumber):
    assert not elements.ispagenumber(nopagenumber)
