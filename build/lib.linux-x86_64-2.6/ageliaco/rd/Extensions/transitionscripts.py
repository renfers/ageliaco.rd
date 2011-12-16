# -*- coding: UTF-8 -*-

def schoolDirSend(self, state_change):
    """ sends an email to the school's director """
    print "schoolDirSend called !!!"
    #pass
    
def schoolDirApprove(self, state_change):
    """ school's director sends an email to the contributor to inform him """
    print "schoolDirApprove called !!!"
    #pass
    
def DIPDirSend(self, state_change):
    """ sends an email to the DIP's responsible for RD (Andenmatten) """
    print "DIPDirSend called !!!"
    #pass
    
    
def acceptAttribution(self, state_change):
    """ tests if all attribution objects in this projet are published
    If it's the case : it sends an email to contributors and supervisors """
    print "acceptAttribution called !!!"
    #pass
    
    
def rejectAttribution(self, state_change):
    """ schoolDir reject attribution 
    it sends an email to the contributor and RD """
    print "rejectAttribution called !!!"
    #pass
    
def reviseAttribution(self, state_change):
    """ schoolDir ask for a revision of the attribution 
    it sends an email to the contributor and RD """
    print "reviseAttribution called !!!"
    #pass
    
def testAllAttributions(self, state_change):
    """ tests if all attribution objects in this projet are accepted (peut être un mix 
    entre accepted et renounced)
    If it's the case : it sends an email to contributors, schools and supervisors 
    et change l'état du projet à "on" (en cours)"""
    print "testAllAttributions called !!!"
    #pass
    
def bilanReject(self, state_change):
    """ sends an email to contributors to ask for a complement on the bilan """
    print "bilanReject called !!!"
    #pass
    
    
def bilanFeedback(self, state_change):
    """ sends an email to contributors to give a feedback on the bilan """
    print "bilanFeedback called !!!"
    #pass
    
def notesFeedback(self, state_change):
    """ sends an email to contributors to give a feedback on meeting notes """
    print "notesFeedback called !!!"
    #pass
