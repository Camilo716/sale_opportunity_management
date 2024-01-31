# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView, fields
from trytond.pyson import Eval
from datetime import datetime
from ....core.ProspectTrace.wizards.make_call import MakeCall


class ScheduleCallStart(ModelView):
    'Inicio agendar llamada a seguimiento de prospecto'
    __name__ = 'sale.prospect_trace.schedule.start'

    currency_date = fields.DateTime('Currency Date', readonly=True)
    date_time = fields.DateTime('Date time', domain=[
        ('date_time', '>=', Eval('currency_date'))])

    @classmethod
    def default_currency_date(cls):
        date = datetime.now()

        return date


class ScheduleCall(Wizard):
    'Agendar llamada a seguimiento de prospecto'
    __name__ = 'sale.prospect_trace.schedule'

    start = StateView(
        'sale.prospect_trace.schedule.start',
        'sale_opportunity_management.schedule_start_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Schedule", 'schedule', 'tryton-ok', default=True)])

    schedule = StateTransition()

    def transition_schedule(self):
        MakeCall.create_schedule_call(self.start.date_time, self.record)
        return 'end'
