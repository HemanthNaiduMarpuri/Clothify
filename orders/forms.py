from django import forms
from decimal import Decimal

class CheckOutForm(forms.Form):
    recipient_name = forms.CharField(max_length=255, required=True, label="Full Name")
    recipient_phone = forms.CharField(max_length=20, required=True, label="Phone Number")
    address_text = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=True, label="Address")
    latitude = forms.DecimalField(max_digits=15, decimal_places=8, required=False)
    longitude = forms.DecimalField(max_digits=15, decimal_places=8, required=False)    

    def clean_recipient_phone(self):
        v = self.cleaned_data['recipient_phone'].strip()
        if len(v) < 6:
            raise forms.ValidationError("Phone Number is not Valid!!")
        return v