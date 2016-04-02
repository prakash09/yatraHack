from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpRequest, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.db.models import Prefetch
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import F
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import *
import requests
import facebook
# Create your views here.
#@login_required
def homePage(request):
    return HttpResponse(json.dumps({"msg":"hi ashish"}))

@csrf_exempt
def userSignup(request):
    data = request.POST
    if User.objects.filter(username=data['f_id']).exists():
        user=User.objects.get(username=data['f_id'])
        if user.profile_info.facebook_token:
            return HttpResponse(json.dumps({"user_id":user.id,"status":1}))
        else:
            user.profile_info.facebook_token=data['access_token']
            user.profile_info.link=data['link']
            user.profile_info.save()
            return HttpResponse(json.dumps({"user_id":user.id,"status":1}))
    else:
        user=User.objects.create(first_name=data['first_name'],username=data['f_id'],email="na@abc.in",password="password")
        up=UserProfile()
        up.user=user
        up.facebook_id=data['f_id']
        up.facebook_token=data['access_token']
        up.profile_photo=data['profile_pic']
        up.link=data['link']
        up.save()
        graph = facebook.GraphAPI(up.facebook_token)
#            friends = graph.get_object("me/invitable_friends")
        friends = graph.get_object("me/taggable_friends")
        user_profile=[]
        count=0
        while count<10:
            for i in friends['data']:
                if User.objects.filter(username=i['id']).exists():
                    user=User.objects.get(username=i['id'])
                    user_profile.append(user.profile_info)
                else:
                    try:
                        user=User.objects.create(first_name=i['name'],username=i['id'],email="na@abc.in",password="password")
                    except:
                        break
                    up=UserProfile()
                    up.user=user
                    up.facebook_id=i['id']
                    up.profile_photo=i['picture']['data']['url']
                    up.save()
                    user_profile.append(up)
            count+=1
            if 'next' in friends['paging'] and count<10:
                friends=json.loads(requests.get(friends['paging']['next']).content)
            else:
                break
        up.friends.add(*user_profile)
        up.save()
        return HttpResponse(json.dumps({"user_id":user.id,"status":1}))

def userLogin(request):
    data = request.POST
    if User.objects.filter(email=data['email']).exist():
        user=User.objects.get(email=data['email'])
        return HttpRequest(json.dumps({"user_id":user.id,"status":1}))
    else:
        return HttpRequest(json.dumps({"error":"user does not exist","status":0}))

def userQuery(request):
    data=request.GET
    flight_query=requests.get("https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?apikey=9ZUHucLFNxFisoCMr6HAtGiIFEH9UVuG&origin="+data['source']+"&destination="+data['destination']+"&departure_date="+data['date'])
#    cab_query=request.get("https://api.sandbox.amadeus.com/v1.2/cars/search-airport?apikey=9ZUHucLFNxFisoCMr6HAtGiIFEH9UVuG&location=NCE&pick_up=2016-06-04&drop_off=2016-06-08")
    return HttpResponse(json.dumps({"status":1,"data":json.loads(flight_query.content)}))


import datetime
def newBooking(request):
    data=request.GET
    b=UserBookings(
            user=User.objects.get(id=int(data['user_id'])).profile_info,
            booking_date=datetime.datetime.now(),#datetime.datetime.strptime(data['booking_date'], "%Y-%m-%d %H:%M"),
            journey_date=datetime.datetime.now(),#datetime.datetime.strptime(data['journey_date'], "%Y-%m-%d %H:%M"),
            source=data['source'],
            destination=data['dest'],
            ticket_cost=int(float(data['ticket_cost'])),
            cash_back=50,#int(data['cash_back'])
            )
    b.save()
    return HttpResponse(json.dumps({"status":1,"booking_id":b.id}))


def friendsSuggestion(request):
    data=request.GET
    profile=User.objects.get(id=int(data["user_id"])).profile_info
    travel_companion=[]
    for i in profile.friends.all():
        startdate = datetime.today()
        enddate = startdate + timedelta(days=4)
        if i.bookings.filter(journey_date__range=[startdate, enddate]).count()>0:
            travel_companion.append(i)
    json_resp=[]
    for j in travel_companion:
        new_obj={"user":j.user.first_name,"booking_date":[]}
        for k in j.bookings.all():
            new_obj["booking_date"]=k.json_data
        json_resp.append(new_obj)
    return HttpResponse(json.dumps({"status":1,"booking":json_resp}))

def allFriends(request):
    data=request.GET
    user=User.objects.get(id=int(data['user_id']))
    return HttpResponse(json.dumps({"all":user.profile_info.friends_cashback()}))

def postToWall(request):
    data=request.GET
    user=User.objects.get(id=data['user_id'])
    graph = facebook.GraphAPI(user.profile_info.facebook_token) # Initializing the object
    graph.put_object("me", "feed", message="Posting on my wall! http://codezilla.com/share/503/?token=123sdfsd")
    return HttpResponse(json.dumps({"status":1,"msg":"Posted to wall\n "}))

