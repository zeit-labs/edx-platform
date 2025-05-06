from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

#
# class Order(models.Model):
#     owner = models.ForeignKey(
#         get_user_model(),
#         null=True,
#         related_name='baskets',
#         on_delete=models.CASCADE,
#         verbose_name=_("Owner"))
#
#     # Basket statuses
#     # - Frozen is for when a basket is in the process of being submitted
#     #   and we need to prevent any changes to it.
#     OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
#         "Open", "Merged", "Saved", "Frozen", "Submitted")
#     STATUS_CHOICES = (
#         (OPEN, _("Open - currently active")),
#         (MERGED, _("Merged - superceded by another basket")),
#         (SAVED, _("Saved - for items to be purchased later")),
#         (FROZEN, _("Frozen - the basket cannot be modified")),
#         (SUBMITTED, _("Submitted - has been ordered at the checkout")),
#     )
#     status = models.CharField(
#         _("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)
#
#     # A basket can have many vouchers attached to it.  However, it is common
#     # for sites to only allow one voucher per basket - this will need to be
#     # enforced in the project's codebase.
#     vouchers = models.ManyToManyField(
#         'voucher.Voucher', verbose_name=_("Vouchers"), blank=True)
#
#     date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
#     date_merged = models.DateTimeField(_("Date merged"), null=True, blank=True)
#     date_submitted = models.DateTimeField(_("Date submitted"), null=True,
#                                           blank=True)
#
#     # Only if a basket is in one of these statuses can it be edited
#     editable_statuses = (OPEN, SAVED)



class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')
        CANCELLED = 'cancelled', _('Cancelled')
        REFUNDED = 'refunded', _('Refunded')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        FIXED = 'fixed', _('Fixed')
        PERCENTAGE = 'percentage', _('Percentage')

    code = models.CharField(max_length=50, primary_key=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_usage = models.PositiveIntegerField()
    usage_count = models.PositiveIntegerField(default=0)  # optionally move to usage model
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    class Type(models.TextChoices):
        PAYMENT = 'payment', _('Payment')
        REFUND = 'refund', _('Refund')

    class Direction(models.TextChoices):
        CREDIT = 'credit', _('Credit')
        DEBIT = 'debit', _('Debit')

    class Status(models.TextChoices):
        CREDIT = 'initiated', _('Initiated')
        DEBIT = 'success', _('Debit')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=50, choices=Status.choices)
    direction = models.CharField(max_length=10, choices=Direction.choices)
    gateway = models.CharField(max_length=50)
    gateway_transaction_id = models.CharField(max_length=255)
    method = models.CharField(max_length=50, help_text='Payment method: Card, Paypal, Apple Pay, etc.')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    response = models.JSONField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True, help_text='Admin stated note for refund reason')
    mode = models.CharField(max_length=20, default='sandbox')
    initiator_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WebhookEvent(models.Model):
    gateway = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    related_transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, related_name='webhook_events')
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)


class AuditLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    gateway = models.CharField(max_length=50)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CatalogueItem(models.Model):
    class Type(models.TextChoices):
        PAID_COURSE = 'paid_course', _('Paid Course')
        # Add other types as needed

    type = models.CharField(max_length=50, choices=Type.choices)
    item_ref_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    catalogue_item = models.ForeignKey(CatalogueItem, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)


# class Invoice(models.Model):
#     class Status(models.TextChoices):
#         DRAFT = 'draft', _('Draft')
#         PAID = 'paid', _('Paid')
#         CANCELLED = 'cancelled', _('Cancelled')
#
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='invoices')
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     currency = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     paid_at = models.DateTimeField(null=True, blank=True)
#
#
# class InvoiceItem(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
#     order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True)
#     original_price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)


# class CreditMemo(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='credit_memos')
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     reason = models.TextField()
#     gateway_refund_transaction_id = models.CharField(max_length=255)
#     transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)


# class EnrollmentOrder(models.Model):
#     enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='enrollment_orders')
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
