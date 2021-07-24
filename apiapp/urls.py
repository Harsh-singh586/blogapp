from django.contrib import admin
from django.urls import path
from django.urls import path,include
from django.conf.urls import url
from apiapp import views
from django.conf.urls import handler404, handler500, handler403, handler400
urlpatterns = [
    url(r'^$',views.apidoc, name = 'api_serv'),
    path('getkey',views.getkey,name = 'get_key'),
    path('verify/<str:apikey>',views.verifykey,name = 'verify_key'),
    path('apikey/<str:apikey>/post/category/<str:category>',views.post_collection,name = 'Post_by Category'),
    path('apikey/<str:apikey>/post/user/<str:username>',views.post_user,name = 'Post_by user'),
    path('apikey/<str:apikey>/post/recent',views.recent_post, name = 'recent_post'),
    path('apikey/<str:apikey>/post/popular',views.popular_post, name = 'popular_post'),
    path('apikey/<str:apikey>/stats',views.stats, name = 'stats_api'),
    path('apikey/<str:apikey>/statsbypost',views.stats_post, name = 'stats_post_api')
    ]