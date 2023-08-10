from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class RequiredValuesTestCase(ModuleTestCase):
    "Test Sale Opportunity Management module"
    module = 'sale_opportunity_management'

    @with_transaction()
    def test_prospecto_en_prospect_trace_es_obligatorio(self):
        pool = Pool()
        ProspectTrace = pool.get('sale.prospect_trace')
        self.assertTrue(ProspectTrace.prospect.required)

    @with_transaction()
    def test_contact_method_en_prospect_es_obligatorio(self):
        pool = Pool()
        Prospect = pool.get('sale.prospect')
        self.assertTrue(Prospect.contact_methods.required)

    @with_transaction()
    def test_name_en_prospect_es_obligatorio(self):
        pool = Pool()
        Prospect = pool.get('sale.prospect')
        self.assertTrue(Prospect.name.required)

    @with_transaction()
    def test_value_en_contact_method_es_obligatorio(self):
        pool = Pool()
        ContactMethod = pool.get('prospect.contact_method')
        self.assertTrue(ContactMethod.value.required)

    @with_transaction()
    def test_contact_type_en_contact_method_es_obligatorio(self):
        pool = Pool()
        ContactMethod = pool.get('prospect.contact_method')
        self.assertTrue(ContactMethod.contact_type.required)

    @with_transaction()
    def test_prospect_en_contact_method_es_obligatorio(self):
        pool = Pool()
        ContactMethod = pool.get('prospect.contact_method')
        self.assertTrue(ContactMethod.prospect.required)


del ModuleTestCase
