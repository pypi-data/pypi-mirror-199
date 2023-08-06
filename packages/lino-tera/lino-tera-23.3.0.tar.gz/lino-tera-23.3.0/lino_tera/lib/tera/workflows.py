# -*- coding: UTF-8 -*-
# Copyright 2016-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for :ref:`tera` applications.

This workflow requires that both :mod:`lino_xl.lib.cal` and
:mod:`lino_xl.lib.courses` are installed.

"""

from lino.api import _

# If we want to change the text and/or button_text of a state, we must
# do this *before* workflow modules are loaded because transition
# actions would otherwise get the unchanged text or button_text.
from lino_xl.lib.cal.choicelists import EntryStates, GuestStates
EntryStates.cancelled.button_text = "⚕"
EntryStates.cancelled.text = _("Called off")
EntryStates.draft.text = _("Scheduled")

from lino_xl.lib.cal.workflows.voga import *
from lino_xl.lib.courses.workflows.std import *

add = EntryStates.add_item
add('60', _("Missed"), 'missed', fixed=True,
    help_text=_("Guest missed the appointment."),
    button_text="☉", noauto=True)  # \u2609 SUN

EntryStates.missed.add_transition(
    required_states='cancelled suggested draft took_place')

EntryStates.took_place.guest_state = GuestStates.present
EntryStates.cancelled.guest_state = GuestStates.excused
EntryStates.missed.guest_state = GuestStates.missing

EntryStates.ignore_required_states = True
