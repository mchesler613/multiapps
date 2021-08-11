from django.db import models

# Create your models here.
class OneModel(models.Model):
    name=models.CharField(max_length=10)

    class Meta:
        app_label = 'one'

    def __str__(self):
        return self.name
