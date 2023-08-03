from trytond.model import ModelSQL, ModelView, fields 
from datetime import date

class Call(ModelSQL, ModelView):
    'Llamada'
    
    __name__ = 'sale.call'

    date = fields.Date('Date')
    description = fields.Char('Description')

    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect track')

    interest_types = [
        ('0', '0 - No contestó'),
        ('1', '1 - total desinterés'),
        ('2', '2 - Interés intermedio'),
        ('3', '3 - Interés alto, generar venta')
    ]

    interest = fields.Selection(interest_types, 'Interest')


    @classmethod
    def default_date(cls):
        return date.today()