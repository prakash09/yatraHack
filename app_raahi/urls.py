from django.conf.urls import patterns, include, url
from .views import *
urlpatterns = [
    url(r'^$',homePage, name='home_page'),
    url(r'^signup/$', userSignup, name='user_signup'),
    url(r'^signin/$', userLogin, name='user_signin'),
    url(r'^user-query/$', userQuery, name='user_query'),
    url(r'^booking/$', newBooking, name='bookings'),
    url(r'^suggestion/$',friendsSuggestion , name='friends_suggestion'),
    url(r'^all/$',allFriends , name='all_friends'),
    url(r'^post/$',postToWall , name='post'),


]
