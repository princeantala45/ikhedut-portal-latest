from django.contrib import admin
from ikhedut.models import (
    Contact,
    Signup,
    Ad,
    CropSale,
    Order,
    OrderItem
)

admin.site.register(Contact)
admin.site.register(Signup)

@admin.register(CropSale)
class CropSaleAdmin(admin.ModelAdmin):
    list_display = ("crop", "seller", "quantity", "price", "is_approved")
    list_filter = ("is_approved",)
    search_fields = ("crop", "seller__username")

    actions = ["approve_selected", "reject_selected"]

    # This ensures that even if you add a crop from the Admin panel, 
    # the seller is set to YOU (the admin) automatically if left blank.
    def save_model(self, request, obj, form, change):
        if not obj.seller:
            obj.seller = request.user
        super().save_model(request, obj, form, change)

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)

    def reject_selected(self, request, queryset):
        for obj in queryset:
            if obj.image:
                obj.image.delete(save=False)
            obj.delete()
# AD ADMIN
# -------------------------
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("productname", "price", "city", "is_approved")
    list_filter = ("is_approved", "city")
    search_fields = ("productname", "city", "fullname")

    actions = ["approve_ads", "reject_ads"]

    def approve_ads(self, request, queryset):
        queryset.update(is_approved=True)

    approve_ads.short_description = "Approve selected ads"

    def reject_ads(self, request, queryset):
        for obj in queryset:
            if obj.image:
                obj.image.delete(save=False)
            obj.delete()

    reject_ads.short_description = "Reject selected ads"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "fullname",
        "mobile",
        "payment_method",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "user__username",
        "fullname",
        "mobile",
        "upi_id",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "total_amount",
        "created_at",
        "cancel_requested_at",
    )

    inlines = [OrderItemInline]

    actions = ["approve_cancellation"]

    def approve_cancellation(self, request, queryset):
        updated = queryset.filter(
            status="cancel_requested"
        ).update(status="cancelled")

        self.message_user(
            request,
            f"{updated} order(s) cancelled successfully."
        )

    approve_cancellation.short_description = (
        "Approve selected cancellation requests"
    )
