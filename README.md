# django-next-article-suggestion

Check out my article [Next Article Suggestion in Django](https://ianwaldron.com/blog/next-article-suggestion-in-django/) for more information.

## Overview

The "next_suggestion" Django model manager method produces a "suggestion" for what a user should read next depending upon the context of the article they're already reading.

Specifically, the recommendation engine establishes context across three dimensions: category, tags, and recency.

The manager is located at "core.managers.py."

## Setup

Once you've cloned a local copy of the repo, first create a virtual environment.

```shell
python3 -m venv env
```

This operation might take a few seconds. Once installed, activate the virtual environment.

```shell
source env/bin/activate
```

Next, install the requirements (Django, etc.)

```shell
pip install -r requirements.txt
```

## Migrate Database

The migrations for the three models (Category, Tag, & Article) have already been created. All you need to do is migrate the database.

```shell
python manage.py migrate
```

## Admin

You're almost ready to access the admin portal to begin creating and working with data. First, you need a user account with admin privileges (is_staff=True).

I've created a fixture that will produce a default user so you can get up and running right away. To user this user account, load the fixture into the database.

```shell
python manage.py loaddata users
```

Now start the application on a development server to access the admin portal.

```shell
python manage.py runserver
```

Navigate to the admin login page running on the development server exposed at port 8000.

[admin login](http://127.0.0.1:8000/admin/login)

You may now login with the default user's credentials:
* username: "example"
* password: "not-secure"

From here, you can now create and update objects.

Alternatively, you can load dummy data if you don't wish to do so manually.

```shell
python manage.py loaddata categories tags articles
```

Note: the order the fixtures are in when they're loaded matters due to dependencies.

## Get Suggestions (shell)

Now you're able to test the suggestion engine in a shell environment.

```shell
python manage.py shell
from core.models import Article
```

Now let's get a suggestion. The method has a single positional argument for an article from which to make a suggestion.

```shell
article_1 = Article.objects.first()
article_2 = Article.objects.next_suggestion(article_1)
print(f"'{article_2}' is a suggestion based upon '{article_1}'")
```

Next and with the development sever running, add and update more objects with different types of relationships and see how the recommendations evolve.