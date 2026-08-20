from django.contrib import admin
from .models import Client,Formateur,Formation,Reservation,Profile
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Client)
admin.site.register(Formateur)
admin.site.register(Formation)
admin.site.register(Reservation)
admin.site.register(Profile)

#Mix Profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)