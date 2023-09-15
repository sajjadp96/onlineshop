from django.db import models
from user.models import Address
from product.models import Product

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

    
class Order(BaseModel):
    customer = models.CharField(max_length=15,)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    @property
    def price(self):
        return sum([item.price*item.quantity for item in self.orderitem_set.all()])

    def __str__(self) -> str:
        return f"{self.customer}"



class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    

    def __str__(self) -> str:
        return f"{self.quantity}"
