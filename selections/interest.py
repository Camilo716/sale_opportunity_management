class Interest():
    @staticmethod
    def get_interest_levels():
        interest_levels = [
            ('', None),
            ('0', '0 - Not answered'),
            ('1', '1 - Complete disinterest'),
            ('2', '2 - Middle interest'),
            ('3', '3 - High interest'),
            ('4', '4 - Closed sale')
        ]

        return interest_levels
