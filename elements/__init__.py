#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import elements.__patch__
from elements.caption import iscaption
from elements.caption import iscaption_code
from elements.caption import iscaption_figure
from elements.caption import iscaption_table
from elements.headline.decide import isheadline
from elements.headline.decide import noheadline
from elements.headline.decide import noheadline_pattern
from elements.headline.decide import singlechar
from elements.headline.level import level_numbered
from elements.headline.lookup import HEADLINES
from elements.pagenumber import InvalidPage
from elements.pagenumber import InvalidPages
from elements.pagenumber import InvalidRomanPageNumber
from elements.pagenumber import isnumber_withgaps
from elements.pagenumber import ispagenumber
from elements.pagenumber import validate_pageorder
from elements.pagenumber import validate_toc
from elements.quote import isquote
from elements.toc import istoc
from elements.toc import toc_flat

__version__ = '0.12.1'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
