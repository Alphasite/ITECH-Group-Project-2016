from django.contrib import admin
from models import GameState, Event, Results, Price, OwnItem, Item

# Register your models here.
admin.site.register(GameState)
admin.site.register(Results)
admin.site.register(Event)
admin.site.register(Item)
admin.site.register(Price)
admin.site.register(OwnItem)