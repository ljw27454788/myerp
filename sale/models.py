from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from factory.models import Client, Product

import os
import uuid

User = get_user_model()
# Create your models here.


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    invoice_code = models.CharField(max_length=20, unique=True, editable=False)
    note = models.TextField(max_length=200, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.invoice_code:
            today = timezone.now().strftime("%Y%m%d")
            prefix = "C" + today

            last_order = (
                Order.objects.filter(invoice_code__startswith=prefix)
                .order_by("-invoice_code")
                .first()
            )
            if last_order:
                last_seq = int(last_order.order_number[-4:])
                next_seq = f"{last_seq + 1:04d}"
            else:
                next_seq = "0050"

            self.invoice_code = prefix + next_seq

        super().save(*args, **kwargs)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    quantity = models.PositiveIntegerField(default=0)
    remain_quantity = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=4)
    complete = models.BooleanField(default=False)
    reply_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.quantity * self.price


class SendInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    invoice_code = models.CharField(max_length=20, unique=True, editable=False)
    note = models.TextField(max_length=200, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=12, decimal_places=4)

    def save(self, *args, **kwargs):
        if not self.invoice_code:
            today = timezone.now().strftime("%Y%m%d")
            prefix = "CY" + today

            last_order = (
                Order.objects.filter(invoice_code__startswith=prefix)
                .order_by("-invoice_code")
                .first()
            )
            if last_order:
                last_seq = int(last_order.order_number[-4:])
                next_seq = f"{last_seq + 1:04d}"
            else:
                next_seq = "0050"

            self.invoice_code = prefix + next_seq

        super().save(*args, **kwargs)


class SendOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    invoice = models.ForeignKey(SendInvoice, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    total = models.DecimalField(max_digits=12, decimal_places=4, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

# 价格记录
class PriceRecord(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="产品")
    price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="单价")
    moq = models.PositiveIntegerField(null=True, blank=True, verbose_name="最小起订量")
    has_tax = models.BooleanField(default=False, verbose_name="是否含税")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("client", "product", "moq")
        
    def __str__(self):
        return f'{self.client}_{self.product}'

# 样品单
class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="产品")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="客户")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    lead_time = models.DateField(default=None, null=True, blank=True, verbose_name="回复交期")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
    send_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name="发送日")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.client}_{self.product}_{self.quantity}'
