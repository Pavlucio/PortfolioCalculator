from django import forms
from .models import Portfolio, Item

CURRENCY_CHOISES = [
    ("AUD", "Australian Dollar"),
    ("BGN", "Bulgarian Lev"),
    ("BRL", "Brazilian Real"),
    ("CAD", "Canadian Dollar"),
    ("CHF", "Swiss Franc"),
    ("CNY", "Chinese Renminbi Yuan"),
    ("CZK", "Czech Koruna"),
    ("DKK", "Danish Krone"),
    ("EUR", "Euro"),
    ("GBP", "British Pound"),
    ("HKD", "Hong Kong Dollar"),
    ("HUF", "Hungarian Forint"),
    ("IDR", "Indonesian Rupiah"),
    ("ILS", "Israeli New Sheqel"),
    ("INR", "Indian Rupee"),
    ("ISK", "Icelandic Króna"),
    ("JPY", "Japanese Yen"),
    ("KRW", "South Korean Won"),
    ("MXN", "Mexican Peso"),
    ("MYR", "Malaysian Ringgit"),
    ("NOK", "Norwegian Krone"),
    ("NZD", "New Zealand Dollar"),
    ("PHP", "Philippine Peso"),
    ("PLN", "Polish Złoty"),
    ("RON", "Romanian Leu"),
    ("SEK", "Swedish Krona"),
    ("SGD", "Singapore Dollar"),
    ("THB", "Thai Baht"),
    ("TRY", "Turkish Lira"),
    ("USD", "United States Dollar"),
    ("ZAR", "South African Rand")
]
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title']
        exclude = ['user']


class CurrencyForm(forms.Form):
    base_currency = forms.ChoiceField(choices=CURRENCY_CHOISES, label="Select base currency")
    portfolio_id = forms.IntegerField(widget=forms.HiddenInput())


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['ticker', 'quantity']


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['ticker', 'quantity']
        widgets = {'ticker': forms.TextInput(attrs={'readonly': 'readonly'})}