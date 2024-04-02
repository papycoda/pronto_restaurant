from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class FoodItem(MenuItem):
    class Meta:
        verbose_name = "food item"

class DrinkItem(MenuItem):
    class Meta:
        verbose_name = "drink item"

class GrubItem(MenuItem):
    size = models.CharField(max_length=100, blank=True, null=True)
    fillings = models.CharField(max_length=100, blank=True, null=True)
    extra_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    order = models.OneToOneField('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='table_associated')

    def __str__(self):
        return f"Table {self.number}"

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders_placed')
    items = models.ManyToManyField(FoodItem, through='OrderItem')
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for Table {self.table.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, null=True, blank=True)
    drink_item = models.ForeignKey(DrinkItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        item_name = self.food_item.name if self.food_item else self.drink_item.name
        return f"{self.quantity} x {item_name} (Order: {self.order.id})"

class Reservation(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')

    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.date_time} at {self.table}"
