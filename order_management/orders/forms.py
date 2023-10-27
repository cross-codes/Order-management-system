from django import forms
from .models import Order


class UpdateOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["title", "desc", "date", "pr_tag"]


class OrderSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)
