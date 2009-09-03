from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    AddField('Quote', 'slug', models.SlugField, max_length=50, null=True, db_index=True)
]

