from django import template
import datetime
from home.models import Reaction,Comments,Page
register = template.Library()

@register.simple_tag
def likes(post_id):
    like = Reaction.objects.filter(post_id = post_id, reaction = True).count()
    return like

@register.simple_tag
def dislikes(post_id):
    dislike = Reaction.objects.filter(post_id = post_id, reaction = False).count()
    return dislike

@register.simple_tag
def comments(post_id):
    comment = Comments.objects.filter(post_id = post_id).count()
    return comment

@register.simple_tag
def totallike(username):
    q = []
    inst = Page.objects.filter(username = username)
    for i in inst:
    	q.append(i.post_id)
    totallike = Reaction.objects.filter(post_id__in = q, reaction = True).count()
    return totallike

@register.simple_tag
def totaldislike(username):
    q = []
    inst = Page.objects.filter(username = username)
    for i in inst:
    	q.append(i.post_id)
    totaldislike = Reaction.objects.filter(post_id__in = q, reaction = False).count()
    return totaldislike

@register.simple_tag
def totalcomment(username):
    q = []
    inst = Page.objects.filter(username = username)
    for i in inst:
    	q.append(i.post_id)
    totalcomment = Comments.objects.filter(post_id__in = q).count()
    return totalcomment