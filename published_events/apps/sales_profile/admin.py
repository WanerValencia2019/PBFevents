from django.contrib import admin

from published_events.apps.sales_profile.models import SaleProfile, Withdrawal


class SaleProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "amount_available", "amount_retired", "last_withdraw"]


admin.site.register(SaleProfile, SaleProfileAdmin)
admin.site.register(Withdrawal)
