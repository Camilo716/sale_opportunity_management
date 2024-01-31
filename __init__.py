from trytond.pool import Pool

# Prospect Core
from .core.Prospect.models.prospect import Prospect
from .core.Prospect.models.contact_method import ContactMethod
from .core.Prospect.wizards.assign_operator \
    import AssignOperator, AssignOperatorStart
from .core.Prospect.wizards.reassign_prospect_by_prospect \
    import ReasignProspectByProspect, ReassignProspectByProspectStart
from .core.Prospect.wizards.reassign_prospect_by_operator \
    import ReassignProspectByOperator, ReassignProspectByOperatorStart

# Prospect Trace Core
from .core.ProspectTrace.wizards.make_call \
    import MakeCall, MakeCallAsk, MakeCallAskTask, MakeCallStart
from .core.ProspectTrace.wizards.schedule_call \
    import ScheduleCall, ScheduleCallStart
from .core.ProspectTrace.models.prospect_trace \
    import ProspectTrace

# Call Core
from .core.Call.models.call import Call
from .core.Call.models.pending_call import PendingCall
from .core.Call.models.pending_task import PendingTask

# Role core
from .core.Role.models.user import User

from .locations import city
from .locations import department

__all__ = ['register']


def register():
    Pool.register(
        User,
        PendingCall,
        Call,
        PendingTask,
        department.Department,
        city.City,
        ContactMethod,
        Prospect,
        ProspectTrace,
        AssignOperatorStart,
        ScheduleCallStart,
        MakeCallStart,
        MakeCallAsk,
        MakeCallAskTask,
        ReassignProspectByOperatorStart,
        ReassignProspectByProspectStart,
        module='sale_opportunity_management', type_='model')
    Pool.register(
        ScheduleCall,
        AssignOperator,
        MakeCall,
        ReassignProspectByOperator,
        ReasignProspectByProspect,
        module='sale_opportunity_management', type_='wizard')
    Pool.register(
        module='sale_opportunity_management', type_='report')
