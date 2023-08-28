from trytond.pool import Pool
from . import prospect
from . import prospect_trace
from . import call
from . import pending_call
from .locations import city
from .locations import department

__all__ = ['register']


def register():
    Pool.register(
        pending_call.PendingCall,
        call.Call,
        department.Department,
        city.City,
        prospect.ContactMethod,
        prospect.Prospect,
        prospect_trace.ProspectTrace,
        prospect.AssignOperatorStart,
        prospect_trace.ScheduleCallStart,
        prospect_trace.MakeCallStart,
        prospect_trace.MakeCallAsk,
        prospect.ReassignProspectByOperatorStart,
        prospect.ReassignProspectByProspectStart,
        module='sale_opportunity_management', type_='model')
    Pool.register(
        prospect_trace.ScheduleCall,
        prospect.AssignOperator,
        prospect_trace.MakeCall,
        prospect.ReassignProspectByOperator,
        prospect.ReasignProspectByProspect,
        module='sale_opportunity_management', type_='wizard')
    Pool.register(
        module='sale_opportunity_management', type_='report')
