# -*- coding: UTF-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity

#from cycle import Cycle

from ageliaco.rd import _


from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName

#from cycle import ICycle,Cycle
#from ageliaco.rd.attribution import IAttribution

import datetime

    
class ICycles(form.Schema):
    """
    Cycles de Projet RD
    """
# class addcycle(dexterity.AddForm):
#     grok.name('Cycle')
#     def update(self):
#         z3c.form.Form.update(self)
#         widget = form.widgets["contributor"] # Get one wiget
#         
#         for w in widget.items(): print w # Dump all widgets
# 

# class AddCycleForm(grok.AddForm):
#     grok.context(ICycles)
#     grok.name('Cycle')
#     #form_fields = grok.AutoFields(Cycles)
#     label = u"Création de cycles annuels d'administration"
#     grok.require('zope2.View')
#     
#     @grok.action(u"Ajout d'un cycle")
#     def add(self, **data):
#         from cycle import ICycle,Cycle
#         cycle = Cycle()
#         nb_cycles = len(self.context)
#         projet = self.context.ac_parent
#         cycle.year = str(datetime.datetime.today().year)
#         cycle.id = cycle.year
#         if nb_cycle == 0:
#             cycle.title = u"Initial"
#             cycle.contributors = projet.contributors
#         #else :
#         self.context[cycle.id] = cycle
#         return self.redirect(self.url(self.context[cycle.id]))