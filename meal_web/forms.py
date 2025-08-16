from django import forms
from .models import Subscription, Meal

class SubscriptionForm(forms.ModelForm):
    days = forms.MultipleChoiceField(
        choices=[(str(i), label) for i, label in [(0,'Mon'),(1,'Tue'),(2,'Wed'),(3,'Thu'),(4,'Fri'),(5,'Sat'),(6,'Sun')]],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Subscription
        fields = ['diet_preference']

    def save(self, user=None, commit=True):
        instance = super().save(commit=False)
        days_list = self.cleaned_data.get('days', [])
        instance.selected_days = ",".join(days_list)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
