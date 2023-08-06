# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.fields.osmap_advanced import OSMapAdvancedField
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IOSMapAdvancedBehaviorSchema(model.Schema):
    """ OSmap Advanced Behavior Schema
    """

    advanced_geolocation = OSMapAdvancedField(
        title=_('Geolocation'),
        description=_('Enter an address or set the location mark on the map'),
        required=False,
    )


@implementer(IOSMapAdvancedBehaviorSchema)
@adapter(IDexterityContent)
class OSMapAdvancedBehaviorFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def advanced_geolocation(self):
        return self.context.advanced_geolocation

    @advanced_geolocation.setter
    def advanced_geolocation(self, value):
        self.context.advanced_geolocation = value
