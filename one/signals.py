from .models import OneModel
from django.db.models.signals import post_save

def save_one_model(sender, instance, **kwargs):
    print(f'save_one_model: {sender}, {instance})
