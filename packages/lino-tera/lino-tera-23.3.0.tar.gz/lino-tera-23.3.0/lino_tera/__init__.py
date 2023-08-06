# -*- coding: UTF-8 -*-
# Copyright 2014-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This is the main module of Lino Tera.

.. autosummary::
   :toctree:

   lib


"""

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO['version']

srcref_url = 'https://gitlab.com/lino-framework/tera/blob/master/%s'
# doc_trees = ['docs', 'dedocs']
intersphinx_urls = {
    'docs' : "https://tera.lino-framework.org/",
    'dedocs' : "https://tera.lino-framework.org/de/",
}
