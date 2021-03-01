---
layout: post
title:  "Week Twelve: Integrating the Backend with the Frontend"
date:   2021-01-12
categories: backend, frontend, visualisations
name: Team 19
---

This week we began to work on integrating the backend of our web application with the frontend. This primarily involved making the different
pages of the user interface dynamic depending on the information stored in the database, rather than being hardcoded.

## Current Progress

### Surveyor

One of main features we implemented was the ability for surveyors to create new tasks and assign them to groups. When creating these tasks,
there is the option to dynamically add as many questions as required to the feedback form, as well as selecting the type of question from
"Likert Scale", "Traffic Light", or "Word Cloud".

![New Task](/COMP0016_2020_21_Team19/assets/create_new_task.png)

After a new task is created, this will be shown on the surveyor's dashboard. The description of the task will be shown along with the group
it has been assigned to, the number of people within that group, the number of people who have completed the task, and the due date.

![Surveyor Dashboard](/COMP0016_2020_21_Team19/assets/surveyor_dashboard.png)

Surveyors also now have the ability to create new groups. As of yet there is no way to assign respondents to this group, however this is
functionality which we will be looking to implement within the following week.

![New Group](/COMP0016_2020_21_Team19/assets/create_new_group.png)

### Respondent

As we did for the surveyor, we also changed the respondent dashboard to be integrated with the backend; showing tasks dynamically by retrieving
them from the database.

![Respondent Dashboard](/COMP0016_2020_21_Team19/assets/respondent_dashboard.png)

A new page that has been added for the respondent is the progress page. This page displays a series of graphs to show the user's progress,
both overall and within specific groups. Each of the graphs has the x-axis representing time, and the y-axis representing the score. This
score is calculated by a scoring function based off the responses they have given to tasks using the feedback forms. As of yet this scoring function simply computes an average of the likert value responses from the feedback form.

![Respondent Progress Page](/COMP0016_2020_21_Team19/assets/respondent_progress_page.png)


## Next Steps

Next week we will continue working to integrate the backend of our system with the frontend. This will include displaying a task overview page
if the surveyor clicks on one of the tasks on their dashboard. This overview will include a pie chart detailing all of the likert value
responses for the questions on the feedback form.

Also, the surveyor dashboard should show a series of graphs and leaderboards to detail the progress of each of the groups that they manage.