# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.interfaces import IOSMapAdvancedField
from contenttypes.basic.interfaces import IOSMapAdvancedWidget
from datetime import datetime
from plone import api
from plone.api.exc import InvalidParameterError
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(IOSMapAdvancedWidget)
class OSMapAdvancedWidget(TextWidget):

    default_point_value = '{"type": "point","coordinates": [[0,0]]}'

    name = 'osmap-widget'
    label = _('OSMap Widget')
    timestamp = datetime.now().strftime('%s')

    @property
    def portal_url(self):
        return api.portal.get().absolute_url()

    @property
    def default_value(self):
        return self.field.default or self.default_point_value

    def default_value_map(self):
        try:
            default_coords = api.portal.get_registry_record(name='coordinates.map_center')
            default_value = """{
                "type": "point",
                "coordinates": [[""" + default_coords.replace('|', ',') + """]]
            }"""
            return default_value
        except InvalidParameterError:
            return self.default_point_value


@implementer(IFieldWidget)
@adapter(IOSMapAdvancedField, IFormLayer)
def OSMapAdvancedFieldWidget(field, request):
    return FieldWidget(field, OSMapAdvancedWidget(request))


@adapter(IOSMapAdvancedField, IOSMapAdvancedWidget)
class OSMapAdvancedConverter(BaseDataConverter):
    """ Convert between the context and the widget
    """

    def toWidgetValue(self, value):
        return self.parse_coordinates(value)

    def toFieldValue(self, value):
        return self.parse_coordinates(value)

    def parse_coordinates(self, value):
        if not value:
            return ''

        try:
            json.loads(value)
        except json.decoder.JSONDecodeError:
            return ''

        return value
