# Django Blog App

A small but complete blog application built with Django, demonstrating
models, class-based views, forms, authentication, and templates.

## What it does

- User registration and login/logout (Django's built-in auth)
- Create, edit, and delete blog posts (only the author can edit/delete their own)
- View a paginated list of all posts
- Comment on posts (no login required to comment)
- Django admin panel for managing posts and comments

## How to run

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for the /admin/ panel
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Concepts this demonstrates

- **Models & relationships**: `Post` has a `ForeignKey` to Django's `User`;
  `Comment` has a `ForeignKey` to `Post`.
- **Class-based views**: `ListView`, `DetailView`, `CreateView`,
  `UpdateView`, `DeleteView` instead of writing repetitive function views.
- **Authentication & permissions**: `LoginRequiredMixin` to require login,
  and a custom `AuthorRequiredMixin` so only the post's author can edit or
  delete it.
- **Forms**: `ModelForm` for posts and comments, plus a custom
  `UserCreationForm` subclass for registration.
- **Templates & template inheritance**: a shared `base.html` with template
  blocks extended by each page.

## Project structure

```
django_blog/
├── manage.py
├── blogproject/         # project settings, root urls.py
├── blog/                 # the app
│   ├── models.py         # Post, Comment
│   ├── views.py          # CRUD views + registration
│   ├── forms.py           # PostForm, CommentForm, RegisterForm
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       ├── blog/         # base, list, detail, form, delete-confirm
│       └── registration/ # login, register
└── requirements.txt
```

## Note on the secret key

`settings.py` ships with a Django-generated development secret key, which is
fine for local learning/demo use. Never reuse a checked-in secret key in a
real production deployment — generate a new one and load it from an
environment variable instead.

## Ideas to extend it (good for interview talking points)

- Add categories/tags for posts
- Add a "like" feature
- Switch to Django REST Framework to expose the blog as an API
- Deploy it (Render, Railway, or PythonAnywhere all have free tiers)
