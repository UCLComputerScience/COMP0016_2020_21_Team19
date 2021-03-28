---
title: Requirements
subtitle: Understanding the characteristics of the problem
layout: post
toc: true
---

## Project Background

Increasingly, hospitals are being mandated to monitor patient wellbeing post-treatment through Patient Reported Outcome Measures (PROMs). These are typically collected using questionnaires designed to receive subjective responses from patients to give a measure of the patient's sense of health and wellbeing. The questionnaires are often distributed in **paper form**, which dramatically increases the time that it takes to collect and analyse (given the questionnaires are mailed to the houses of the patients) and ultimately, the process of collecting and analysing the responses to these questionnaires can take **up to a year** to finalize (Background information about PROMs - NHS Digital, 2021).

![Patient Reported Outcome Measure (PROM) questionnaire](../images/requirements/prom_form.png)

This problem doesn't just exist in the clinic - it also exists in the classroom. The principles of PROMs are also directly applicable to teaching, for example: considering topic evaluation worksheets, module evaluation questionnaires and student feedback forms. Responses to these questionnaires can also provide vital feedback to educators in addition to clinicians, and operate on the same general principles. Yet in most classrooms across schools in Wales, these feedback forms are still distributed and collected using pen and paper despite the technology available to perform the same task digitally.

Our client, Dr Joseph Connor (NHS) has taken an active interest in resolving both of the issues defined above.

<br>

## Project Goals

<br>

The objectives of this project were to produce a **general** web app capable of gathering PROMs data per individuals, allowing clinicians to understand the factors that help and hinder an individual from adherence to set treatment plans in the clinic and the equivalent data in the classroom. If developed, the solution would significantly speed the time taken to create, collate, distribute and analyse responses to questionnaires in both clinical and classroom settings and prove immensely useful in both contexts.

<!-- > The strength of brand loyalty begins with how your product makes people feel. - Jay Samit -->

<br>

## Gathering Requirements

<br>


We identified our users by interviewing our client, who referred us to KS2 teachers (who in turn, referred us to KS2 students). Throughout this process, we sought a description of the environment where the problem was occurring using semi-structured interviews (Blandford, 2013) with open-ended questions – allowing us to probe further when needed. Examples of questions included:

<!-- Beginning of Questions to Teachers -->

Questions to teachers (answered by pseudo-users):​

<span style="color:blue">What is the greatest pain point during the process of collecting PROMs?​</span>

Distributing PROMs is okay. We have loads of PROM resources internally which allows me to find the ones that I need quickly. The pain point is really the amount of time that it takes to extract useful information from the responses that we get. We submit the questionnaires to patients not expecting to see the outcomes of it until a year from now, which I think really doesn’t need to be the case. 

<span style="color:blue">What do you think is the solution to this problem?​​</span>

I’m honestly not quite sure why we still mail these instead of using a website or something instead. I think it’d be much faster if we could send them all online, and then get their responses as soon as they’ve completed them, not until every single person has been chased up for a year to respond. 

<span style="color:blue">Who would be the potential users of this solution, other than yourself?​</span>

The patients, so that they can answer questions. 

<span style="color:blue">What format do you think would be most suitable for the final solution (e.g., mobile application, web application, wearable device)?​​</span>

Not a wearable device. These forms can be quite big sometimes, so I think they’d need something bigger than a phone to see it on, so a web app sounds best as far as I see it. It would be great if they could respond to this on their phone too though, in case they don’t have a computer. 

<span style="color:blue">Where would this solution (mainly) be used?​​</span>

I’ll be using it at my desk most of the time. I presume the patients will probably be using it at home. 

<span style="color:blue">When would this system be used?​​</span>

Every few days for me. Potentially more often for my colleagues. Ours normally go out in batches, so it’d really be used either when we get a response back or when we’re sending a batch out. 

<!-- End of Teacher Questions -->

<br>

## Personas

After interviewing our users, we created personas to represent the motivations and desires of the user (Nielsen, 2009). Doing this allows us to make the users more understandable and challenge our assumptions (Dam and Teo, 2020) about the user. We also created scenarios based on the interviews with our users to better understand the context of use, and to assist to evaluate the efficacy of our designs later.

<div id="carouselPersonas" class="carousel carousel-dark slide mb-3" data-bs-ride="carousel">
  <div class="carousel-indicators" style="bottom:-30px">
    <button type="button" data-bs-target="#carouselPersonas" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselPersonas" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselPersonas" data-bs-slide-to="2" aria-label="Slide 3"></button>
    <button type="button" data-bs-target="#carouselPersonas" data-bs-slide-to="3" aria-label="Slide 4"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../images/requirements/personas/clinician.jpg" class="d-block w-100" alt="Clinician Persona">
    </div>
    <div class="carousel-item">
      <img src="../images/requirements/personas/patient.jpg" class="d-block w-100" alt="Patient Persona">
    </div>
    <div class="carousel-item">
      <img src="../images/requirements/personas/teacher.jpg" class="d-block w-100" alt="Teacher Persona">
    </div>
    <div class="carousel-item">
      <img src="../images/requirements/personas/student.jpg" class="d-block w-100" alt="Student Persona">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselPersonas" data-bs-slide="prev" style="left:-80px">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselPersonas" data-bs-slide="next" style="right:-80px">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

<br>

## Use Cases
<div class="btn-group">
  <button id="zoomInButton" type="button" class="btn btn-primary">Zoom In</button>
  <button id="zoomOutButton" type="button" class="btn btn-primary">Zoom Out</button>
  <button id="resetButton" type="button" class="btn btn-primary">Reset</button>
</div>
<input id="rangeSlider" class="range-input" type="range" min="0.1" max="3" step="0.01" value="1">
<div class="border border-3 border-dark mt-3">
  <img id="overall-class-diagram" src="../images/requirements/use-case.svg" alt="Use Case Diagram">
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
  maxScale: 3
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

## MoSCoW Requirements

<br>

<div class="accordion accordion-flush" id="accordionFlushExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
        Must Have
      </button>
    </h2>
    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" >
      <div class="accordion-body">
        <table class="table table-hover table-responsive">
          <thead>
            <th>Requirement</th>
            <th>Type</th>
          </thead>
          <tbody class="table-success">
            <tr>
              <td>Surveyors can collect feedback from respondents.​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Surveyors can set tasks containing qualitative and quantitative responses.​​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>System is accessible via a web-browser.​​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Surveyors must be able to see individual Responses to a task.​​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Surveyors must be able to create and manage groups of Respondents that they can assign tasks to collectively.​</td>
              <td>Non-functional</td>
            </tr>
            <tr>
              <td>The ability to score and rank Respondents by the responses that they generate on a league table.​</td>
              <td>Non-functional</td>
            </tr>
            <tr>
              <td>Respondent should be able to see the tasks that they have been assigned to complete.​​​</td>
              <td>Non-functional</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingTwo">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
        Should Have
      </button>
    </h2>
    <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingTwo" >
      <div class="accordion-body">
        <table class="table table-hover table-responsive">
          <thead>
            <th>Requirement</th>
            <th>Type</th>
          </thead>
          <tbody class="table-info">
            <tr>
              <td>Summary visualisations for groups​.​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Create and reuse Task templates​.​​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Responsive to different display sizes​.​​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Visualisations for the breakdown of responses to a question.​​​</td>
              <td>Non-functional</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingThree">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
        Could Have
      </button>
    </h2>
    <div id="flush-collapseThree" class="accordion-collapse collapse" aria-labelledby="flush-headingThree" >
      <div class="accordion-body">
        <table class="table table-hover table-responsive">
          <thead>
            <th>Requirement</th>
            <th>Type</th>
          </thead>
          <tbody class="table-warning">
            <tr>
              <td>Attach links to questions and track number of link clicks for each question​.​​</td>
              <td>Functional</td>
            </tr>
            <tr>
              <td>Word clouds to visualise text responses​.​​​</td>
              <td>Non-functional</td>
            </tr>
            <tr>
              <td>Modify the way that a question is scored​​.​​​</td>
              <td>Non-functional</td>
            </tr>
            <tr>
              <td>Dedicated page for visualising group progress over time​.​​​</td>
              <td>Non-functional</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingFour">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseFour" aria-expanded="false" aria-controls="flush-collapseFour">
        Won't have
      </button>
    </h2>
    <div id="flush-collapseFour" class="accordion-collapse collapse" aria-labelledby="flush-headingFour" >
      <div class="accordion-body">
        <table class="table table-hover table-responsive">
          <thead>
            <th>Requirement</th>
            <th>Type</th>
          </thead>
          <tbody class="table-danger">
            <tr>
              <td>Feedback forms will not contain any task-specific content and should only be used as a mechanism to gather feedback.​​</td>
              <td>Functional</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<br>

## References

NHS Digital. 2021. Background information about PROMs - NHS Digital. [online] Available at: <https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/patient-reported-outcome-measures-proms/background-information-about-proms> [Accessed 17 November 2020].

Kovacevic, D., 2018. Patient Reported Outcome Measure (PROM) feedback form.. [image] Available at: <https://www.researchgate.net/profile/David-Kovacevic/publication/326524497/figure/fig1/AS:652804830011402@1532652208322/Patient-Reported-Outcomes-Measurement-Information-System-PROMIS-Global-10-form.png> [Accessed 21 March 2021].

Nielsen, L. (2009). Personas. [online] The Interaction Design Foundation. Available at: https://www.interaction-design.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/personas. [Accessed 8 November 2020]​

Dam, R.F. and Teo, Y.S. (2020). Learn How to Use the Best Ideation Methods: Challenge Assumptions. [online] The Interaction Design Foundation. Available at: https://www.interaction-design.org/literature/article/learn-how-to-use-the-best-ideation-methods-challenge-assumptions. [Accessed 8 November 2020]​

