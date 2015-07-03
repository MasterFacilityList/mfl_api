from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


USER_MAPPING = {
    "model": "users.MflUserGroups",
    "unique_fields": ["user", "group"],
    "records": [
        {
            "mfluser": {
                "email": "superuser@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Superusers"
            }
        },
        {
            "mfluser": {
                "email": "national_admin@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "National Administratiors"
            }
        },
        {
            "mfluser": {
                "email": "nairobi_admin@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "County Administratiors"
            }
        },
        {
            "mfluser": {
                "email": "publisher@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Publishers"
            }
        },
        {
            "mfluser": {
                "email": "public@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Public Users"
            }
        },
        {
            "mfluser": {
                "email": "mombasa@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "kilifi@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "nairobi@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "narok@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "tanariver@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "starehe@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Sub County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "mathare@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Sub County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "kamukunji@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Sub County Health Records Information Officer"
            }
        },
        {
            "mfluser": {
                "email": "kmpdb@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Regulators (makers)"
            }
        },
        {
            "mfluser": {
                "email": "coc@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Regulators (makers)"
            }
        },
        {
            "mfluser": {
                "email": "ncck@mfltest.slade360.co.ke"
            },
            "group": {
                "name": "Regulators (makers)"
            }
        }
    ]
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        national = Group.objects.get(name="Superusers")

        for perm in Permission.objects.all():
            national.permissions.add(perm.id)
