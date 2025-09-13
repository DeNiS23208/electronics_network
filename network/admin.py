from django.contrib import admin
from django.utils.html import format_html
from .models import NetworkNode, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    list_filter = ("release_date",)

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "supplier_link", "debt", "created_at", "level_display")
    list_filter = ("city", "country")  # фильтр по городу (и стране)
    search_fields = ("name", "city", "country", "email")
    filter_horizontal = ("products",)
    actions = ["clear_debt"]

    @admin.display(description="Поставщик", ordering="supplier__name")
    def supplier_link(self, obj: NetworkNode):
        if not obj.supplier:
            return "—"
        return format_html(
            '<a href="/admin/network/networknode/{id}/change/">{name}</a>',
            id=obj.supplier.id, name=obj.supplier.name
        )

    @admin.display(description="Уровень")
    def level_display(self, obj: NetworkNode):
        return obj.level

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность обнулена у {updated} объектов.")
