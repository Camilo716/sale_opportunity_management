from trytond.model import ModelSQL, ModelView, fields
from datetime import date


from .selections.interest import Interest
from .selections.call_types import CallTypes
from .selections.call_results import CallResults


class Call(ModelSQL, ModelView):
    'Llamada'

    __name__ = 'sale.call'

    _states = {'readonly': True}

    date = fields.Date('Date', states=_states)
    description = fields.Text('Description', strip=True)

    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect trace')

    interest = fields.Selection(
        Interest.get_interest_levels(), 'Interest', required=True)
    call_type = fields.Selection(
        CallTypes.get_call_types(), 'Call type', states=_states)
    call_result = fields.Selection(
        CallResults.get_call_results(),
        'Call result', states=_states)

    @classmethod
    def default_date(cls):
        return date.today()
