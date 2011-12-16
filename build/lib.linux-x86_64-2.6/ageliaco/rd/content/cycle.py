# -*- coding: UTF-8 -*-
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.fieldproperty import FieldProperty
from cycles import ICycles
from attribution import IAttribution, Attribution, schools

from ageliaco.rd import _

import datetime

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid

from Acquisition import aq_inner, aq_parent
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot

class TwiceSameSupevisor(Invalid):
    __doc__ = _(u"Choisir un autre superviseur secondaire ou primaire!")


class GroupMembers(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    
    grok.implements(IContextSourceBinder)
    
    def __init__(self, group_name):
        self.group_name = group_name
    
    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        group = acl_users.getGroupById(self.group_name)
        terms = []
        terms.append(SimpleVocabulary.createTerm('', str(''), ''))
        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))
            
        return SimpleVocabulary(terms)    


    
"""
<model xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema>
    <field name="num_projet" type="zope.schema.TextLine">
      <description />
      <title>Numero Projet</title>
    </field>
    <field name="supervisor" type="zope.schema.TextLine">
      <description>Personne de RD qui supervise ce projet</description>
      <required>False</required>
      <title>Superviseur</title>
    </field>
    <field name="superviseur2" type="zope.schema.TextLine">
      <description>Personne qui epaule le superviseur</description>
      <required>False</required>
      <title>Superviseur2</title>
    </field>
    <field name="debut" type="zope.schema.TextLine">
      <description>L'annee a laquelle le projet a commence ou devrait commencer</description>
      <title>Annee de debut</title>
    </field>
    <field name="duration" type="zope.schema.Int">
      <description>Nombre d'annees que le projet devrait durer</description>
      <title>Duree</title>
    </field>
    <field name="presentation" type="plone.app.textfield.RichText">
      <default>Presentation</default>
      <description>Presentation des enjeux et objectifs du projet</description>
      <missing_value />
      <required>False</required>
      <title>Presentation</title>
    </field>
  </schema>
</model>
"""
# class IContributor(form.Schema):
#     """
#     Contributeur par cycle de projet RD
#     """
#     id = schema.TextLine(
#             title=_(u"Id"),
#             description=_(u"L'identifiant (login)"),
#             required=True,
#         )
#     fullname = schema.TextLine(
#             title=_(u"Nom"),
#             description=_(u"Le nom complet"),
#             required=False,
#         )
#     mail = schema.TextLine(
#             title=_(u"Mail"),
#             description=_(u"L'adresse courrielle"),
#             required=False,
#         )
#     school = schema.TextLine(
#             title=_(u"Etablissement"),
#             description=_(u"L'établissement"),
#             required=False,
#         )
        

class ICycle(form.Schema):
    """
    Cycle de projet RD
    """
    
    # -*- Your Zope schema definitions here ... -*-
    id = schema.TextLine(
            title=_(u"Année"),
            description=_(u"L'année d'administration du projet"),
            required=True,
        )
        
    form.widget(contributor=AutocompleteMultiFieldWidget)
    contributor = schema.List(
            title=_(u"Contributeurs"),
            value_type=schema.Choice(vocabulary=u"plone.principalsource.Users",),    
            required=False,
        )
            
    dexterity.write_permission(supervisor='cmf.ReviewPortalContent')
    supervisor = schema.Choice(
            title=_(u"Superviseur"),
            description=_(u"Personne de R&D qui supervise ce projet"),
            source=GroupMembers('superviseur'),
            required=False,
        )
    dexterity.write_permission(supervisor2='cmf.ReviewPortalContent')
    supervisor2 = schema.Choice(
            title=_(u"Superviseur secondaire"),
            description=_(u"Personne qui épaule le premier superviseur"),
            source=GroupMembers('superviseur'),
            required=False,
        )

    @invariant
    def validateSupervisorSupervisor2(data):
        if data.supervisor is not None and data.supervisor2 is not None:
            if data.supervisor == data.supervisor2:
                raise TwiceSameSupevisor(_(u"Le superviseur secondaire doit être différent du premier!"))
    

    presentation = RichText(
            title=_(u"Présentation"),
            description=_(u"Enjeux et objectifs du projet pour l'année"),
            required=True,
        )    

    def applyChanges(self, data):
        """
        Reflect confirmed status to Archetypes schema.
    
        @param data: Dictionary of cleaned form data, keyed by field
        """
        
    
        # This is the context given to the form when the form object was constructed
        cycle = self.context
    
        assert ICycle.providedBy(cycle) # safety check
    
        # Call archetypes field mutator to store the value on the patient object
        cycle.setContributors(tuple(data["contributor"]))
        print "Apply Changes : ", data["contributor"]



class Cycle(object):
    """Cycle
    """
    
    grok.implements(ICycle)
    def __init__(self):
        self.contributor = self.aq_inner.aq_parent.contributor
        print "creation cycle : ",self.aq_inner.aq_parent.contributor
        


@form.default_value(field=ICycle['contributor'])
def contributorDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    context = data.context
    terms = []
    contributors = []
    folder = data.context
    print folder.keys()
    last_year = str(datetime.datetime.today().year - 1)

    portal_url = getToolByName(folder, 'portal_url')
    acl_users = getToolByName(context, 'acl_users')
    
    portal = portal_url.getPortalObject() 
    parent = folder.aq_inner
    grandparent = parent.aq_parent
    print grandparent.contributors

    try: #looking for preceding cycle
        last_cycle = folder[last_year]
        contributors = last_cycle.contributors
    except : #no cycle before, let's find the project's contributors
        try:
            
            contributors = grandparent.contributors
        except:
            print "bad, bad, ...", folder, parent, parent.aq_parent
    #print dir(data)  
    #print dir(context)
    context.setContributors(contributors)
    context.contributors = contributors
    print "context.contributors = ", context.contributors
    #data.set(context.contributors)
    #data["contributor"] = list(context.contributors)
    print data.field.setTaggedValue.__doc__
    
    if len(context.contributors):
        data.field.setTaggedValue(context.contributors[0],context.contributors[0])
    return list(context.contributors)
    
@grok.subscribe(ICycle, IObjectAddedEvent)
@grok.subscribe(ICycle, IObjectModifiedEvent)
def setDublin(cycle, event):
    print dir(event)
    print cycle.title

    #portal = getUtility(ISiteRoot)
    #acl_users = getToolByName(portal, 'acl_users')
    acl_users = getToolByName(cycle, 'acl_users')
    
    #cycle.setContributors(cycle.contributors)
    #cycle.setId = str(datetime.datetime.today().year)
    #cycle.contributors += cycle.initalcontributors
    print "cycle.contributor : ", cycle.contributor
    cycle.setContributors(cycle.contributor)
    
    # attribution creation - one per contributor
    for author in cycle.contributor:
    
        id = 'attribution_%s'%author
        try:
            attribution = cycle[id]
        except: 
            user = acl_users.getUserById(author)
            if user:
                fullname = user.getProperty(u'fullname') or auteur
                school = user.getProperty(u'title') or u'N/A'
                print school
                if school in schools.keys():
                    sector = schools[school][1]
                else:
                    sector = u'non disponible'
                
                cycle.invokeFactory("ageliaco.rd.attribution", 
                                id=id, 
                                title='Attribution %s'%fullname, 
                                contributor=author, 
                                school=school,
                                sector=sector,
                                hour = 0.0,
                                hourRD = 0.0,
                                hourFinal = 0.0
                                )
                attribution = cycle[id]
                attribution.indexObject()
                #Attribution(attribution).set(author,school)
            else:
                print "User %s not found! Attribution not created "%author
    return cycle.contributors


@form.default_value(field=ICycle['id'])
def idDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return str(datetime.datetime.today().year)

    
# @grok.subscribe(ICycle, IObjectModifiedEvent)
# def resetDublin(cycle,event):
#     #cycle.setContributors(cycle.contributors)
#     print cycle.contributors
#     for contributor in cycle.newcontributors:
#         print contributor
#         if contributor not in cycle.contributors:
#             print cycle.contributors, tuple([contributor])
#             cycle.contributors += tuple([contributor])
#     return cycle.contributors
# def createGroup(projet, event):
#     acl_users = getToolByName(projet, 'acl_users')
#     mail_host = getToolByName(projet, 'MailHost')
#     portal_url = getToolByName(projet, 'portal_url')
#     
#     portal = portal_url.getPortalObject()
#     sender = portal.getProperty('email_from_address')
# 
#     return

class AddForm(grok.AddForm):
    grok.context(ICycles)
    grok.name('Cycle')
    #form_fields = grok.AutoFields(Cycles)
    label = u"Création de cycles annuels d'administration"
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