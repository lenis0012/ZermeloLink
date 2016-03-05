# Fix django path
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.web.settings'
os.environ['ZLINK_MOODLE'] = 'web.moodle'

# Import django
import django
from moodle.models import Subject, Cohort

django.setup()

# Load subjects
subjects = {}
for subject in Subject.objects.all():
    subjects[subject.name] = subject


# Get subject by name
def get_subject(name):
    if name in subjects:
        return subjects[name]
    else:
        return None


def get_subjects():
    return subjects