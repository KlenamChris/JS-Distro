from django import forms
# from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        # model = Item
        fields = ['item_type', 'model', 'assigned_to', 'data_assigned']