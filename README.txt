Introduction
============

This product is intended for a service management in Geneva School Departement (DIP).
This service is "Ressources & Développement" and it brings a support for educational projects
in the upper secondary schools (colleges).

This product is dependant on **ageliaco.p10userdata**, because it does set the basic properties
in user data conforming to our ldap settings.


Installation
============
  * Go to admin > Site Setup > Add-ons
  * Activate plone.app.ldap
  * Activate ageliaco.p10userdata
  * Go to ZMI > acl_users > ldap-plugin > acl_users
    ** reset LDAP Server
    ** reset "Configure" to fit your needs (filter and groups)
  * Activate ageliaco.rd

There is a bug concerning plone.app.ldap => when the ldap server is set 
it doesn't set properly the port number, and the ldap filter is not set either.

This product may contain traces of nuts.


Authors
=======
  "AGELIACO", Serge Renfer mailto:serge.renfer@gmail dot com


