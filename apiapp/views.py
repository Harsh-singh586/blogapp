from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from apiapp.models import Apikey
import secrets
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apiapp.serializers import PostSerializer
from home.models import Page, Reaction, Comments
# Create your views here.
def create_key():
    key = secrets.token_urlsafe(20)
    return str(key)

def apidoc(request):
	flag = Apikey.objects.filter(username = request.user.username)
	if flag:
		dic = {'apikey': flag[0]}
	else:
		dic = {'apikey' : None}
	return render(request, 'apidoc.html', dic)

def getkey(request):
	if request.method == "GET":
		flag = Apikey.objects.filter(username = request.user.username)
		if not flag:
			inst = Apikey()
			inst.username = request.user.username
			apikey = create_key()
			inst.apikey = apikey
			inst.save()
			print(apikey)
			apikey = json.dumps(apikey)
			return JsonResponse({"apikey": apikey}, status=200)
		else:
			return HttpResponse(request.user.username)

@api_view(['GET'])
def verifykey(request, apikey):
	if request.method == 'GET':
		flag = Apikey.objects.filter(apikey = apikey)
		if flag:
			username = flag[0].username
			res = {'username' : username}
			return Response(res)
		else:
			res = {'error' : 'Invalid Key'}
			return Response(res)

@api_view(['GET'])
def post_collection(request, apikey, category):
    if request.method == 'GET':
    	flag = Apikey.objects.filter(apikey = apikey)
    	if flag:
    		posts = Page.objects.filter(category = category)
    		serializer = PostSerializer(posts, many=True)
    		return Response(serializer.data)
    	return Response({'error':'Invalid API Key'})

@api_view(['GET'])
def post_user(request, apikey, username):
    if request.method == 'GET':
    	flag = Apikey.objects.filter(apikey = apikey)
    	if flag:
    		posts = Page.objects.filter(username = username)
    		serializer = PostSerializer(posts, many=True)
    		return Response(serializer.data)
    	return Response({'error':'Invalid API Key'})

@api_view(['GET'])
def recent_post(request, apikey):
	if request.method == 'GET':
		flag = Apikey.objects.filter(apikey = apikey)
		if flag:
			posts = Page.objects.filter().order_by('date').reverse()[0 : 5]
			serializer = PostSerializer(posts, many = True)
			return Response(serializer.data)
		return Response({'error':'Invalid API Key'})

@api_view(['GET'])
def popular_post(request, apikey):
	if request.method == 'GET':
		flag = Apikey.objects.filter(apikey = apikey)
		if flag:
			posts = Page.objects.filter().order_by('reactions').reverse()[0 : 5]
			serializer = PostSerializer(posts, many = True)
			return Response(serializer.data)
		return Response({'error':'Invalid API Key'})

@api_view(['GET'])
def stats(request, apikey):
	if request.method == 'GET':
		flag = Apikey.objects.filter(apikey = apikey)
		if flag:
			username = flag[0].username
			postid = Page.objects.filter(username = username).values_list('post_id')
			postid_lst =  [i[0] for i in postid]
			like = Reaction.objects.filter(post_id__in = postid_lst, reaction = True).count()
			dislike = Reaction.objects.filter(post_id__in = postid_lst, reaction = False).count()
			comment = Comments.objects.filter(post_id__in = postid_lst).count()
			return Response({'likes' : like, 'dislike' : dislike, 'comment' : comment})
		return Response({'error' : 'Invalid API Key'})


@api_view(['GET'])
def stats_post(request, apikey):
	if request.method == 'GET':
		flag = Apikey.objects.filter(apikey = apikey)
		if flag:
			username = flag[0].username
			postid = Page.objects.filter(username = username).values_list('post_id')
			postid_lst = [i[0] for i in postid]
			data = []
			print('f')
			for j in postid_lst:
				like = Reaction.objects.filter(post_id = j, reaction = True).count()
				dislike = Reaction.objects.filter(post_id = j, reaction = False).count()
				comment = Comments.objects.filter(post_id = j).count()
				headline = Page.objects.get(post_id = j).headline
				temp_dict = {'post_id' : j, 'Headline' : headline, 'Likes' : like, 'Dislikes' : dislike, 'Comments' : comment}
				data.append(temp_dict)
			print('s')
			return Response(data)
		else:
			return Response({'error' : 'Invalid API Key'})