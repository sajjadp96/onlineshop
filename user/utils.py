from user.models import User
from product.models import Product
from datetime import datetime

today = datetime.now().date()

def get_all_users_email()-> list:
    
    emails = list(User.objects.all().values_list('email',flat=True))
    
    return emails[1:]


def get_new_products()-> list:
    
    products = list(Product.objects.filter(created_at__date=today).values_list("name",flat=True))
    
    return products


def ad_message()->str:
    
    m = ("\n".join(get_new_products()))
  
    ad_str = f"""The following products are available\n{m}"""
    
    return ad_str