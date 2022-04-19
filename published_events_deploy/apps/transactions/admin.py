from django.contrib import admin
from published_events_deploy.apps.transactions.models import Transaction
from django.contrib.admin.decorators import display

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ["user_identification", "ticket_type", "ticket_amount","get_status"]

    @display(description="Status")
    def get_status(self, obj: Transaction) -> str:
        return obj.status

admin.site.register(Transaction, TransactionsAdmin)