from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed,QueryDict
from django.core import serializers
from django.db.models import Q
import json, datetime

from todoapp.models import *

def todo(request, id = None):

	# read and read by id, @return json
	if request.method == 'GET':

		if id != None:
			try:
				t = Todo.objects.get(pk=id)
				res = serializers.serialize("json", [t])
				return HttpResponse(res, content_type="application/json")
			except Todo.DoesNotExist:
				response = json.dumps({'errors': ['No Items found'], 'success': False})
				return HttpResponse(response, content_type="application/json")

		keyword = request.GET.get('keyword', '')

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

	# create, @return json
	elif request.method == 'POST':

		query = request.POST.get('query', '');

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
			return HttpResponseBadRequest('Query missing')

	# delete, @return json
	elif request.method == 'DELETE':
		if id == None:
			return HttpResponseBadRequest('ID missing')
		else:
			try:
				t = Todo.objects.get(pk=id)
				t.delete()
				response = json.dumps({'message': 'Item has been deleted', 'success': True})
				return HttpResponse(response, content_type="application/json")
			except Todo.DoesNotExist:
				response = json.dumps({'errors': ['No Items found'], 'success': False})
				return HttpResponse(response, content_type="application/json")

	# delete, @return json
	elif request.method == 'PUT':
		if id == None:
			return HttpResponseBadRequest('ID missing')
		else:
			request.PUT = QueryDict(request.body)
			query = request.PUT.get('query', '');
			if query != '':
				query = query.split(',')

				try:
					todo = Todo.objects.get(pk=id)
					todo.todo_text = query[0]
					todo.tags.clear()
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

					response = json.dumps({'message': 'Item has been updated', 'success': True})
					return HttpResponse(response, content_type="application/json")
				except Todo.DoesNotExist:
					response = json.dumps({'errors': ['No Items found'], 'success': False})
					return HttpResponse(response, content_type="application/json")

			else:
				return HttpResponseBadRequest('Query missing')

	else:
		return HttpResponseNotAllowed('Method not allowed')
