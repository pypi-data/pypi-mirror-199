# -*- coding: utf-8 -*-
from contenttypes.basic.interfaces import IOSMapAdvancedField
from zope.interface import implementer
from zope.schema import TextLine


@implementer(IOSMapAdvancedField)
class OSMapAdvancedField(TextLine):
    """ OSMap Advanced Field
    """
