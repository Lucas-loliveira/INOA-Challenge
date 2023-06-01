from django.contrib import admin

from .models import Stock


class StockAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    search_fields = ["stock"]


admin.site.register(Stock, StockAdmin)
