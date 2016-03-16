from django.contrib import admin

# Register your models here.
from .models import Board, Pin

admin.site.register(Board)
admin.site.register(Pin)
