from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from charity_donations_app.models import Category, Institution, Donation

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'display_categories')
    search_fields = ('name', 'type')
    list_filter = ('type',)

    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())
    display_categories.short_description = "Categories"

admin.site.register(Category)
admin.site.register(Donation)