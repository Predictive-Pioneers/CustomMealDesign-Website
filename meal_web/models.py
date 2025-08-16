from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meal(models.Model):
    DIET_CHOICES = [
        ('veg', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('high_protein', 'High Protein'),
    ]
    name = models.CharField(max_length=120)
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES)
    calories = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_diet_type_display()})"

class WeeklyMenu(models.Model):
    week_start = models.DateField(help_text='Enter the Monday date for this menu')

    def __str__(self):
        return f"Weekly Menu starting {self.week_start}"

class MenuItem(models.Model):
    DAY_CHOICES = [
        (0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), (4, 'Fri'), (5, 'Sat'), (6, 'Sun')
    ]
    menu = models.ForeignKey(WeeklyMenu, on_delete=models.CASCADE, related_name='items')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)

    class Meta:
        unique_together = ('menu', 'day_of_week')

    def __str__(self):
        return f"{self.menu.week_start} - {self.get_day_of_week_display()} : {self.meal.name}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet_preference = models.CharField(max_length=20, choices=Meal.DIET_CHOICES)
    # store selected days as comma-separated ints '0,2,4' => Mon,Wed,Fri
    selected_days = models.CharField(max_length=50, help_text='Comma-separated days as 0=Mon..6=Sun')
    active = models.BooleanField(default=True)
    paused = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)  # simulated payment
    created_at = models.DateTimeField(auto_now_add=True)

    def selected_days_list(self):
        if not self.selected_days:
            return []
        return [int(x) for x in self.selected_days.split(',') if x.strip().isdigit()]

    def __str__(self):
        return f"Subscription({self.user.username}) - {self.get_diet_preference_display()}"

class Order(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='orders')
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    STATUS = [('pending','Pending'), ('delivered','Delivered'), ('cancelled','Cancelled')]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.date} - {self.meal}"
