class ProspectTraceStates():
    @staticmethod
    def get_prospect_trace_states():
        states = [
            ('unassigned', 'Unassigned'),
            ('open', 'Open'),
            ('with_pending_calls', 'With pending calls'),
            ('closed', 'Closed')
        ]
        return states
