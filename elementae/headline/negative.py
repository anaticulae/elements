# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo


def noheadline(text: str) -> bool:
    """\
    >>> noheadline('name:')
    True
    >>> noheadline('genehmigte   Dissertation')
    True
    """
    text = text.strip(' .:;,?$#')
    text = text.lower()
    if text in NOHEADLINE:
        return True
    text = utilo.normalize_whitespaces(text)
    if text in NOHEADLINE:
        return True
    return False


NOHEADLINE = utilo.splitlines("""\
name
vorgelegt von
promotionsausschuss
genehmigte Dissertation
""")
