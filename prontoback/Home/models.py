from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.core.files.storage import FileSystemStorage

class CustomStaticFileStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            return name  
        return super()._save(name, content)

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    default_image = models.ImageField(upload_to='Static/images/', storage=CustomStaticFileStorage(), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"



class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
    image = ProcessedImageField(upload_to='Static/images/', 
                                processors=[ResizeToFit(width=300, height=150)], 
                                format='JPEG', 
                                options={'quality': 90}, 
                                blank=True, 
                                null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.price and self.price < 0:
            raise ValidationError(_('Price cannot be negative.'))
        super().save(*args, **kwargs)


class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='table_associated')

    def __str__(self):
        return f"Table {self.number}"


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders_placed')
    is_complete = models.BooleanField(default=False)
    items = models.ManyToManyField(MenuItem, through='OrderItem') 
    order_time = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return f"Order for Table {self.table.number} ({self.order_time})"  


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default = '')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order: {self.order.id})"


class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')  # Add related_name
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')

    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.date_time} at {self.table}"

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100,default='The Pronto, Ilorin')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    ticket_url = models.URLField(blank=True, null=True) 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"
        ordering = ['date']

    def save(self, *args, **kwargs):
        if not self.ticket_url:
            self.ticket_url = None
        super().save(*args, **kwargs)
        

 