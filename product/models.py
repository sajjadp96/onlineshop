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
    image = models.ImageField(upload_to='images/categories/', null=True)
    category = models.ForeignKey('self')

    def __str__(self) -> str:
        return self.title


class Product(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/foods/', null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
