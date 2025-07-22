from django.db import models
from django.conf import settings
from django.urls import reverse

import os
import uuid
# Create your models here.

# 基础信息

# 产品
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    in_name = models.CharField(max_length=200, unique=True)
    out_name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)

# 设备
class Machine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30, unique=True)
    note = models.TextField(max_length=1000, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('machines-detail', args=[str(self.id)])
    
    def __str__(self):
        return '%s' % (self.name)
    
# 客户
class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

# 供应商
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

# 原料
class Material(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

# 关联信息
# 每台设备基础产品产能
# class MachineCapability(models.Model):
#     machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
#     product = models.CharField(max_length=100)
#     process = models.CharField(max_length=20)
