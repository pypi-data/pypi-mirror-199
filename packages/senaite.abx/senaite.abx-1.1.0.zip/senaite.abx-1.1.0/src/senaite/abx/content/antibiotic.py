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

from AccessControl import ClassSecurityInfo
from bika.lims import api
from plone.dexterity.content import Item
from Products.CMFCore import permissions
from senaite.abx.interfaces import IAntibiotic
from senaite.core.catalog import SETUP_CATALOG
from zope.interface import implementer


@implementer(IAntibiotic)
class Antibiotic(Item):
    """Antibiotic content
    """
    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()
    exclude_from_nav = True

    @security.protected(permissions.View)
    def getAbbreviation(self):
        """Returns the abbreviation of this antibiotic
        """
        fields = api.get_fields(self)
        return fields.get("abbreviation").get(self)

    @security.protected(permissions.ModifyPortalContent)
    def setAbbreviation(self, value):
        """Sets the abbreviation for this antibiotic
        """
        fields = api.get_fields(self)
        fields.get("abbreviation").set(self, value)

    @security.protected(permissions.View)
    def getAntibioticClass(self):
        """Returns the Antibiotic class this antibiotic is assigned to
        """
        fields = api.get_fields(self)
        return fields.get("antibiotic_class").get(self)

    @security.protected(permissions.View)
    def getRawAntibioticClass(self):
        """Returns the UID of the antibiotic class
        """
        fields = api.get_fields(self)
        return fields.get("antibiotic_class").get_raw(self)

    @security.protected(permissions.ModifyPortalContent)
    def setAntibioticClass(self, value):
        """Sets the antibiotic class for this antibiotic
        """
        fields = api.get_fields(self)
        fields.get("antibiotic_class").set(self, value)
