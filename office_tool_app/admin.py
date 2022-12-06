from django.contrib import admin

from office_tool_app.models import User, Messages, Vacation, Group, Delegation, MedicalLeave, AddressCore, AddressHome

admin.site.register(User)
admin.site.register(Group)
admin.site.register(AddressCore)
admin.site.register(AddressHome)
admin.site.register(Vacation)
admin.site.register(Messages)
admin.site.register(Delegation)
admin.site.register(MedicalLeave)