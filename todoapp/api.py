from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
import json, datetime

from todoapp.models import *

def todo(request):
	query = request.GET.get('query', '');
	if query != '': 
		query = query.split(',')
		pub_date = datetime.datetime.now()

		todo = Todo()
		todo.todo_text = query[0]
		todo.created_at = pub_date
		todo.save()

		del query[0]

		for tag in query:
			if tag.strip() == '':
				continue
			try:
				t = Tag.objects.get(slug=tag)
				todo.tags.add(t)
			except Tag.DoesNotExist:
				t=Tag()
				t.slug = tag
				t.save()
				todo.tags.add(t)

		response = json.dumps({'query': query, 'success': True})
		return HttpResponse(response, content_type="application/json")
	else:
		keyword = request.GET.get('keyword', '');

		if keyword != '':
			data = Todo.objects.order_by('-created_at').filter(Q(tags__slug__contains=keyword) | Q(todo_text__contains=keyword))
		else:
			data = Todo.objects.order_by('-created_at').all()

		tags_data = {}

		for t in data:
			tags = t.tags.all()
			tags_data[t.pk] = [];
			for tag in tags:
				tags_data[t.pk].append(tag.slug)

		list = {}
		list['todos'] = json.loads(serializers.serialize("json", data))
		list['tags'] = tags_data
		response = json.dumps(list)
		return HttpResponse(response, content_type="application/json")
