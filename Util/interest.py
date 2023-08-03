class Interest():
    @staticmethod
    def get_interest_levels():
        interest_levels = [
            ('0', '0 - No contestó'),
            ('1', '1 - total desinterés'),
            ('2', '2 - Interés intermedio'),
            ('3', '3 - Interés alto, generar venta')
        ]

        return interest_levels