"""The transition the different operation states that a facility can be in."""


allowed_transitions = [
    {
        'current_state': 'PENDING_OPENING',
        'next_state': 'OPERATIONAL'
    },

    {
        'current_state': 'OPERATIONAL',
        'next_state': 'NON_OPERATIONAL'
    },
    {
        'current_state': 'NON_OPERATIONAL',
        'next_state': 'CLOSED'
    }
]


def can_transition(current_state, next_state):
    transition_dict = {
        'current_state': current_state,
        'next_state': next_state
    }
    return True if transition_dict in allowed_transitions else False
