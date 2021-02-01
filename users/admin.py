from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('username', 'email', 'display_name', )
  list_editable = ['display_name', ]
  search_fields = ['username', 'email', 'display_name', ]

admin.site.register(UserProfile, UserProfileAdmin)