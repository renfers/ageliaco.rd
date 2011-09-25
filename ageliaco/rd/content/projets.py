# -*- coding: UTF-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity

#from cycle import Projet

from ageliaco.rd import _

# for debug purpose => log(...)
from Products.CMFPlone.utils import log

from projet import IProjet
from cycle import ICycle

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
        
        
class View(grok.View):
    grok.context(IProjets)
    grok.require('zope2.View')
    
    def projets(self, wf_state='all'):
        """Return a catalog search result of projects to show
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        log( "context's physical path : " + '/'.join(context.getPhysicalPath()))
        log( "all projects")
        if wf_state == 'all':
            log( "all projets")
            log('/'.join(context.getPhysicalPath()))
            return catalog(object_provides= IProjet.__identifier__,
                           path={'query': '/'.join(context.getPhysicalPath()), 'depth': 1},
                           sort_on="start", sort_order="reverse")        
        return catalog(object_provides=[IProjet.__identifier__],
                       review_state=wf_state,
                       path={'query': '/'.join(context.getPhysicalPath()), 'depth': 1},
                       sort_on='sortable_title')

    def cycles(self, object, wf_state='all'):
        """Return a catalog search result of issues to show
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        log( 'cycle : ' + object.getPath())
        log( wf_state + " state chosen")
        if wf_state == 'all':
            log( "all cycles")
            return catalog(object_provides= ICycle.__identifier__,
                           path={'query': object.getPath(), 'depth': 1},
                           sort_on="modified", sort_order="reverse")        
        return catalog(object_provides=[ICycle.__identifier__],
                       review_state=wf_state,
                       path={'query': object.getPath(), 'depth': 1},
                       sort_on='sortable_title')
    
