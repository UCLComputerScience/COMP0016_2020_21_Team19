---
layout: post
title:  "Week Thirteen: CRUD, Visualisations, and the Elevator Pitch"
date:   2021-01-19
categories: backend, visualisations, crud
name: Team 19
---

This week we continued to work on the backend. Our focus was primarily on adding visualisation tools to the app and finishing up elements of the app with CRUD functionality.
We also presented our elevator pitch this week - introducing our project to the rest of the year group and the module staff.

## CRUD

The majority of the components of our app which are involved with CRUD functions have now been implemented.
This includes but is not limited to:

- Creating new Tasks
- Responding to Tasks
- Creating new Groups
- Display tasks dynamically on both user dashboards
- View task specific information upon clicking it from the dashboard
- Having a dynamic leaderboard

This was achieved using a combination of build-in Django features (such as the [Forms API](https://docs.djangoproject.com/en/3.1/ref/forms/)), [jQuery](https://jquery.com/) and [Ajax](https://en.wikipedia.org/wiki/Ajax_(programming)) techniques. Overall, this was not too difficult but–due to our collective lack of experience with web development–required some time to get familiar with.


## Visualisations

An important requirement of our project is for the both the Surveyor and Respondent to be able to view data in a simple, yet detailed manner. To that end, we implemented some visualisations using [Chart.js](https://www.chartjs.org/) for charting, and [jQuery](https://jquery.com/) for data retrieval.

Please note that while the functionality to make the visualisations work has been implemented, we understand there is some room for refinement with regards to styling and formatting. We aim to address this within the coming week(s).

### Surveyor

#### Dashboard

![Surveyor Dashboard](/COMP0016_2020_21_Team19/assets/surveyor_dashboard_13.png)

The Surveyor dashboard now shows a range of dynamic graphs of the average score of different groups. This will allow the Surveyor to quickly gauge a group's progress and inform the tasks that they may need to set.

### Task Overview

![Surveyor Task Overview](/COMP0016_2020_21_Team19/assets/surveyor_task_13.png)

The Task Overview page now features functional pie charts, providing the breakdown of responses to different questions within the task.

### Respondent

![Respondent Progress](/COMP0016_2020_21_Team19/assets/respondent_progress_13.png)

The Respondent interface now features a brand new "Progress" page which displays their progress among different groups through interactive line charts.


## Elevator Pitch

As part of the module assessment, we were required to present an Elevator pitch on 15 January.
This was a great opportunity for us to present the problem our project sought to solve, and how we intended to address it.

We allocated time to meet as a group and prepare this short presentation, keeping in mind that our delivery needed to be informative, engaging yet concise. Following the presentation, we were pleased to hear at our next meeting that out client thought we met these requirements.

![Slide 1](/COMP0016_2020_21_Team19/assets/presentation/1.png)
![Slide 2](/COMP0016_2020_21_Team19/assets/presentation/2.png)
![Slide 3](/COMP0016_2020_21_Team19/assets/presentation/3.png)
![Slide 4](/COMP0016_2020_21_Team19/assets/presentation/4.png)

## Next Steps

We will now focus our efforts to integrating an SSO solution with our web app. Our client has recommended [Keycloak](https://www.keycloak.org/) and we will be exploring this for Identity and Access Management. Completing this will be a big step towards the completion of our web app.

It has also become evident that there is a need for Surveyors to be able to manage different groups within the system and this is a feature we will implement this coming week.