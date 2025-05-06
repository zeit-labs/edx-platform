from django.contrib import admin
from .models import (
    Order,
    Coupon,
    Transaction,
    WebhookEvent,
    AuditLog,
    CatalogueItem,
    OrderItem,
    # Invoice,
    # InvoiceItem,
    # CreditMemo,
    # Enrollment,
    # EnrollmentOrder,
    CouponUsage
)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status',)
    search_fields = ('id', 'user__email')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'max_usage', 'usage_count', 'expires_at')
    search_fields = ('code',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'type', 'status', 'gateway', 'method', 'amount', 'currency', 'created_at')
    list_filter = ('type', 'status', 'gateway', 'method', 'mode')
    search_fields = ('id', 'gateway_transaction_id')


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'gateway', 'event_type', 'related_transaction', 'handled', 'created_at')
    list_filter = ('gateway', 'handled')
    search_fields = ('id', 'event_type')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'gateway', 'created_at')
    search_fields = ('action', 'user__email')


@admin.register(CatalogueItem)
class CatalogueItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'item_ref_id', 'price', 'currency', 'created_at')
    list_filter = ('type', 'currency')
    search_fields = ('item_ref_id',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'catalogue_item', 'original_price', 'discount_amount', 'final_price')
    search_fields = ('id', 'order__id', 'catalogue_item__item_ref_id')


# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'status', 'total', 'currency', 'created_at', 'paid_at')
#     list_filter = ('status', 'currency')
#     search_fields = ('id', 'order__id')
#
#
# @admin.register(InvoiceItem)
# class InvoiceItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'invoice', 'order_item', 'original_price', 'discount_amount', 'price', 'quantity')
#
#
# @admin.register(CreditMemo)
# class CreditMemoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'invoice', 'total', 'gateway_refund_transaction_id', 'created_at')
#     search_fields = ('gateway_refund_transaction_id',)
#
#
# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'course_id', 'enrollment_type', 'created_at')
#     list_filter = ('enrollment_type',)
#     search_fields = ('course_id', 'user__email')
#
#
# @admin.register(EnrollmentOrder)
# class EnrollmentOrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'enrollment', 'order', 'created_at')
#     search_fields = ('order__id', 'enrollment__id')


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'coupon', 'user', 'count', 'created_at')
    search_fields = ('coupon__code', 'user__email')
