from django.contrib import admin
from .models import Dish, Bill, DishComment, ServerComment

# Register your models here.
admin.site.register(Dish)
admin.site.register(Bill)
admin.site.register(DishComment)
admin.site.register(ServerComment)