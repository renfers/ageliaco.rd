# -*- coding: UTF-8 -*-
from five import grok
from zope import schema

from plone.directives import form, dexterity
from z3c.form import field, button

#from cycle import Projet

from ageliaco.rd import _

# for debug purpose => log(...)
from Products.CMFPlone.utils import log

from projet import IProjet
from cycle import ICycle
#from auteur import IAuteur

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from zope.interface import invariant, Invalid

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName

from plone.app.textfield import RichText

#from cycle import IProjet,Projet
#from ageliaco.rd.attribution import IAttribution
from collective.gtags.field import Tags

from Products.CMFCore.interfaces import IFolderish

import datetime

    
class IProjets(form.Schema):
    """
    Projets de Projet RD
    """
    presentation = RichText(
            title=_(u"Projets R&D"),
            required=True,
        )    

class IBaseAuteur(form.Schema):
    """
    Info de base pour generer plus tard les Auteurs de projet
    """


    firstname = schema.TextLine(
            title=_(u"Prénom"),
            description=_(u"Prénom"),
            required=True,
        )

    lastname = schema.TextLine(
            title=_(u"Nom"),
            description=_(u"Nom de famille"),
            required=True,
        )

    school = schema.Choice(
            title=_(u"Ecole"),
            description=_(u"Etablissement scolaire de référence"),
            vocabulary=u"ageliaco.rd.schools",
            required=False,
        )

    address = schema.Text(
            title=_(u"Adresse"),
            description=_(u"Adresse postale"),
            required=False,
        )
        
    email = schema.TextLine(
            title=_(u"Email"),
            description=_(u"Adresse courrielle"),
            required=True,
        )

class INewProjet(form.Schema):
    """
    to gather fields from both parents
    """
            

    #form.widget(contributor=AutocompleteMultiFieldWidget)
    contributor = schema.List(
            title=_(u"Contributeurs"),
            value_type=schema.Object(title=u"Auteur",
                                     schema=IBaseAuteur),   
            required=False,
        )

    duration = schema.Int(
            title=_(u"Durée"),
            description=_(u"Durée (en années) du projet, prévue ou effective"),
            required=True,
        )
    
    presentation = RichText(
            title=_(u"Présentation"),
            description=_(u"Présentation synthétique du projet (présentation publiée)"),
            required=True,
        )    
                
    problematique = RichText(
            title=_(u"Problématique"),
            description=_(u"Problématique et contexte du projet pour l'année à venir"),
            required=True,
        )    
        
    objectifs = RichText(
            title=_(u"Objectifs"),
            description=_(u"Objectifs du projet pour l'année"),
            required=True,
        )    

    resultats = RichText(
            title=_(u"Résultats"),
            description=_(u"Retombées (profs et/ou élèves) du projet pour l'année"),
            required=True,
        )    

    moyens = RichText(
            title=_(u"Moyens"),
            description=_(u"Moyens nécessaires pour l'année"),
            required=True,
        )    

    subject = Tags(
            title=_(u"Domaines")
            )

    def applyChanges(self, data):
        """
        Reflect confirmed status to Archetypes schema.
    
        @param data: Dictionary of cleaned form data, keyed by field
        """
        print "Apply Changes : ", data["contributor"]


        
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
    


class NewProjetForm(form.Form):
    grok.context(IFolderish)
    grok.name('newprojet')
    grok.require('cmf.AddPortalContent')
    ignoreContext = True

    fields = field.Fields(INewProjet)

    @button.buttonAndHandler(u'Submit')
    def handleApply(self, action):
        data, errors = self.extractData()
