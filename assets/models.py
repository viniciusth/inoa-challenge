from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Asset(models.Model):
  ticker = models.CharField(max_length=6)
  user = models.ForeignKey(
    User, 
    on_delete=models.CASCADE,
  )
  price = models.DecimalField(max_digits=20, decimal_places=4, null=True)
  stop_loss_price = models.DecimalField(max_digits=20, decimal_places=4, null=True)
  stop_limit_price = models.DecimalField(max_digits=20, decimal_places=4, null=True)
  def __str__(self):
    return '{0}'.format(self.ticker)
   