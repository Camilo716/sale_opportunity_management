# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields


class PendingCall(ModelSQL, ModelView):
    'Llamada pendiente a un prospecto'
    __name__ = "sale.pending_call"

    date = fields.Date('Date', required=True)
    prospect_trace = fields.Many2One('sale.prospect_trace', 'Prospect trace')
