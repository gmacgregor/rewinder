from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    AddField('Bookmark', 'image', models.ImageField, max_length=100, null=True),
    AddField('Bookmark', 'remove_image', models.BooleanField, initial=False),
    AddField('Bookmark', 'html_image_caption', models.TextField, null=True),
    AddField('Bookmark', 'image_caption', models.TextField, null=True)
]
