from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        
class Category(BaseModel):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/categories/',blank=True,null=True)
    category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='categorychild',blank=True,null=True)

    def __str__(self) -> str:
        return self.title


class Product(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/products', null=True,blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    discount = models.DecimalField(decimal_places=1, max_digits=3, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='productcategory')
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
