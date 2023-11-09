from django.db import models
from user.models import Address
from product.models import Product
from user.models import User

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

    
class Order(BaseModel):
    
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    address = models.ForeignKey(Address,on_delete=models.CASCADE,related_name="address")
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    status_field = models.TextChoices("Status","Pending Rejected Sent")
    status = models.CharField(choices=status_field.choices, max_length=10,default="Pending")
    
    # price = models.DecimalField(max_digits=6,decimal_places=2)

    @property
    def price(self):
        total = sum([(item.price*item.quantity)/100*item.discount for item in self.items.all()])
        return total

    @property
    def final_price(self):
        return self.price / 100 * (self.discount or 100)
    
    
    def __str__(self) -> str:
        return f"{self.customer}"
    


class OrderItem(BaseModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    
    
    def __str__(self) -> str:
        return f"{self.quantity}"
    
    def save(self, *args, **kwargs):
        related_order_items = OrderItem.objects.filter(order=self.order, product=self.product).exclude(id=self.id)
        if len(related_order_items):
            total_quantity = sum([item.quantity for item in related_order_items])
            for item in related_order_items:
                item.delete()
            self.quantity = total_quantity + self.quantity
        super().save(*args, **kwargs)
    
