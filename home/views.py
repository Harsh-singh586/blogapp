from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Page, Comments, Reaction, Emailverify, Forgetpass
import secrets
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.utils.timezone import now
from django.http import JsonResponse
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
import requests
# Create your views here.

def landing(request):
	if request.user.is_authenticated:
		return redirect('/dashboard')
	food = Page.objects.filter(category = 'Food')
	food = food[0 : min(3, len(food))]
	travel = Page.objects.filter(category = 'Travel')
	travel = travel[0 : min(3, len(travel))]
	technology = Page.objects.filter(category = 'Technology')
	technology = technology[0 : min(3, len(technology))]
	fashion = Page.objects.filter(category = 'Fashion')
	fashion = fashion[0 : min(3, len(fashion))]
	pop_post = Page.objects.filter().distinct('category').order_by('category','reactions').reverse()
	pop_post = pop_post[0 : min(3, len(pop_post))]
	recent = Page.objects.filter().distinct('category').order_by('category','date')
	head = Page.objects.filter().order_by('date').reverse()[0]
	return render(request,'landing.html',context =  {'food' : food, 'tech' : technology, 'travel' : travel, 'post' : recent,'head' : head,'fashion':fashion,'pop_post': pop_post})

def create_key():
    key = secrets.token_urlsafe(10)
    return str(key)

def send_mail(to, subject, content):
	message = Mail(
        from_email='codersintense@gmail.com',
        to_emails= to,
        subject= subject,
        html_content = content)
	sg = SendGridAPIClient('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')
	response = sg.send(message)
	code = response.status_code
	return code

def verifyemail(request, key):
	flag = Emailverify.objects.filter(activation_key = key)
	if flag:
		inst = flag[0]
		username = inst.username
		user = User.objects.filter(username = username)
		if user:
			user = user[0]
			user.is_active = True
			user.save()
			inst.delete()
			return HttpResponse('<center><h1>Email Verified Login</h1><a href="/login">Login</a></center')
	else:
		return HttpResponse('<h1>404</h1>')

def changepass(request):
	if request.method == 'POST':
		email = request.POST['email']
		usr = User.objects.filter(email = email)
		if usr:
			usr = usr[0]
			username = usr.username
			key = create_key() 
			inst = Forgetpass()
			inst.username = username
			inst.verification_key = key 
			inst.save()
			link = 'https://myblogspot.herokuapp.com/forgetpass/'+str(key)
			body =  "<h1>Password Change Request</h1><h3>Click On the following link to change your Password</h3><a href = {l}>Click Here to verify</a>".format(l = link)
			subject = 'Password Change Request'
			status = send_mail(email, subject, body)
			return redirect('/login')

def forgetpass(request,key):
	flag = Forgetpass.objects.filter(verification_key = key)
	if not flag:
		return HttpResponse('<h1>404</h1')
	username = flag[0].username
	usr = User.objects.filter(username = username)
	if usr:
		inst = usr[0]
		if request.method == 'POST':
			password1 = request.POST['password1']
			password2 = request.POST['password2']
			if password1 == password2:
				inst.set_password(password1)
				inst.save()
				flag[0].delete()
				return HttpResponse('<h1>Password Changed Login Now</h1><a href = "/login">Login</a>')
			else:
				messages.info(request,'Password Mismatch')
	return render(request,'changepass.html')

def log_in(request):
	if request.user.is_authenticated:
		return redirect('/dashboard')
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		usr = User.objects.filter(username = username)
		if usr:
			usr = usr[0]
			if usr.is_active == False:
				messages.info(request,'Email Not Verified')
			else:
				login_user = authenticate(request, username=username, password=password)
				print(login_user)
				if login_user:
					login(request, login_user)
					return redirect('/dashboard')
				else:
					messages.info(request, 'Invalid Login')
	return render(request,'login.html')

def log_out(request):
	auth.logout(request)
	return redirect('/login')

def register(request):
	if request.user.is_authenticated:
		return redirect('/dashboard')
	if request.method=="POST":
		first_name = request.POST["name"]
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password1"]
		password2 = request.POST["password2"]
		if password==password2:
			if User.objects.filter(username=username).exists():
				messages.info(request,'username taken')
				return redirect('/register')
			else:
				user = User.objects.create_user(username = username, password=password,first_name=first_name,is_active = False,email = email)
				key = create_key()
				inst = Emailverify()
				inst.username = username
				inst.activation_key = key
				inst.save()
				print('127.0.0.1/verifyemail/'+str(key))
				link = 'https://myblogspot.herokuapp.com/verifyemail/'+str(key)
				body =  "<h1>You are On way! Let's Confirm Your Email Address</h1><h3>Click On the following link to verify your Email</h3><a href = {l}>Click Here to verify</a>".format(l = link)
				subject = 'Verify Your Email'
				status = send_mail(email, subject, body)
				user.save()
				return HttpResponse('<center><h1>Email Sent for Verification Verify your Email and Login</h1></center>')
		else:
			messages.info(request,'Password Mismatch')
			return redirect('/register')
	return render(request,'register.html')

@login_required(login_url = '/login')
def dashboard(request):
	post = Page.objects.filter(username = request.user.username)
	return render(request,'dashboard.html',context = {'post' : post})

@login_required(login_url = '/login')
def newpost(request):     
	if request.method == 'POST':
		heading = request.POST['heading'] 
		cont = request.POST['cont']
		keyword = request.POST['keyword']
		category = request.POST['category']
		img = request.POST['get_img']
		print(img)
		print(type(img))
		key = create_key()
		d = now()
		inst = Page()
		inst.post_id = key 
		inst.headline = heading
		inst.content = cont
		inst.date = now()
		inst.likes = 0
		inst.dislikes = 0
		inst.views = 0
		inst.comments = 0
		inst.username = request.user.username
		inst.category = category
		inst.img = img
		inst.save()
	return render(request,'newpost.html') 

def showpost(request,key):
	flag = Page.objects.filter(post_id = key)
	if flag:
		post = Page.objects.get(post_id = key)
		like = len(Reaction.objects.filter(post_id = key, reaction = True))
		dislike = len(Reaction.objects.filter(post_id = key, reaction = False))
		comments = Comments.objects.filter(post_id = key)
		react = None
		if request.user.is_authenticated:
	 	    react = Reaction.objects.filter(post_id = key, username = request.user.username)
	 	    if react:
	 	    	react = Reaction.objects.get(post_id = key, username = request.user.username)
	 	    else:
	 	    	react = None
		return render(request,'showpost.html',context = {'post' : post,'react' : react,'likes':like,'dislikes':dislike, 'comments' : comments})
	else:
		return HttpResponse('404')

@login_required(login_url = '/login')
def stats(request):
	total_likes = 0
	total_dislikes = 0
	total_comments = 0
	post_detail = requests.get('http://127.0.0.1:8000/api/apikey/BSTmRn31WZjMUxjL7Zf3dsqK0p0/statsbypost').json()
	return render(request,'stats.html',context={'total_likes':total_likes,'total_dislikes':total_dislikes,'total_comments':total_comments, 'post_detail' : post_detail})

@login_required(login_url = '/login')
def like(request, key):
	if request.method == "GET":
		flag = Reaction.objects.filter(username = request.user.username, post_id = key)
		page = Page.objects.get(post_id = key)
		if not flag:
			inst = Reaction()
			inst.username = request.user.username
			inst.reaction = True
			inst.post_id = key
			inst.save()
			page.reactions = page.reactions + 1
			page.save()
		else:
			inst = Reaction.objects.get(username = request.user.username, post_id = key)
			if inst.reaction == True:
				inst.delete()
				page.reactions = page.reactions - 1
				page.save()
			elif inst.reaction == False:
				inst.reaction = True
				inst.save()
	likes = len(Reaction.objects.filter(post_id= key, reaction = True))
	dislikes = len(Reaction.objects.filter(post_id= key, reaction = False))
	return JsonResponse({"likes": likes,"dislikes" : dislikes}, status=200)

@login_required(login_url = '/login')
def dislike(request, key):
	if request.method == "GET":
		flag = Reaction.objects.filter(username = request.user.username, post_id = key)
		page = Page.objects.get(post_id = key)
		if not flag:
			inst = Reaction()
			inst.username = request.user.username
			inst.reaction = False
			inst.post_id = key
			inst.save()
			page.reactions = page.reactions + 1
			page.save()
		else:
			inst = Reaction.objects.get(username = request.user.username, post_id = key)
			if inst.reaction == False:
				inst.delete()
				page.reactions = page.reactions - 1
				page.save()
			elif inst.reaction == True:
				inst.reaction = False
				inst.save()
	likes = len(Reaction.objects.filter(post_id= key, reaction = True))
	dislikes = len(Reaction.objects.filter(post_id= key, reaction = False))
	return JsonResponse({"likes": likes,"dislikes" : dislikes}, status=200)

@login_required(login_url = '/login')
def comment(request, key):
	inst = Comments()
	page = Page.objects.get(post_id = key)
	if request.method == "GET":
		comment = request.GET['comment']
		inst.username = request.user.username
		inst.post_id = key
		k = create_key() 
		inst.comment_id = k 
		inst.comments = comment
		inst.save()
		r = page.reactions
		print(r)
		page.reactions =  r + 1
		page.save()
	len_comment = len(Comments.objects.filter(post_id = key))
	return JsonResponse({"len_comment" : len_comment}, status = 200)

@login_required(login_url = '/login')
def delete_comment(request, key):
	if request.method == "GET":
		inst = Comments.objects.get(comment_id = key)
		post_id = inst.post_id
		inst.delete()
		page = Page.objects.get(post_id = post_id)
		page.reactions = page.reactions - 1
		page.save()
	len_comment = len(Comments.objects.filter(post_id = post_id))
	return JsonResponse({'len_comment' : len_comment}, status = 200)

@login_required(login_url = '/login')
def comment_update(request, key):
	comment = Comments.objects.filter(post_id = key)
	return render(request, 'comment_update.html', {'comment' : comment})

'''@login_required(login_url = '/login')
def stats(request):
	username = request.user.username
	posts = Page.objects.filter(username = username)
	return render(request, 'stats.html', {'posts' : posts})
'''
@login_required(login_url = '/login')
def edit_post(request, key):
	post = Page.objects.get(post_id = key)
	if request.method == 'POST':
		heading = request.POST['heading'] 
		cont = request.POST['cont']
		keyword = request.POST['keyword']
		category = request.POST['category']
		img = request.POST['get_img']
		inst = Page.objects.get(post_id = key)
		inst.headline = heading
		inst.content = cont
		inst.username = request.user.username
		inst.category = category
		inst.img = img
		inst.save()
	return render(request, 'edit.html', {'post' : post})

def category(request, key):
	post = Page.objects.filter(category = key)
	if post:
	    post = post[0 : min(9, len(post))]
	return render(request, 'category.html', {'post' : post, 'key' : key})

def user(request, key):
	print('s')
	post = Page.objects.filter(username = key)
	l = post.count()
	if post:
	    post = post[0 : min(9, l)]
	return render(request, 'category.html', {'post' : post, 'key' : key})

@login_required(login_url = '/login')
def all_comments(request):
	username = request.user.username
	postid = Page.objects.filter(username = username).values_list('post_id')
	postid_lst =  [i[0] for i in postid]
	comments = Comments.objects.filter(post_id__in = postid_lst)
	return render(request, 'allcomments.html', {'comments':comments})

def handler_404(request, exception):
	print('dcccccccc')
	html = '<center><h1>Either you Did a Mistake or Me</h1><h1>Explore me more <a href = "/">Explore me<a></h1></center>'
	return HttpResponse(html)

def handler_500(request):
	html = '<center><h1>Either you Did a Mistake or Me</h1><h1>Explore me more <a href = "/">Explore me<a></h1></center>'
	return HttpResponse(html)