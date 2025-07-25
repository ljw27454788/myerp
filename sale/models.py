from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

import os
import uuid

User = get_user_model()
# Create your models here.

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order_code = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def save(self, *args, **kwargs):
        if not self.order_code:
            today = timezone.now().strftime('%Y%m%d')
            prefix = 'C' + today
            
            last_order = Order.objects.filter(order_code__startswith=prefix).order_by('-order_code').first()
            if last_order:
                last_seq = int(last_order.order_number[-4:])
                next_seq = f'{last_seq + 1:04d}'
            else:
                next_seq = '0001'
                
            self.order_number = prefix + next_seq
            
        super().save(*args, **kwargs)