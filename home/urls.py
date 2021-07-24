"""blogapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path,include
from django.conf.urls import url
from home import views
from django.conf.urls import handler404, handler500, handler403, handler400
urlpatterns = [
    url(r'^$',views.landing),
    url(r'^login/$',views.log_in),
    url(r'^register/$',views.register),
    path('verifyemail/<str:key>',views.verifyemail,name = 'verify_email'),
    url(r'changepass$',views.changepass,name = 'forget pass'),
    path('forgetpass/<str:key>',views.forgetpass,name = 'change_forget_pass'),
    url(r'^logout$',views.log_out,name = 'logout'),
    url(r'^dashboard$',views.dashboard,name = 'dashboard'),
    url(r'^dashboard/newpost$',views.newpost,name = 'newpost'),
    url(r'^dashboard/comments$',views.all_comments,name = 'comments'),
    path('post/<str:key>',views.showpost,name = 'showpost'),
    url(r'^dashboard/stats$',views.stats,name = 'stats'),
    path('reaction/<str:key>/like',views.like,name = 'post like'),
    path('reaction/<str:key>/dislike',views.dislike,name = 'post dislike'),
    path('comment/<str:key>',views.comment,name = 'comment'),
    path('comment/<str:key>/delete',views.delete_comment,name = 'delete comment'),
    path('update/<str:key>', views.comment_update,name = 'update comment'),
    path('edit/<str:key>', views.edit_post,name = 'Edit Post'),
    path('category/<str:key>', views.category,name = 'Category'),
    path('user/<str:key>', views.user,name = 'Category'),
]
handler404 = views.handler_404
handler500 = views.handler_500	