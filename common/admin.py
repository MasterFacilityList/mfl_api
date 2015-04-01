from django.contrib import admin

from .models import (
    Contact, Province, County, District,
    Division, Location, SubLocation, Constituency)

admin.site.register(Contact)
admin.site.register(Province)
admin.site.register(County)
admin.site.register(District)
admin.site.register(Division)
admin.site.register(Location)
admin.site.register(SubLocation)
admin.site.register(Constituency)
