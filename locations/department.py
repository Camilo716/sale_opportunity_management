# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields


class Department(ModelSQL, ModelView):
    'Departamento'
    __name__ = 'sale.department'

    name = fields.Char('Department')
    code = fields.Char('Code')
