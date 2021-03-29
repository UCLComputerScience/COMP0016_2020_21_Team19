---
title: Testing
layout: post
toc: true
---

## Testing Strategy

<br>

Testing is an incredibly important part of development as it provides us, developers, with confidence that our code does what it is supposed to do. We've taken this message to heart and have put in the hours to ensure not only that our tests cover our code to a very high standard, but have used writing tests as an opportunity to **document** behaviours of our web app which otherwise would have been nontrivial. We're confident that in our tests, developers looking to extend our application will have a valuable resource.

<br>

## Unit Testing

<br>

We conducted unit testing for the following reasons:

1. They provide us with confidence that the subcomponents of our solution work correctly.

2. Unit tests **tell us if we've broken something later on in the development process** during refactoring or whilst adding a new feature. 

3. They are an opportunity to document the micro-behaviour of our solution. 

4. Assistance in debugging: a failing test is a great way to isolate buggy behaviour.

Accordingly, we implemented unit testing before we attempted any other kind of testing so that we could completely automate its execution and make it part of our Continuous Integration/Continuous Deployment workflow.

Our implementation of unit tests follows the convention defined in the [django docs](https://docs.djangoproject.com/en/3.1/topics/testing/overview/). We used the testing package [unittest](https://docs.python.org/3/library/unittest.html) to create a `TestCase` for each application:

- `views.py`: testing the correct pages are loaded and correct response codes are returned.
- `models.py`: testing whether objects are created, and whether their attributes match what we expect.
- `utils.py`: testing that specific utility functions return from the ORM what is expected of them.
- `handler.py`: testing that the responses to `GET` and `POST` requests behaved as expected.

We created multiple tests for each function, simulating behaviour on different (and sometimes erroneous) inputs to ensure that each function behaved in the way that we had anticipated.

To ensure that we'd covered as much of the code as possible, we used package [coverage](https://pypi.org/project/coverage/) to generate HTML documents detailing the statements we'd covered, and those that we'd missed.

![Coverage Report](../images/testing/coverage.png)

In total, we wrote **109** unit tests and have code coverage of **97%**.

<br>

## Integration Testing

<br>

Integration testing is extremely important to us given it simulates the interaction between all of the subcomponents of our app, and the way that the user eventually interacts with it.

The latter realisation led to our strategic decision to steer clear of traditional integration testing suites such as [selenium](https://pypi.org/project/selenium/) which requires dependency and subcomponent mocking, and typically involves testing individual isolated components of the web application. Instead, **we opted to use end to end testing** tool [cypress](https://www.cypress.io/) which we believe to be a much more valuable form of testing given that it **provides the most accurate emulation of how a user will interact with the app** (Guijarro, 2021).

Cypress also had the benefit of being **completely automated**, which allowed us to integrate our end to end tests into our CI/CD workflow. It also enabled us to run the same suite on different browsers - enabling us to identify compatibility issues on the fly (saving an immense amount of time debugging).

![gif](../images/testing/cypress/login.gif)

We used cypress specifically to test user interactions with the app - such as typing things into forms and submitting them, checking that our redirects on different pages are correct and testing table sorting or searching functionalities.

<br>

### Semi-Automation

<br>

Note that though Cypress enabled the full automation and testing of all components, we deliberately chose to exclude tests that involved creating new objects (such as creating new tasks or creating new responses) from our automated test suite, as the results of these influenced the state of the test database and the other subsequent integration tests.

These excluded tests have been tested **extensively** manually.

<br>

### Results

On our existing workflow, we run **152 end to end tests per browser, all of which pass.**.

<!-- > The strength of brand loyalty begins with how your product makes people feel. - Jay Samit -->

<br>

## Compatibility Testing

<br>

The principal users of our web application in a clinical and educational use case are likely to be accessing our solution using browsers such as **Internet Explorer** and **Microsoft Edge**, which both differ significantly to the **Google Chrome** and **Mozilla Firefox** browsers used in development.

Accordingly, compatibility testing - testing that the dependencies and libraries that we use are compatible with their browsers - is of paramount importance to ensuring that our end users can use our web application at all.

<div id="carouselCompatibility" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselCompatibility" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselCompatibility" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselCompatibility" data-bs-slide-to="2" aria-label="Slide 3"></button>
  </div>
  <div class="carousel-inner pb-4">
    <div class="carousel-item active">
      <img src="../images/testing/ie.png" class="d-block w-100" alt="Slide 1">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>Internet Explorer</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/firefox.png" class="d-block w-100" alt="Slide 2">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>Firefox</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/safari.png" class="d-block w-100" alt="Slide 3">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>Safari</h5>
      </div>
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselCompatibility" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselCompatibility" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

We've taken a semi-automated approach to compatibility testing:

- We use Cypress to run end-to-end tests on different browsers and from the command line.
- For the browsers that Cypress does not emulate (such as Internet Explorer), we've tested each page and action in the app manually.

To add another layer of certainty, we used tools like [caniuse](https://caniuse.com/) to test whether there are any compatibility conflicts with between the dependencies that we have and the browsers that our clients shall likely use. 

Historically, this has **allowed us to uncover the root cause of a number of compatibility issues** including HTML5 datepickers not being supported by Internet Explorer [and more](https://caniuse.com/?search=HTML5).

Having consulted tools like this throughout the project, and having performed compatibility testing across, numerous different browsers, we are **confident that our solution is compatible with Chrome, Firefox, Internet Explorer, Microsoft Edge, Safari, Opera and the mobile editions of these browsers**.

<br>

## Responsive Design Testing

<br>

Activity League is required to be general: usage in schools, clinics and for patients implies usage across a wide range of devices. Consequently, it is important to ensure that the web app's responsive design performs as it is intended to to ensure that the end user has a smooth experience and is able to interact with the web app.

To perform responsive design testing, we used [Chrome developer tools](https://developers.google.com/web/tools/chrome-devtools) to test the design and all functionality across a range of different devices. 


<div id="carouselResponsiveness" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="2" aria-label="Slide 3"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="3" aria-label="Slide 4"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="4" aria-label="Slide 5"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="5" aria-label="Slide 6"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="6" aria-label="Slide 7"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="7" aria-label="Slide 8"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="8" aria-label="Slide 9"></button>
    <button type="button" data-bs-target="#carouselResponsiveness" data-bs-slide-to="9" aria-label="Slide 10"></button>
  </div>
  <div class="carousel-inner pb-4">
    <div class="carousel-item active">
      <img src="../images/testing/responsive/add_multiple_participants.png" class="d-block w-100" alt="Slide 1">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPhone 5/SE</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/login.png" class="d-block w-100" alt="Slide 2">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPhone X</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/manage_group.png" class="d-block w-100" alt="Slide 3">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPhone 6/7/8</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/manage_users.png" class="d-block w-100" alt="Slide 4">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPhone 6/7/8</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/surveyor_dashboard_ipad.png" class="d-block w-100" alt="Slide 5">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPad Pro</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/surveyor_dashboard_mobile.png" class="d-block w-100" alt="Slide 6">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPhone X</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/task_history.png" class="d-block w-100" alt="Slide 7">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPhone 6/7/8</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/task_overview_ipad.png" class="d-block w-100" alt="Slide 8">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>iPad</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/task_overview_mobile.png" class="d-block w-100" alt="Slide 9">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>Google Pixel 2</h5>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../images/testing/responsive/task_overview.png" class="d-block w-100" alt="Slide 10">
      <div class="carousel-caption d-none d-md-block" style="bottom:-50px">
        <h5>Window Resizing</h5>
      </div>
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselResponsiveness" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselResponsiveness" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

Manual repsonsiveness testing initially alerted us to issues with the way that `Chart.js` rendered on smaller screens and in Activity League has always been a successful method of identifying responsiveness issues.

The conclusion of our Responsiveness testing is that **the web application is responsive across all display sizes that we have tested it with - retaining its slick UI and usability in all.** However, the manual nature of these tests is likely a source of error (however small) and future work on this project may seek to automate this process using tools such as [the Galen Framework](http://galenframework.com/), though unfortunately due to time constraints we were unable to attempt to incorporate this into Activity League.

<br>

## Performance Testing

<br>

Since our application is likely to be used by multiple organisations at the same time, it is important that the web app can function successfully under load. During our research, most performance testing solutions we could find offered limited functionality for free and required a paid plan for more thorough testing, such as testing pages which were only accessible after logging in.

One viable option we came across was [Lighthouse](https://developers.google.com/web/tools/lighthouse), an automated tool for reporting on performance and accessibility. Lighthouse audit is based on [Deque’s aXe](https://www.deque.com/axe/) core rules engine, which is among leading digital accessibility toolkits. Furthermore, since it is entirely free and integrated into Google Chrome's Developer Tools, we could test all the pages of our application. Running the audit generates a comprehensive report that gives information on all of the tests that passed in addition to the ones that failed. We've attached Lighthouse-generated reports for some of our pages below:

<br>

<div class="accordion accordion-flush" id="accordionFlushLighthouse">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Desktop Respondent Dashboard
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" >
      <div class="accordion-body">
      <iframe src="../lighthouse/desktop_respondent_dashboard.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Desktop Surveyor Dashboard
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" >
      <div class="accordion-body">
      <iframe src="../lighthouse/desktop_surveyor_dashboard.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingThree">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Desktop Surveyor Leaderboard
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" >
      <div class="accordion-body">
      <iframe src="../lighthouse/desktop_surveyor_leaderboard.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingFour">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseFour" aria-expanded="false" aria-controls="flush-collapseFour">
        Desktop Task Overview
      </button>
    </h2>
    <div id="flush-collapseFour" class="accordion-collapse collapse" aria-labelledby="flush-headingFour" >
      <div class="accordion-body">
      <iframe src="../lighthouse/desktop_task_overview.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingFive">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseFive" aria-expanded="false" aria-controls="flush-collapseFive">
        Desktop User Progress
      </button>
    </h2>
    <div id="flush-collapseFive" class="accordion-collapse collapse" aria-labelledby="flush-headingFive" >
      <div class="accordion-body">
      <iframe src="../lighthouse/desktop_user_progress.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingSix">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseSix" aria-expanded="false" aria-controls="flush-collapseSix">
        Mobile Respondent Dashboard
      </button>
    </h2>
    <div id="flush-collapseSix" class="accordion-collapse collapse" aria-labelledby="flush-headingSix" >
      <div class="accordion-body">
      <iframe src="../lighthouse/mobile_respondent_dashboard.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingSeven">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseSeven" aria-expanded="false" aria-controls="flush-collapseSeven">
        Mobile Surveyor Dashboard
      </button>
    </h2>
    <div id="flush-collapseSeven" class="accordion-collapse collapse" aria-labelledby="flush-headingSeven" >
      <div class="accordion-body">
      <iframe src="../lighthouse/mobile_surveyor_dashboard.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingEight">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseEight" aria-expanded="false" aria-controls="flush-collapseEight">
        Mobile Surveyor Leaderboard
      </button>
    </h2>
    <div id="flush-collapseEight" class="accordion-collapse collapse" aria-labelledby="flush-headingEight" >
      <div class="accordion-body">
      <iframe src="../lighthouse/mobile_surveyor_leaderboard.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingNine">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseNine" aria-expanded="false" aria-controls="flush-collapseNine">
        Mobile Task Overview
      </button>
    </h2>
    <div id="flush-collapseNine" class="accordion-collapse collapse" aria-labelledby="flush-headingNine" >
      <div class="accordion-body">
      <iframe src="../lighthouse/mobile_task_overview.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTen">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTen" aria-expanded="false" aria-controls="flush-collapseTen">
        Mobile User Progress
      </button>
    </h2>
    <div id="flush-collapseTen" class="accordion-collapse collapse" aria-labelledby="flush-headingTen" >
      <div class="accordion-body">
      <iframe src="../lighthouse/mobile_user_progress.html" title="description" width="100%" height="1000vh"></iframe>
      </div>
    </div>
  </div>
</div>

<br>

Looking deeper into these numbers, we can notice consistently that under the best practices section, we are continuously being penalised for a lack of https. This is something that we wanted to integrate, though decided not to due to time constraint, and the fact that we don't have a domain name, which complicates the process of obtaining a certificate.

<br>

## References

<br>

Guijarro, R., 2021. Testing Strategies for Modern Web Applications. [Blog] Medium, Available at: <https://medium.com/scopedev/testing-strategies-for-modern-web-applications-71836e480cc6> [Accessed 3 January 2021].

