"""Module to hold constant variable to be used throughout the code base"""


TRUTH_NESS = ['True', 'TRUE', 'true', 't', 'T', 'Y', 'y', 'yes', 'Yes', 'YES', '1']  # NOQA

FALSE_NESS = ['False', 'FALSE', 'false', 'f', 'F', 'N', 'n', 'no', 'No', 'NO', '0']  # NOQA
BOOLEAN_CHOICES = tuple((value, 'True') for value in TRUTH_NESS) + tuple((value, 'False') for value in FALSE_NESS)  # NOQA
