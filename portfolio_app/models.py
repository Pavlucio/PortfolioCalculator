from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Portfolio(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.title} {self.created}'


class Item(models.Model):
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ticker = models.CharField(max_length=200)
    quantity = models.IntegerField()
    created = models.DateField(auto_now_add=True)


    class Meta:
        ordering = ['ticker']

    def __str__(self):
        return f'{self.ticker} {self.quantity}'