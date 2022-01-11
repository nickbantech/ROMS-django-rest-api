from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from FoodItems.models import Product
from django.conf import settings

CURRENCY = settings.CURRENCY


class Table(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=150)
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_free = models.BooleanField(default=True)
    active_order_id = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.active_order_id = self.table_orders.filter(active=True).last().id\
            if self.table_orders.filter(active=True).exists() else None
        self.is_free = False if self.active_order_id else True
        self.value = 0 if self.is_free else self.value
        super(Table, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'
    
    def tag_active_order_id(self):
        last_table = self.table_orders.filter(active=True).last()
        return last_table.id if last_table else 'No Table'

    
class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    title = models.CharField(blank=True, null=True, max_length=50)
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL, related_name='table_orders')

    class Meta:
        ordering = ['-timestamp', ]

    def __str__(self):
        return f'Table {self.table.title}' if self.table else 'Table'

    def save(self, *args, **kwargs):
        self.value = self.order_items.all().aggregate(Sum('total_value'))['total_value__sum'] if \
            self.order_items.all() else 0
        self.value = self.value if self.value else 0
        super(Order, self).save(*args, **kwargs)
        self.table.value = self.value if self.value and self.active else 0
        self.table.save()

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_table(self):
        return f'{self.table.title}' if self.table else 'No table'

    def tag_active(self):
        return 'Closed' if not self.active else 'Active'

    def tag_timestamp(self):
        return self.timestamp.date()
    

@receiver(post_save, sender=Order)
def update_table_status(sender, instance, created, **kwargs):
    if created:
        instance.table.is_free = False
        instance.table.save()


class OrderItem(models.Model):
    product_related = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_related = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    value = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    qty = models.PositiveIntegerField(default=1)
    total_value = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f'{self.product_related.title}'

    def save(self, *args, **kwargs):
        self.value = self.product_related.value
        self.total_value = self.value * self.qty
        super(OrderItem, self).save(*args, **kwargs)
        self.order_related.save()

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_total_value(self):
        return f'{self.total_value} {CURRENCY}'

    def tag_order_related(self):
        return f'{self.order_related.__str__}'

    def tag_product_related(self):
        return f'{self.product_related.title}'


@receiver(post_delete, sender=OrderItem)
def update_order(sender, instance, *args, **kwargs):
    instance.order_related.save()