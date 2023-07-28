# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields 

class Prospect(ModelSQL, ModelView):
    'Prospecto'
    
    __name__ = 'sale.prospect'

    name = fields.Char('Name')
    tel = fields.Integer('Tel')