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
from zope.interface import Interface, Attribute
from zope.component.factory import Factory
from zope.schema.fieldproperty import FieldProperty

from ageliaco.rd import _

import datetime

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from Products.CMFCore.utils import getToolByName

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid
from z3c.form.object import registerFactoryAdapter

from copy import deepcopy


class GroupMembers(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    
    grok.implements(IContextSourceBinder)
    
    def __init__(self, group_name):
        self.group_name = group_name
    
    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        #group = acl_users.getGroupById(self.group_name)
        try:
            parent = context.aq_inner.aq_parent
            group = parent.contributor
        except:
            print context.aq_inner, context.aq_inner.parent
            
        terms = []
        
    
        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    member_mail = user.getProperty('email') or ''
                    ecole = user.getProperty('ecole') or ''
                    if ecole:
                        member_name = member_name + ' (' + ecole + ')'
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))
            
        return SimpleVocabulary(terms)    
    
class ICouple(Interface):
    """
    Attribution horaire
    """
    id = schema.TextLine(
            title=u'ID',
            #readonly = True,
            required = True)
    contributor = schema.TextLine(
                        title=u"Contributeur",
                        required=False,
                        )
    school = schema.TextLine(
                        title=u"Ecole",
                        required=False,
                        )
    sector = schema.TextLine(
            title=u'Centre de concertation',
            #readonly = True,
            required = False)
            
    hour = schema.Float(title=u"Heure(s) totale demandée (R&D + école)", min=0.0,
                        required=False,
                        )
                        
class Couple(object):
    grok.implements(ICouple)
    contributor = FieldProperty(ICouple['contributor'])
    hour = FieldProperty(ICouple['hour'])
    def __init__(self):
        pass
    def set(self,id,contributor,school,hour,email=u''):
        self.id = id
        self.school = school
        self.contributor = contributor
        self.email = email
        if school in schools.keys():
            self.sector = schools[school][1]
        else:
            self.sector = u'non disponible'
        self.hour = hour
    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)   
    
        
registerFactoryAdapter(ICouple, Couple)
class IAttribution(form.Schema):
    """
    Attribution horaire
    """
    title = schema.TextLine(
            title=_(u"Titre"),
            description=_(u"Défini le type d'attribution"),
            required=True,
        )
    

    hoursAttribution = schema.List(
            title=u"Attribution horaire par contributeur",
            value_type = schema.Object(
            schema = ICouple,required=False),
            required=False
        )

# class Attribution(object):
#     grok.implements(IAttribution)
#     pass
    
@form.default_value(field=IAttribution['title'])
def titleDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    context = data.context
    folder = data.context
    
    try: #looking for preceding attribution
        last_attribution = None
        
        attrs = folder.listFolderContents(contentFilter={"portal_type" : "ageliaco.rd.attribution"})
        whichAttribution = len(attrs)
        if whichAttribution == 0:
            return u"Attribution demandée"
        elif whichAttribution == 1:
            return u"Attribution proposée par R&D"
        else :
            return u"Attribution définitive"
            
            
    except  KeyError: #no attribution before, let's find the project's contributors
        print "problemo : in searching for attribution before!"
    return u"Attribution"

@form.default_value(field=IAttribution['hoursAttribution'])
def hoursAttributionDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    context = data.context
    contributors = []
    folder = data.context
    aDic = []
    acl_users = getToolByName(context, 'acl_users')
    last_year = str(datetime.datetime.today().year - 1)

    parent = folder.aq_inner
    grandparent = parent.aq_parent
    print dir(grandparent)
    contributors = grandparent.contributor
    print grandparent.contributors
    
    
    try: #looking for preceding attribution
        last_attribution = None
        
        attrs = folder.listFolderContents(contentFilter={"portal_type" : "ageliaco.rd.attribution"})

        whichAttribution = len(attrs)
        if len(attrs):
            last_attribution = attrs[-1]
        else : print "no attribution before!"
            
    except  KeyError: #no attribution before, let's find the project's contributors
        print "problemo : in searching for attribution before!"
    print contributors  
    if last_attribution:
        print last_attribution.hoursAttribution, dir(last_attribution.hoursAttribution)
        aDic = deepcopy(last_attribution.hoursAttribution)
        print "deepcopy de ", aDic
        return aDic
    for auteur in contributors:
        user = acl_users.getUserById(auteur)
        if user:
            fullname = user.getProperty(u'fullname') or auteur
            ecole = user.getProperty(u'title') or u'N/A'
            print ecole
            email = user.getProperty(u'email') or u''
            aContributor = Couple()
            aContributor.set(id=unicode(auteur), 
                contributor=unicode(fullname), 
                school=unicode(ecole), 
                hour=0.0,
                email=email)
        aDic.append(aContributor)
    return aDic

schools = {u"ECGGR":[u"EC Bougeries",u"CEC"],
    u"CEBOU":[u"Nicolas-Bouvier",u"CEC"],
    u"CECHA":[u"André-Chavanne",u"CEC"],
    u"CEGOU":[u"Emilie-Gourd",u"CEC"],
    u"ECASE":[u"Madame-de-Stael",u"CEC"],
    u"ECSTI":[u"EC Aimée-Stitelmann",u"CEC"],
    u"CALV":[u"Calvin",u"COLLEGES"],
    u"CAND":[u"Candolle",u"COLLEGES"],
    u"CLAP":[u"Claparède",u"COLLEGES"],
    u"COPAD":[u"Alice-Rivaz",u"COLLEGES"],
    u"ROUS":[u"Rousseau",u"COLLEGES"],
    u"SAUS":[u"Saussure",u"COLLEGES"],
    u"SISM":[u"Sismondi",u"COLLEGES"],
    u"VOLT":[u"Voltaire",u"COLLEGES"],
    u"ECBGR":[u"ECG RHONE",u"ECG"],
    u"DUNAN":[u"Henry-Dunand",u"ECG"],
    u"MAILL":[u"Ella-Maillart",u"ECG"],
    u"ECGJP":[u"Jean-Piaget",u"ECG"],
    u"CFPC":[u"CFPC",u"ECOLES PROFESSIONNELLES"],
    u"CFPS":[u"CFPS",u"ECOLES PROFESSIONNELLES"],
    u"CFPT":[u"CFPT",u"ECOLES PROFESSIONNELLES"],
    u"CFPSH":[u"CFPSHR-EGEI",u"ECOLES PROFESSIONNELLES"],
    u"BOUV":[u"CFPCOM-Bouvier",u"ECOLES PROFESSIONNELLES"],
    u"CFPNE":[u"CFPNE",u"ECOLES PROFESSIONNELLES"],
    u"CFPAA":[u"CFPAA",u"ECOLES PROFESSIONNELLES"],
    u"SCAI":[u"SCAI",u"INSERTION"],
    u"COUDR":[u"CO Coudriers",u"CYCLES"]}
