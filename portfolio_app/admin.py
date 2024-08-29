from django.contrib import admin
from .models import Portfolio, Item

# Register your models here.

class ItemInline(admin.TabularInline):
    model = Item
    readonly_fields = ('user',)
    list_display = ('ticker', 'quantity')
    extra = 0

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')
    list_filter = ('user',)
    inlines = [ItemInline]


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Item)