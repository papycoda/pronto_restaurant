import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
#from recurrence.fields import RecurrenceField
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta
import pytz
from django.utils import timezone

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
    table_group = models.CharField(max_length=50, choices=[
        ('bar', 'Bar'),
        ('lounge', 'Lounge'),
        ('outdoor', 'Outdoor')
    ])
    is_reserved = models.BooleanField(default=False)
    reserved_until = models.DateTimeField(null=True, blank=True)
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='table_associated')


    def __str__(self):

        return f"{self.table_group} Table {self.number}"

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    email = models.EmailField()
    date_time = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')

    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.date_time} at {self.table}"


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

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(blank = True, null = True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100, default='The Pronto, Ilorin')
    image = models.ImageField(upload_to='Static/images/', blank=True, null=True)
    ticket_url = models.URLField(blank=True, null=True)
    recurring = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        if not self.ticket_url:
            self.ticket_url = None
        super().save(*args, **kwargs)

    def get_next_occurrence(self):
        now = datetime.now(pytz.UTC)
        today = now.weekday()  # Monday is 0 and Sunday is 6
        start_time_today = datetime.combine(now.date(), self.start_time).replace(tzinfo=pytz.UTC)
        end_time_today = datetime.combine(now.date(), self.end_time).replace(tzinfo=pytz.UTC)
        
        # Check if the event is today and hasn't ended yet
        if start_time_today <= now <= end_time_today:
            return start_time_today
        
        # Find the next occurrence day
        event_days = [day.day_of_week for day in self.days.all()]
        days_ahead = [(day - today + 7) % 7 for day in range(7) if day in event_days]
        
        if not days_ahead:
            return None
        
        days_until_next = min(days_ahead)
        next_occurrence_date = now.date() + timedelta(days=days_until_next)
        next_occurrence = datetime.combine(next_occurrence_date, self.start_time).replace(tzinfo=pytz.UTC)
        
        return next_occurrence

class EventDay(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    event = models.ForeignKey(Event, related_name='days', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.event.name} on {self.day_of_week}"

