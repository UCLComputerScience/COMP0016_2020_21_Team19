---
title: System Design
layout: post
toc: true
---

## System Architecture Diagram

<br>

There are two types of users for our application: `Surveyor`s (those asking the questions) and `Respondent`s (those responding to the questions). Both of these users follow the same general flow throughout the program: they sign in from their device and make requests to our (dockerised) Django application, currently deployed on a Linode Server.

Our PostgreSQL database is not depicted as a part of the diagram. The reason for this is that we've stored the contents of the database as a persistent volume on the Linode server which is referred to by our dockerised app.

<br>

![System Architecture Diagram](../images/design/architecture.png)

## User Sequence Diagrams

<br>

Activity League has a large number of functionalities available to the end user. To help understand how each of these functionalities work in sequence, we've added the following sequence diagrams with functionalities described by page below.

<div id="carouselSequence" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselSequence" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselSequence" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselSequence" data-bs-slide-to="2" aria-label="Slide 3"></button>
    <button type="button" data-bs-target="#carouselSequence" data-bs-slide-to="3" aria-label="Slide 4"></button>
    <button type="button" data-bs-target="#carouselSequence" data-bs-slide-to="4" aria-label="Slide 5"></button>
    <button type="button" data-bs-target="#carouselSequence" data-bs-slide-to="5" aria-label="Slide 6"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../images/design/sequence/1.png" class="d-block w-100" alt="Slide 1">
    </div>
    <div class="carousel-item">
      <img src="../images/design/sequence/2.png" class="d-block w-100" alt="Slide 2">
    </div>
    <div class="carousel-item">
      <img src="../images/design/sequence/3.png" class="d-block w-100" alt="Slide 3">
    </div>
    <div class="carousel-item">
      <img src="../images/design/sequence/4.png" class="d-block w-100" alt="Slide 4">
    </div>
    <div class="carousel-item">
      <img src="../images/design/sequence/5.png" class="d-block w-100" alt="Slide 5">
    </div>
    <div class="carousel-item">
      <img src="../images/design/sequence/6.png" class="d-block w-100" alt="Slide 6">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselSequence" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselSequence" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>


## User Authentication Sequence Diagram

<br>

After receiving an invite, there are two ways that a user can sign up to Activity League:

1. The user could sign up regularly using the Sign Up form. If the user has accessed /accounts/signup, this means that they have been invited or are creating an organisation. Submitting this form via a `POST` request (assuming that the form validates) shall cause the backend to create a new associated user object and return a redirect to the user's dashboard.
2. The user could sign up using Google SSO. If the user chooses to sign up using SSO, Activity League makes an authentication request to Google. If the authentication is successful, the Activity League backend will create the associated user object associated with the new user and redirect them to their dashboard.


![User Authentication Sequence Diagram](../images/design/signup.png)

<br>

## Class Diagrams (Entity Relationship)

<br>

### Overall

<br>

For a better understanding of the entity relations of the system, zoom in and out of the entity relationship diagram below.

<div class="btn-group">
  <button id="zoomInButton" type="button" class="btn btn-primary">Zoom In</button>
  <button id="zoomOutButton" type="button" class="btn btn-primary">Zoom Out</button>
  <button id="resetButton" type="button" class="btn btn-primary">Reset</button>
</div>
<input id="rangeSlider" class="range-input" type="range" min="0.1" max="8" step="0.01" value="1">
<div class="border border-3 border-dark mt-3">
  <img id="overall-class-diagram" src="../images/design/overall.svg" alt="Overall class diagram">
</div>

<script src="https://cdn.jsdelivr.net/npm/@panzoom/panzoom@4.3.2/dist/panzoom.min.js"></script>
<script>
const img = document.getElementById('overall-class-diagram');
const zoomInButton = document.getElementById('zoomInButton');
const zoomOutButton = document.getElementById('zoomOutButton');
const resetButton = document.getElementById('resetButton');
const rangeSlider = document.getElementById('rangeSlider');
const panzoom = Panzoom(img, {
  minScale: 0.1,
  maxScale: 8
  //contain: 'outside'
})
zoomInButton.addEventListener('click', (event) => {
  panzoom.zoomIn();
  rangeSlider.value = panzoom.getScale();
})
zoomOutButton.addEventListener('click', (event) => {
  panzoom.zoomOut();
  rangeSlider.value = panzoom.getScale();
})
resetButton.addEventListener('click', (event) => {
  panzoom.reset();
  rangeSlider.value = panzoom.getScale();
})
rangeSlider.addEventListener('input', (event) => {
  panzoom.zoom(event.target.valueAsNumber)
})
img.parentElement.addEventListener('wheel', (event) => {
  panzoom.zoomWithWheel(event);
  rangeSlider.value = panzoom.getScale();
})
</script>

<br>

### App-specific

<br>

For each app in our Django project (Surveyor, Respondent, Core and Authentication), we've included an application-specific entity relationship diagram below.

<div id="carouselClassDiagrams" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselClassDiagrams" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselClassDiagrams" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselClassDiagrams" data-bs-slide-to="2" aria-label="Slide 3"></button>
    <button type="button" data-bs-target="#carouselClassDiagrams" data-bs-slide-to="3" aria-label="Slide 4"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../images/design/class-diagrams/1.png" class="d-block w-100" alt="Slide 1">
    </div>
    <div class="carousel-item">
      <img src="../images/design/class-diagrams/2.png" class="d-block w-100" alt="Slide 2">
    </div>
    <div class="carousel-item">
      <img src="../images/design/class-diagrams/3.png" class="d-block w-100" alt="Slide 3">
    </div>
    <div class="carousel-item">
      <img src="../images/design/class-diagrams/4.png" class="d-block w-100" alt="Slide 4">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselClassDiagrams" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselClassDiagrams" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>