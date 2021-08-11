from django.db import models

# Create your models here.
class OneModelId(models.Model):

    class Meta:
        app_label = 'two'

    def __str__(self):
        return f'{self.id}'

class TwoModel(models.Model):
    name = models.CharField(max_length=10)
    one_model = models.ForeignKey(OneModelId, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'two'

    def __str__(self):
        return self.name

