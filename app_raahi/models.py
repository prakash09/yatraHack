from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template import loader
from django.db.models import signals
from django.db.models.signals import post_save
import facebook
import requests
import json
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile_info")
    profile_photo=models.TextField(max_length=500,null=True,blank=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    facebook_token = models.TextField(max_length=1000, blank=True, null=True)
    link=models.TextField(max_length=500,null=True, blank=True)
    friends = models.ManyToManyField("self", symmetrical=False, related_name='friends_list',blank=True)

    def __unicode__(self):
        return self.user.first_name

    def friends_cashback(self):
        friends=self.friends.all()
        data=[]
        for i in friends:
            cb=0
            for j in i.bookings.all():
                cb+=j.cash_back
            data.append({"name":i.user.first_name,"photo_url":i.profile_photo,"total_bookings":i.bookings.all().count(),"cash_back":cb})
        return data

class UserBookings(models.Model):
    user=models.ForeignKey(UserProfile, related_name="bookings")
    booking_date=models.DateTimeField()
    journey_date=models.DateTimeField()
    source=models.CharField(max_length=255)
    destination=models.CharField(max_length=255)
    ticket_cost=models.IntegerField(default=0)
    cash_back=models.IntegerField(default=0)
    def __unicode__(self):
        return self.user.user.first_name
    def json_data(self):
        return {"journey_date":str(self.journey_date), "ticket_cost":self.ticket_cost}
