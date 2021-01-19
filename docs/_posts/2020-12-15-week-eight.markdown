---
layout: post
title:  "Week Eight: Django Forms"
date:   2020-12-15
categories: backend, forms
name: Team 19
---

This week, our primary focus has been to continue our implementation of backend functionalities for the templates that we had already established in the last couple of weeks.

We decided that among the most important functionalities at the moment was the ability to collect responses. Hence, the three of us went about attempting to integrate forms in Django...

## Django Forms

### Research

As is the case with the majority of the functionalities that the three of us are implementing, none of us have had any prior experience dealing with online forms. Hence, the three of us set about compiling a list of tutorials and sources detailing how we might go about implementing them in Django.

We came across a few very good sources, notably [this one from simpleisbetterthancomplex.com](https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html), teaching us how to implement forms using the existing Django Forms API, which appeared to be exactly what we needed to get started.

### Implementation

#### HTML Base Classes

Reading through numerous tutorials gave us much-needed guidance about how the rendering process actually took place in Django. Given that our forms were going to be dynamic in the sense that Surveyors would be able to create as many questions as they like of whichever response type that we allowed them, we knew that we couldn't rely on a static html template for our forms (even if, as our client had informed us, the majority of the time there would only be 5-10 questions on the form).

Looking to resolve this issue, we soon realised that (somewhat) like other languages, HTML had a functionality similar to inheritance in Object-Oriented Programming (OOP) which allowed you to define base classes in html, which other HTML templates could then extend, and choose to "override" some regions within, like so:

**base.html**
```html
{% load static %}<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

    <title>Activity League - Dashboard</title>

    <!-- Bootstrap core CSS -->
    <link href="{% static 'bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="{% static 'bootstrap/css/dashboard.css' %}" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">Activity League</a>
      <ul class="navbar-nav px-3">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#">
              {{user}}<span data-feather="user"></span>
          </a>
          <div class="dropdown-menu">
            <a class="dropdown-item" href="../login">Sign Out</a>
          </div>
        </li>
      </ul>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
                {% block sidebar %}
                {% endblock %}
            </ul>
          </div>
        </nav>


        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
            {% block content %}
            {% endblock %}
        </main>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="{% static 'bootstrap/js/bootstrap.min.js' %}"></script>

    <!-- Icons -->
    <script src="https://unpkg.com/feather-icons/dist/feather.min.js"></script>
    <script>
      feather.replace()
    </script>

    {% block scripts %}
    {% endblock %}
  </body>
</html>
``` 

In addition to forms, we realised that this was something that we could and definitely should implement for the rest of our html templates, given they shared the taskbar on the left, the same page structure and at least a few of the same scripts. Hence, we implemented this as an experiment ahead of our base forms implementation, which ended up being a success.

#### Forms API

After this we continued the implementation of forms using the Forms API, implementing the **factory** design pattern to create forms to be rendered:

```python3
QuestionFormset = modelformset_factory(
    Question,
    fields=('link', 'description'),
    extra=4,
    widgets={
        'description': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Question here'
            }
        ),
        'link': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'URL (optional)'
            }
        ),
    }
)
```

Using the Forms API, we submitted forms through **POST** requests, using csrf tokens to authenticate ourselves.

For the time being, we left this as a predominantly static implementation knowing that we were going to need to make further changes to the structure of our database and the location of our database (given we had planned on dockerizing the application). Connecting Django to my local running instance of PostgreSQL though, we tested that we were able to both create and submit forms. 

## Customised URLs

This week we also sought after creating nice URLs for each and every user, such as the customised urls that bloggers on [medium.com](https://www.medium.com/) had. We implemented this using changes to our urls.py file, where we took to allowing each surveyor and respondent to have their own customised URL in the form of surveyor/respondent@(customised ID)/(page). After injecting this ID into the html, we accomplished the desired result:

![Custom URL](/COMP0016_2020_21_Team19/assets/custom-url.png)

## Next Steps

Before we begin working on scaling the backend implementation any further, we have decided that given we are going to be hosting the application eventually on Linode, that it would make a lot of sense to dockerize the application whilst we can to ensure that the application runs as smoothly as it does on Linode as it does locally.

See you next week!