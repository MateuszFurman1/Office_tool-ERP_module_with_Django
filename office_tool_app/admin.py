from django.contrib import admin

from office_tool_app.models import User, Messages, Vacation, Address, Group, Delegation

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Address)
admin.site.register(Vacation)
admin.site.register(Messages)
admin.site.register(Delegation)