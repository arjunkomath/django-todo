from django.db import models

class Tag(models.Model):
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.slug

class Todo(models.Model):
    todo_text = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name="tag")
    created_at = models.DateTimeField('date published')

    def __str__(self):              
        return self.todo_text
