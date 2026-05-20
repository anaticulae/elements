# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import elementae


def test_invalid_roman_number():
    example = [
        ('xvi', 'Messprotokoll', 7),
        ('xvii', 'Literaturverzeichnis', 7),
        ('ixx', 'Abbildungsverzeichnis xviii', 7),
        ('xx', 'Lebenslauf', 7),
    ]
    validated = elementae.validate_pageorder(example)
    expected = [
        elementae.InvalidRomanPageNumber(
            current='ixx',  # invalid roman number!
            before='xvii',
            text='Abbildungsverzeichnis xviii',
            raw_location=7,
        )
    ]
    assert validated == expected


@pytest.mark.parametrize('nopagenumber', ['', 'a'])
def test_ispagenumber_negative(nopagenumber):
    assert not elementae.ispagenumber(nopagenumber)
