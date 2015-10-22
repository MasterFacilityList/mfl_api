import random

from django.core.management import BaseCommand

from django.contrib.auth import get_user_model

from facilities.models import JobTitle
from common.models import County, ContactType
from admin_offices.models import AdminOffice, AdminOfficeContact

system_user = get_user_model().objects.get(email='system@ehealth.or.ke')

names = [
    {
        "first_name": "Brian",
        "last_name": "Nguyo",
        "contact": "0756353637"
    },
    {
        "first_name": "James",
        "last_name": "Limpopo",
        "contact": "0856464675"
    },
    {
        "first_name": "Dominic",
        "last_name": "Musee",
        "contact": "0876453637"
    },
    {
        "first_name": "Wilberforce",
        "last_name": "Otieno",
        "contact": "0756371848"
    },
    {
        "first_name": "Damaris",
        "last_name": "Sikaine",
        "contact": "0713547788"
    }
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        index = random.randint(0, 10)
        contact_type = ContactType.objects.get(name='MOBILE')
        for name in names:
            admin_office = AdminOffice.objects.create(
                created_by=system_user,
                updated_by=system_user,
                county=County.objects.all()[index],
                job_title=JobTitle.objects.all()[index],
                first_name=name.get('first_name'),
                last_name=name.get('last_name'))
            try:
                AdminOfficeContact.objects.create(
                    admin_office=admin_office,
                    created_by=system_user,
                    updated_by=system_user,
                    contact_type=contact_type,
                    contact=name.get('contact'))
            except:
                # the contact and contact type already exists
                pass
