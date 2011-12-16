# -*- coding: UTF-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from ageliaco.rd import ICycle, IAttribution, ICycles

import datetime

class CycleForm(grok.AddForm):
    grok.context(ICycles)
    form_fields = grok.AutoFields(Cycle)
    label = u"Création d'un cycle annuel d'administration"
    grok.require('zope2.View')
    
    @grok.action(u"Ajout d'un cycle")
    def add(self, **data):
        cycle = Cycle()
        nb_cycles = len(self.context)
        projet = self.context.ac_parent
        cycle.year = str(datetime.datetime.today().year)
        cycle.id = cycle.year
        if nb_cycle == 0:
            cycle.title = u"Initial"
            cycle.contributors = projet.contributors
        #else :
        self.context[cycle.id] = cycle
        return self.redirect(self.url(self.context[cycle.id]))