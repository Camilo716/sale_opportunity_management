from trytond.pool import Pool
from . import prospect
from . import prospect_trace
from . import call
from .locations import city
from .locations import department

__all__ = ['register']


def register():
    Pool.register(
        call.Call,
        department.Department,
        city.City,
        prospect.Prospect,
        prospect.ContactMethod,
        prospect_trace.ProspectTrace,

        module='sale_opportunity_management', type_='model')
    Pool.register(
        module='sale_opportunity_management', type_='wizard')
    Pool.register(
        module='sale_opportunity_management', type_='report')
