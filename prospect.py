# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields 

class Prospect(ModelSQL, ModelView):
    'Prospecto'
    __name__ = 'sale.prospect'

    name = fields.Char('Name')
    city = fields.Char('City')

    contact_methods = fields.One2Many('prospect.contact_method', 'prospect', 'Contact methods') 


class ContactMethod(ModelSQL, ModelView):
    'Mecanismo de contacto'
    __name__ = 'prospect.contact_method'

    _type = [
        ('phone', 'Phone'),
        ('mobile', 'Mobile'),
        ('email', 'Email')
    ]
    contact_type = fields.Selection(_type, 'Contact type')

    value = fields.Char('Value')

    prospect = fields.Many2One('sale.prospect', 'Prospect')
    
