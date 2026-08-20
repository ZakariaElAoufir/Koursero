from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.user.username

#User Profile by default after signing up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

#Automate the Profile
post_save.connect(create_profile, sender=User)


class Client(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Formateur(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Formation(models.Model):
    titre = models.CharField(max_length=255)
    descriptif = models.CharField(max_length=250, default='', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_formation = models.DateTimeField(default=datetime.datetime.today)
    image = models.ImageField(upload_to='uploads/formation/', default='uploads/formation/default.jpg')
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE, related_name='reservations')
    date_reservation = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return str(self.formation)
