from django.contrib import admin

from application.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "serial",
        "code",
        "name",
        "qty",
        "is_touched",
    )
    list_filter = ("is_touched",)
    list_display_links = (
        "code",
        "name",
    )
    search_fields = (
        "code",
        "name",
    )
    ordering = ("serial",)
    list_per_page = 20
