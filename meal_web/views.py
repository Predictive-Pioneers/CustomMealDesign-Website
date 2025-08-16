from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import timedelta

from .models import WeeklyMenu, Meal, Subscription, MenuItem, Order
from .forms import SubscriptionForm

def home(request):
    return render(request, 'meal_web/home.html')

def menu_view(request):
    menu = WeeklyMenu.objects.order_by('-week_start').first()
    meals = Meal.objects.none()
    if menu:
        meals = Meal.objects.filter(id__in=[item.meal_id for item in menu.items.all()])
    diet = request.GET.get('diet')
    if diet:
        meals = meals.filter(diet_type=diet)
    return render(request, 'meal_Web/menu.html', {'menu': menu, 'meals': meals, 'diet': diet})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created — please log in')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'meal_Web/register.html', {'form': form})

@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)  # Don't save to DB yet
            subscription.user = request.user        # Set user
            subscription.save()                     # Now save
            return redirect('my_subscription')
    else:
        form = SubscriptionForm()
    return render(request, 'meal_web/subscribe.html', {'form': form})

def generate_orders_for_subscription(sub: Subscription):
    if not sub.user_id:
        raise ValueError("Subscription must have a user before generating orders.")

    menu = WeeklyMenu.objects.order_by('-week_start').first()
    if not menu:
        return
    
    days = sub.selected_days_list()  # should return a list of day indices (0=Mon)
    for d in days:
        try:
            item = MenuItem.objects.get(menu=menu, day_of_week=d)
        except MenuItem.DoesNotExist:
            item = None
        
        if item:
            # Match diet type or use alternative
            if item.meal.diet_type == sub.diet_preference:
                meal = item.meal
            else:
                alt = MenuItem.objects.filter(
                    menu=menu,
                    day_of_week=d,
                    meal__diet_type=sub.diet_preference
                ).first()
                meal = alt.meal if alt else item.meal

            order_date = menu.week_start + timedelta(days=d)
            Order.objects.create(subscription=sub, meal=meal, date=order_date)

@login_required
def my_subscription(request):
    sub = Subscription.objects.filter(user=request.user).first()
    orders = []
    if sub:
        orders = sub.orders.order_by('date')
    return render(request, 'meal_web/my_subscription.html', {'sub': sub, 'orders': orders})

@login_required
def toggle_paid(request):
    sub = get_object_or_404(Subscription, user=request.user)
    sub.paid = not sub.paid
    sub.save()
    messages.success(request, f"Subscription paid status set to {sub.paid}")
    return redirect('my_subscription')

@login_required
def toggle_pause(request):
    sub = get_object_or_404(Subscription, user=request.user)
    sub.paused = not sub.paused
    sub.save()
    messages.success(request, f"Subscription paused={sub.paused}")
    return redirect('my_subscription')

@login_required
def change_diet(request):
    sub = get_object_or_404(Subscription, user=request.user)
    if request.method == 'POST':
        new = request.POST.get('diet')
        if new in dict(Meal.DIET_CHOICES):
            sub.diet_preference = new
            sub.save()
            messages.success(request, 'Diet preference updated')
        return redirect('my_subscription')
    return render(request, 'meal_web/change_diet.html', {'sub': sub, 'choices': Meal.DIET_CHOICES})
