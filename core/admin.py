from django.contrib import admin
from .models import Profile, Listing


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'name', 'org', 'contact')
    list_filter = ('role',)
    search_fields = ('name', 'org', 'contact')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'kind', 'title', 'owner', 'status', 'created_at')
    list_filter = ('kind', 'status')
    search_fields = ('title', 'org', 'desc')
    list_editable = ('status',)