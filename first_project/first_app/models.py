from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=264, unique=False)
    last_name = models.CharField(max_length=264, unique=False)
    email = models.EmailField(max_length=264,unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

class Order(models.Model):
    user_fk = models.ForeignKey(User, verbose_name=("User FK"), on_delete=models.CASCADE)
    order_name = models.CharField(("Order Name"), max_length=50)
    order_amount = models.IntegerField(("Order Amount"))
            
class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)
    
    def __str__(self):
        return self.top_name 

#multiple products can be added to multiple orders  
# book can have multiple authors, and an author can have written multiple books.
class Product(models.Model):
    orders = models.ManyToManyField('Order')
    
class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    url = models.URLField(unique=True)
        
    def __str__(self):
        return self.name 
    
    # In the code snippet I provided, on_delete=models.
    # CASCADE is added to the ForeignKey fields in both the Webpage and AccessRecord models. 
    # This argument specifies that when a referenced Topic or Webpage is deleted, 
    # all related Webpage or AccessRecord objects should also be deleted. This ensures referential integrity in the database.

class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return str(self.name)
