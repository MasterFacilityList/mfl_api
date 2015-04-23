"""The transition the different operation states that a facility can be in."""


ALLOWED_TRANSITIONS = [

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


ALLOWED_MOH_UPGRADES = [
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

ALLOWED_FBO_UPGRADES = [
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

ALLOWED_PRIVATE_UPGRADES = [
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


def reverse_dict(transition_dict):
    """
    This will allow for reversal of a record. More like a contra entry in
    accounting.
    """
    next_state = transition_dict.get("next_state")
    current_state = transition_dict.get("next_state")
    if not next_state and not current_state:
        return {
            "lower": transition_dict.get("upper"),
            "upper": transition_dict.get("lower")
        }

    return {
        "current_state": transition_dict.get("next_state"),
        "next_state": transition_dict.get("current_state")
    }


def transition_helper(transition_dict, transitions_class):
    if transition_dict in transitions_class:
        return True
    elif reverse_dict(transition_dict) in transitions_class:
        return True
    else:
        return False


def can_transition(current_state, next_state):
    transition_dict = {
        'current_state': current_state,
        'next_state': next_state
    }
    return transition_helper(transition_dict, ALLOWED_TRANSITIONS)


def can_upgrade_or_downgrade_in_moh(current_level, next_level):
    transition_dict = {
        'lower': current_level,
        'upper': next_level
    }
    return transition_helper(transition_dict, ALLOWED_MOH_UPGRADES)


def can_upgrade_or_downgrade_in_fbo(current_level, next_level):
    transition_dict = {
        'lower': current_level,
        'upper': next_level
    }
    return transition_helper(transition_dict, ALLOWED_FBO_UPGRADES)


def can_upgrade_or_downgrade_in_private_sector(current_level, next_level):
    transition_dict = {
        'lower': current_level,
        'upper': next_level
    }
    return transition_helper(transition_dict, ALLOWED_PRIVATE_UPGRADES)
