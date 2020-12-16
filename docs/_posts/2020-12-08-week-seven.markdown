---
layout: post
title:  "Week Seven"
date:   2020-12-08
categories: sso, system architecture, linode, frontend, backend
name: Team 19
---

This week, our primary focus was on completing the front end, devising a system architecture diagram for our client and beginning the implementation of the back end. Similar to previous weeks, we have continued to meet as a team on a (almost) daily basis as we have found that collaborative programming has been a very effective approach thus far.

# Frontend

We have implemented the majority of the frontend. However, it is currently all hardcoded and not integrated with the Django backend - this is something we will be working on in the coming week. Although there are some further refinements to be made on the frontend, we feel are only minor concerns which can be resolved after some progress has been made on the backend, which is a more important task at this stage of the development cycle.

We created the following pages following our Figma prototype as a guide and point of reference.

![Login Screen](/COMP0016_2020_21_Team19/assets/login.png)
*Login Screen*

## Interviewee Interface

![Interviewee Dashboard](/COMP0016_2020_21_Team19/assets/interviewee_dashboard.png)
*Interviewee Dashboard*


![Interviewee Leaderboard](/COMP0016_2020_21_Team19/assets/interviewee_leaderboard.png)
*Interviewee Leaderboard*


![Response](/COMP0016_2020_21_Team19/assets/response.png)
*Response*

## Interviewer Interface

![Interviewer Dashboard](/COMP0016_2020_21_Team19/assets/interviewer_dashboard.png)
*Interviewer Dashboard*


![Interviewer Leaderboard](/COMP0016_2020_21_Team19/assets/interviewer_leaderboard.png)
*Interviewer Leaderboard*


![Task Overview](/COMP0016_2020_21_Team19/assets/task_overview.png)
*Task Overview*


![New Task](/COMP0016_2020_21_Team19/assets/new_task.png)
*New Task*

# Linode

Our client asked us to decide on a Linode server for our project, for which we opted for the following specification:
Ubuntu 20.10, Nanode 1GB: 1 CPU, 25GB Storage, 1GB RAM.
We feel this is sufficient for the time being, given our scale of deployment.

# Next Steps

## Backend

We will now begin implementing backend functionality by configuring Django to work with MySQL and our existing database schema.

![Database Schema](/COMP0016_2020_21_Team19/assets/database_schema.png)

Fortunately, from our preliminary research it seems there is plenty of documentation and guidance about using MySQL with Django.


## SSO and Authentication

After consulting with our client and a team who our client referred us to, we will be exploring Keycloak to allow single sign-on with Identity and Access Management.
