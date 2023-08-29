from trytond.model import ModelSQL, ModelView, fields
from datetime import date


from .selections.interest import Interest
from .selections.call_types import CallTypes
from .selections.call_results import CallResults


class Call(ModelSQL, ModelView):
    'Llamada'
    __name__ = 'sale.call'
    _order_name = 'date'
    _states = {'readonly': True}

    date = fields.Date('Date', states=_states)
    description = fields.Text('Description', strip=True)

    prospect_trace = fields.Many2One(
        'sale.prospect_trace', 'Prospect trace', required=True, states=_states)

    interest = fields.Selection(
        Interest.get_interest_levels(), 'Interest', required=True)

    call_type = fields.Selection(
        CallTypes.get_call_types(), 'Call type', states=_states)
    call_result = fields.Selection(
        CallResults.get_call_results(),
        'Call result', states=_states)
    call_business_unit = fields.Selection(
        [('brigade', 'Brigade'),
         ('optics', 'Optics'),
         ('equipment', 'Equipment')],
        'Business unit', states=_states
    )
    call_assigned_operator = fields.Many2One(
        'res.user', "Assigned operator", states=_states)

    @classmethod
    def __setup__(cls):
        super(Call, cls).__setup__()

        cls._order = [
            ('date', 'DESC NULLS FIRST')
        ]

    @classmethod
    def default_date(cls):
        return date.today()
