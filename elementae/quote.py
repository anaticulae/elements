# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

QUOTES = '"\''


def isquote(text: str) -> bool:
    """\
    >>> isquote('"Improve the development,  using system data."')
    True
    """
    text = text.strip()
    start, end = text[0], text[-1]
    if start in QUOTES and end in QUOTES:
        return True
    return False
