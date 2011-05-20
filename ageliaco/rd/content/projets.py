# -*- coding: UTF-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity

#from cycle import Projet

from ageliaco.rd import _


from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName

from plone.app.textfield import RichText

#from cycle import IProjet,Projet
#from ageliaco.rd.attribution import IAttribution

import datetime

    
class IProjets(form.Schema):
    """
    Projets de Projet RD
    """
    presentation = RichText(
            title=_(u"Projets R&D"),
            required=True,
        )    
