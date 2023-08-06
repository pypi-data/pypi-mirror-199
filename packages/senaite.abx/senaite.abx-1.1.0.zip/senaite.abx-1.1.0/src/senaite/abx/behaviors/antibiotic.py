# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.ABX.
#
# SENAITE.ABX is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020-2023 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from senaite.abx import messageFactory as _
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidget
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IAntibioticBehavior(model.Schema):

    abbreviation = schema.TextLine(
        title=_(u"Abbreviation"),
        required=True,
    )

    antibiotic_class = UIDReferenceField(
        title=_(u"Antibiotic class"),
        allowed_types=("AntibioticClass", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "antibiotic_class",
        UIDReferenceWidget,
        display_template="<a href='${url}'>${title}</a>",
        query={
            "portal_type": "AntibioticClass",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        columns=[
            {
                "name": "title",
                "label": _(u"column_label_title", default=u"Title"),
            }
        ],
        catalog=SETUP_CATALOG
    )


@implementer(IAntibioticBehavior)
@adapter(IDexterityContent)
class Antibiotic(object):

    def __init__(self, context):
        self.context = context

    def _get_abbreviation(self):
        return getattr(self.context, "abbreviation", "")

    def _set_abbreviation(self, value):
        value = value and value.strip()
        self.context.abbreviation = value

    abbreviation = property(_get_abbreviation, _set_abbreviation)

    def _get_antibiotic_class(self):
        uid = getattr(self.context, "antibiotic_class", None)
        if not uid:
            return None
        if isinstance(uid, list):
            uid = uid[0]
        return uid

    def _set_antibiotic_class(self, value):
        if api.is_uid(value) or api.is_dexterity_content(value):
            value = api.get_uid(value)
            self.context.antibiotic_class = value

    antibiotic_class = property(_get_antibiotic_class, _set_antibiotic_class)
