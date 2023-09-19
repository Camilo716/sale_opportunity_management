# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields


class PendingCall(ModelSQL, ModelView):
    'Llamada pendiente a un prospecto'
    __name__ = "sale.pending_call"

    date = fields.DateTime('Date', required=True)

    def get_rec_name(self, name):
        if self.date:
            return str(self.date)


class PendingTask(ModelSQL, ModelView):
    'Tarea pendiente a un seguimiento de prospecto'
    __name__ = "sale.pending_task"

    description = fields.Text('Description', required=True)
    done = fields.Boolean('Done')
    prospect_trace = fields.Many2One(
        'sale.prospect_trace', 'Prospect trace',
        required=True, readonly=True)

    @classmethod
    def default_done(cls):
        return False
