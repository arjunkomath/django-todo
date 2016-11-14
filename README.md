# django-todo
Basic todo app ( https://arcane-sands-10463.herokuapp.com )

## USAGE

### Create (POST): Create a new todo

```
headers : {'Content-Type': 'application/x-www-form-urlencoded'}
POST /api/todo
body: { query : 'todo,tag1,tag2...' }
```

### Read (GET): List todos, all or by id

List all todos - `GET /api/todo`

List todo by id - `GET /api/todo/:id`

### Update (PUT): Update an exsisting todo

```
headers : {'Content-Type': 'application/x-www-form-urlencoded'}
PUT /api/todo:id
body: { query : 'todo,tag1,tag2...' }
```

### Delete (DELETE): Delete todo by id

```
DELETE /api/todo/:id
```
