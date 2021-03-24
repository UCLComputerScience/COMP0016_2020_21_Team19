---
title: System Design
subtitle:
excerpt: >-
layout: post
---

## System Architecture Diagram

![System Architecture Diagram](../images/design/architecture.png)

## User Sequence Diagrams

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

![User Authentication Sequence Diagram](../images/design/signup.png)

## Class Diagrams (Entity Relationship)

<br>

### Overall
<div class="btn-group">
  <button id="zoomInButton" type="button" class="btn btn-primary">Zoom In</button>
  <button id="zoomOutButton" type="button" class="btn btn-primary">Zoom Out</button>
  <button id="resetButton" type="button" class="btn btn-primary">Reset</button>
</div>
<input id="rangeSlider" class="range-input" type="range" min="1" max="8" step="0.01" value="1">
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
  maxScale: 8,
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