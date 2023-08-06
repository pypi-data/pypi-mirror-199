# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""The :ref:`voga` extension of :mod:`lino_xl.lib.invoicing`.

This adds a new field :attr:`course
<lino_voga.lib.invoicing.models.Plan.course>` to the invoicing plan
and a "basket" button to the Course model.

.. autosummary::
   :toctree:

    models
    fixtures.demo_bookings


"""

raise Excption("User lino_xl.lib.invoicing.order_model instead")

from lino_xl.lib.invoicing import Plugin, _


class Plugin(Plugin):

    extends_models = ['Plan']
