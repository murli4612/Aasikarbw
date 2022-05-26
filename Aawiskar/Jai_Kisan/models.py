from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
STATE_CHOICES = (
  ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
  ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
  ('Assam','Assam'),
  ('Bihar','Bihar'),
  ('Chandigarh','Chandigarh'),
  ('Chhattisgarh','Chhattisgarh'),
  ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
  ('Daman and Diu','Daman and Diu'),
  ('Delhi','Delhi'),
  ('Goa','Goa'),
  ('Gujarat','Gujarat'),
  ('Haryana','Haryana'),
  ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu & Kashmir','Jammu & Kashmir'),
  ('Jharkhand','Jharkhand'),
  ('Karnataka','Karnataka'),
  ('Kerala','Kerala'),
  ('Lakshadweep','Lakshadweep'),
  ('Madhya Pradesh','Madhya Pradesh'),
  ('Maharashtra','Maharashtra'),
  ('Manipur','Manipur'),
  ('Meghalaya','Meghalaya'),
  ('Mizoram','Mizoram'),
  ('Nagaland','Nagaland'),
  ('Odisha','Odisha'),
  ('Puducherry','Puducherry'),
  ('Punjab','Punjab'),
  ('Rajasthan','Rajasthan'),
  ('Sikkim','Sikkim'),
  ('Tamil Nadu','Tamil Nadu'),
  ('Telangana','Telangana'),
  ('Tripura','Tripura'),
  ('Uttarakhand','Uttarakhand'),
  ('Uttar Pradesh','Uttar Pradesh'),
  ('West Bengal','West Bengal'),
)
class Customer(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 name = models.CharField(max_length=200)
 locality = models.CharField(max_length=200)
 city = models.CharField(max_length=50)
 zipcode = models.IntegerField()
 state = models.CharField(choices=STATE_CHOICES, max_length=50)

 def __str__(self):
  # return self.user.username
  return str(self.id)
CATEGORY_CHOICES = (
 ('T', 'Tracter'),
 ('BM', 'Boring Machine'),
 ('H', 'Harvestor'),
 ('C', 'Cultivater'),
)
class Product(models.Model):
 title = models.CharField(max_length=100)
 selling_price = models.FloatField()
 discounted_price = models.FloatField()
 description = models.TextField()
 brand = models.CharField(max_length=100)
 category = models.CharField( choices=CATEGORY_CHOICES, max_length=2)
 product_image = models.ImageField(upload_to='productimg',default="")

 def __str__(self):
  return str(self.id)

class Item(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 duration = models.PositiveIntegerField(default=1)

 def __str__(self):
  return str(self.id)

 @property
 def total_cost(self):
   return self.duration * self.product.discounted_price

STATUS_CHOICES = (
     ('Accepted', 'Accepted'),
     ('On The Way', 'On The Way'),
     ('Work in Progress','Work in progress'),
     ('Completed', 'Completed'),
     ('Cancel', 'Cancel')
 )
class Booked(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     duration = models.PositiveIntegerField(default=1)
     ordered_date = models.DateTimeField(auto_now_add=True)
     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

     # Below Property will be used by orders.html page to show total cost
     @property
     def total_cost(self):
         return self.duration * self.product.discounted_price

class Vendor(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, primary_key=True, db_column='id',on_delete=models.CASCADE)
    User_name=models.CharField(max_length=200)
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    email =models.EmailField(max_length=50)
    phone =models.CharField(max_length=12)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    city = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    password = models.CharField(max_length=20)
    conform_password =models.CharField(max_length=20)
    def __str__(self):
        # return self.user.username
        return str(self.id)

        class Meta:
            db_table = "auth_user_datum"
            verbose_name = "User Data"
            verbose_name_plural = "User Datum"
