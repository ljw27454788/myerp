from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

import os
import uuid

User = get_user_model()
# Create your models here.

# 基础信息
class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="材料种类名称")

    class Meta:
        verbose_name = "产品种类"

    def __str__(self):
        return self.name


# 产品
class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', '千克'),
        ('pcs', '个'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    in_name = models.CharField(max_length=200, unique=True, verbose_name="内部名称")
    out_name = models.CharField(max_length=200, unique=True, verbose_name="对外名称")
    code = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="产品编码")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pcs', verbose_name="单位")
    price = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True, verbose_name="产品价格")
    cost = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True, verbose_name="产品成本")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="产品种类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "产品"
    
    def __str__(self):
        return self.in_name
    
    def get_materials(self):
        """获取产品所需的所有原料"""
        return self.productmaterial_set.all()

# 设备
class Machine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30, unique=True)
    note = models.TextField(max_length=1000, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('factory:machines-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name
    
# 客户
class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

# 供应商
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name

class MaterialCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="材料种类名称")

    class Meta:
        verbose_name = "原料种类"

    def __str__(self):
        return self.name

# 原料
class Material(models.Model):
    UNIT_CHOICES = [
        ('kg', '千克'),
        ('pcs', '个'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True, verbose_name="原料名称")
    code = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="原料编码")
    specification = models.CharField(max_length=200, null=True, blank=True, verbose_name="规格")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pcs', verbose_name="单位")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="单价")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="供应商")
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="原料种类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "原料"
    
    def __str__(self):
        return self.name


# 产品原料BOM（物料清单）
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="原料")
    quantity = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="用量")
    
    class Meta:
        unique_together = ("product", "material")
        verbose_name = "产品原料清单"
    
    def __str__(self):
        return f"{self.product.name} - {self.material.name}"