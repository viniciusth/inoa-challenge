from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Active(models.Model):
  ticker = models.CharField(max_length=6)
  user = models.OneToOneField(
    User, 
    on_delete=models.CASCADE,
    primary_key=True,
    default=None,
  )

  def __str__(self):
    return '{0} - {1}'.format(self.ticker, self.usr)
   