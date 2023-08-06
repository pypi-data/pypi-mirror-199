# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""The `demo` fixture for this plugin."""

from lino.api import rt, _


def objects():
    Team = rt.models.teams.Team
    yield Team(name="Eupen", ref="E")
    yield Team(name="St. Vith", ref="S")

