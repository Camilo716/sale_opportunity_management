from trytond.model import ModelSQL, ModelView, fields
from datetime import date


from .selections.interest import Interest
from .selections.call_types import CallTypes
from .selections.call_results import CallResults


class Call(ModelSQL, ModelView):
    'Llamada'

    __name__ = 'sale.call'

    date = fields.Date('Date')
    description = fields.Char('Description')

    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect trace')

    interest = fields.Selection(Interest.get_interest_levels(), 'Interest')
    call_type = fields.Selection(CallTypes.get_call_types(), 'Call type')
    call_result = fields.Selection(
        CallResults.get_call_results(), 'Call result', required=False)

    @classmethod
    def default_date(cls):
        return date.today()

    @fields.depends('interest')
    def on_change_interest(self):
        if self.interest:
            if self.interest == '0':
                self.call_result = 'missed_call'
            else:
                self.call_result = 'answered_call'
