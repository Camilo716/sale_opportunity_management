from trytond.model import ModelSQL, ModelView, fields 
from datetime import date

class Call(ModelSQL, ModelView):
    'Llamada'
    
    __name__ = 'sale.call'

    date = fields.Date('Fecha', )

    @classmethod
    def default_date(cls):
        return date.today()