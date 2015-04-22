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


allowed_moh_upgrades = [
    {
        "lower": "DISPENSARY",
        "upper": "HEALTH_CENTER"
    },
    {
        "lower": "HEALTH_CENTER",
        "upper": "SUB_DISTRICT_HOSPITAL"
    },
    {
        "lower": "SUB_DISTRICT_HOSPITAL",
        "upper": "DISRRICT_HOSPITAL"
    },
    {
        "lower": "DISRRICT_HOSPITAL",
        "upper": "PROVINCIAL_HOSPITAL"
    },
    {
        "lower": "PROVINCIAL_HOSPITAL",
        "upper": "NATIONAL_REFERRAL_HOSPITAL"
    }

]

allowed_fbo_upgrades = [
    {
        "lower": "DISPENSARY",
        "upper": "HEALTH_CENTER"
    },
    {
        "lower": "HEALTH_CENTER",
        "upper": "LOWEST_LEVEL_HOSPITAL"
    },
    {
        "lower": "LOWEST_LEVEL_HOSPITAL",
        "upper": "HIGHER_LEVEL_HOSPITAL"
    }

]

allowed_private_upgrades = [
    {
        "lower": "MEDICAL_CENTER",
        "upper": "MATERNITY_HOME"
    },
    {
        "lower": "MEDICAL_CENTER",
        "upper": "NURSING_HOME"
    },
    {
        "lower": "CLINIC",
        "upper": "MATERNITY_HOME"
    },
    {
        "lower": "CLINIC",
        "upper": "NURSING_HOME"
    },
    {
        "lower": "MATERNITY_HOME",
        "upper": "LOWEST_LEVEL_HOSPITAL"
    },
    {
        "lower": "NURSING_HOME",
        "upper": "HIGHER_LEVEL_HOSPITAL"
    },
    {
        "lower": "LOWEST_LEVEL_HOSPITAL",
        "upper": "HIGHER_LEVEL_HOSPITAL"
    }

]


def can_transition(current_state, next_state):
    transition_dict = {
        'current_state': current_state,
        'next_state': next_state
    }
    return True if transition_dict in allowed_transitions else False


def can_upgrade_in_moh(current_level, next_level):
    transition_dict = {
        'lower': current_level,
        'upper': next_level
    }
    return True if transition_dict in allowed_moh_upgrades else False


def can_upgrade_in_fbo(current_level, next_level):
    transition_dict = {
        'lower': current_level,
        'upper': next_level
    }
    return True if transition_dict in allowed_fbo_upgrades else False


def can_upgrade_in_private_sector(current_level, next_level):
    transition_dict = {
        'lower': current_level,
        'upper': next_level
    }
    return True if transition_dict in allowed_private_upgrades else False
