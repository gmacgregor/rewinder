from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    AddField('Quote', 'credit', models.CharField, max_length=255, null=True),
    DeleteField('Quote', 'author'),
    DeleteField('Quote', 'source')
]
