---
title: Implementation
layout: post
toc: true
---

## Django
Activity League has been developed using Django. Django proved to be a very good choice for the development of our web app, as it handled standard cases of functionalities
that would need to be implemented in our platform by default (for example, the creation and validation of forms). Moreover, Django has its own ORM (Object-Relational Mapper) which completely
handles the relationship between the classes that we defined as our project and the relations in our PostgreSQL database.

Activity League has been programmed to follow Django's file-structure convention and default Model View Template implementation. Django breaks down a project into applications. Each 
generated application has a models.py file containing the classes to be used in that application (translated to relations in the database by the ORM), a views.py file containing view functions
which map web requests to web responses and plenty of flexibility when writing control logic. For each app that we defined in the project, we created a utils.py file containing the vast majoroity
of the logic and utility functions associated with each of our view functions.

Applications that are involved with pages that create and submit forms, such as the new task page and pages allowing you to add/remove people from groups and organisations also have a dedicated
forms.py file. This file leverages the existing Django Forms API and contains the structure and content of the forms that are used in each of these views.

<div id="carouselDjango" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselDjango" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselDjango" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselDjango" data-bs-slide-to="2" aria-label="Slide 3"></button>
    <button type="button" data-bs-target="#carouselDjango" data-bs-slide-to="3" aria-label="Slide 4"></button>
    <button type="button" data-bs-target="#carouselDjango" data-bs-slide-to="4" aria-label="Slide 5"></button>
    <button type="button" data-bs-target="#carouselDjango" data-bs-slide-to="5" aria-label="Slide 6"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../images/design/django/1.png" class="d-block w-100" alt="Slide 1">
    </div>
    <div class="carousel-item">
      <img src="../images/design/django/2.png" class="d-block w-100" alt="Slide 2">
    </div>
    <div class="carousel-item">
      <img src="../images/design/django/3.png" class="d-block w-100" alt="Slide 3">
    </div>
    <div class="carousel-item">
      <img src="../images/design/django/4.png" class="d-block w-100" alt="Slide 4">
    </div>
    <div class="carousel-item">
      <img src="../images/design/django/5.png" class="d-block w-100" alt="Slide 5">
    </div>
    <div class="carousel-item">
      <img src="../images/design/django/6.png" class="d-block w-100" alt="Slide 6">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselDjango" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselDjango" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

## Bootstrap
To ensure that our application was responsive to changes in the screen size and devices using it, we used the frontend framework Bootstrap when creating our HTML templates. Consequently, the web application is optimised for specific devices when using it. For example, logging in to Activity League on an iPhone will hide our sidebar menu and open it on click, with a smooth transition animation, whereas when viewed on desktop, it remains stuck to the left hand side of the page.

This was an important consideration for us, given that our dashboard is feature and content heavy, and without the ability to restyle the layout by device, our web app would have been virtually unusable on smaller devices.

<div id="carouselBootstrap" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselBootstrap" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselBootstrap" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselBootstrap" data-bs-slide-to="2" aria-label="Slide 3"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../images/design/bootstrap/1.png" class="d-block w-100" alt="Slide 1">
    </div>
    <div class="carousel-item">
      <img src="../images/design/bootstrap/2.png" class="d-block w-100" alt="Slide 2">
    </div>
    <div class="carousel-item">
      <img src="../images/design/bootstrap/3.png" class="d-block w-100" alt="Slide 3">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselBootstrap" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselBootstrap" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

## Database
All data stored by Activity League lies in a PostgreSQL database. PostgreSQL was a particularly suitable choice for Activity League, given there was extensive literature and resources available on the Django documentation on integrating the two of them. Our data also fit the relational model very nicely given the structure of our data, and the fact that lots of the functionalities required could be implemented using small, structured SQL queries. Conveniently, PostgreSQL was also open source. This stands in contrast to other popular databases including MongoDB, which was a paid alternative.

As mentioned in the previous section, Django's ORM handled the translation between models (classes) defined specific to Activity League to PostgreSQL tables, where one model defined corresponded to one table.

## Docker
To ensure the easy deployment of Activity League, we decided to dockerise the entire application. Docker is a containerisation service - allowing for software to be distributed in the form of packages called containers. Containers allowed developers to isolate the development of an app from its local environment. This is particularly useful in deployment, as it means that theoretically, any system with docker installed could simply pull the Activity League container and run it on their system without dependency version conflicts (dependencies and versions are specified in the container).

Given Activity League was going to be deployed on a Linode server, Docker's containerisation system also likely saved a great amount of time debugging features that worked locally but didn't work on the server, which allowed us to further refine and implement new functionalities to our solution.

![Docker](../images/design/docker.png)

## Linode
Activity League is currently deployed on a Linode server with 1 core, 1GB of RAM and 25GB of storage for a total cost of $5 per month. Linode was selected out of client preference, but was a convenient choice for the project deployment given its simplicity to setup.

![Linode](../images/design/linode.png)

As part of a continuous deployment practice, Activity League makes use of WatchTower on the Linode server. Every time a new commit is made to the the main branch, GitHub Actions runs our tests and if they pass, builds a new Docker image hosted on GitHub packages, which WatchTower looks for. WatchTower is configured to probe the project repository every 60 seconds, and if it detects a newer edition of the image being hosted by GitHub Packages, it takes the old version down and deploys the new image automatically.

The database state is separate from this image - it is a persistent volume stored on the Linode server, meaning that we can continue merging pull requests in the main repository (assuming there were no changes to the structure of the database) without having to repopulate the database each time that it was built. Hence, each time that we pushed to the main branch, we would see the latest version of the app deployed to the server in under two minutes.

## Design Patterns

### Model View Template
By default, Django formats its files in accordance with the principles of the MVT design pattern (each application have models.py, views.py and template files associated with them). Our solution has been developed in extension of thes principles which nicely decouples the templates from the views, subsequently making editing specific pages a lot easier.

The design pattern is very similar to the Model View Controller pattern, which separates the models from the views with the controller (housing all of the control logic) as the middle man. This design pattern was an option that we considered given it would have made the flow easier to understand. However, we decided that the MVT template was the optimal choice as the controller is managed by Django itself (controlling The interactions between the models and the view), making an additional implementation unnecessary.

MVT allows Activity League to be easily scalable: the addition of a new page simply requires the creation of a new template, a URL being added and a single function being written within the application to render the newly defined template. We hope that in future, our design choice here significantly speeds the process by which developers may add new pages and functionalities to Activity League.

### Adapter
During the invitation processs (by email), Activity League uses two dependencies: django-invitations (takes care of the email invitations) and django-allauth (takes care of secure user authentication). As Activity League is invite-only and django-allauth doesn't support customisation of signup methods (signup is either closed or it isn't), we implemented the adapter design pattern to change the signal that was being passed from django-inviations to django-allauth. This allows us to selectively open the signup if a user is creating an organisation, but closes it off otherwise.

