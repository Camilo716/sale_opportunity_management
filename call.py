from trytond.model import ModelSQL, ModelView, fields 
from datetime import date
from Util.interest import Interest

class Call(ModelSQL, ModelView):
    'Llamada'
    
    __name__ = 'sale.call'

    date = fields.Date('Date')
    description = fields.Char('Description')

    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect track')

    interest = fields.Selection(Interest.get_interest_levels(), 'Interest')

    @classmethod
    def default_date(cls):
        return date.today()