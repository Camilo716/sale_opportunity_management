# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields


class City(ModelSQL, ModelView):
    'Ciudad'
    __name__ = 'sale.city'

    name = fields.Char('City')
    code = fields.Char('Code')
    parent = fields.Many2One('sale.department', 'Departamento')
