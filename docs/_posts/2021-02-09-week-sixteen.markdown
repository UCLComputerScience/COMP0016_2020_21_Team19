---
layout: post
title:  "Week Sixteen: Refining the Prototype"
date:   2021-02-09
categories: refining, prototype, frontend
name: Team 19
---

Having shared our server IP with our client last week, we awaited user feedback to inform the next steps of our development. Nevertheless, this week we made some minor refinements to our application, focusing on increasing user-friendliness, and touching up some areas that our client pointed out in the live demo last week.

## Improvements

### Managing groups

The page for managing participants of a group was improved by making the delete button larger, coloured and styled to fit the theme of the rest of our website.

Some new functionality was also added, with the Surveyor now being able to delete entire groups.

![Old Delete Button](/COMP0016_2020_21_Team19/assets/group-delete-old.png)

![New Delete Button](/COMP0016_2020_21_Team19/assets/group-delete-new.png)

Clicking the delete button now also displays a browser popup asking for confirmation.

![New Delete Button](/COMP0016_2020_21_Team19/assets/group-delete-popup.png)

### Pages with no content

Previously, pages which did not have any content (e.g. the dashboard for a Respondent with no assigned tasks) appeared empty, providing no explanation to the user. We resolved this by simply adding an `if` statement within the Django templates to show a message if there was no content for that page. We were able to achieve the same affect for dynamically rendered content using JavaScript.

![Empty Pages](/COMP0016_2020_21_Team19/assets/no-tasks.png)

### Explaing the Score

During the live demo, our client rightly pointed out that although we had displayed scores for different tasks and groups, there was a lack of clarity about what these actually represented.

We decided the most elegant way to solve this would be to include a `tooltip` triggered by mouse hover explaining the score and its computation.

![Score Explanation Tooltip](/COMP0016_2020_21_Team19/assets/score-explanation.png)

### Traffic Light Responses

The traffic light responses previously were aligned to the left of the page which looked odd since there was a large empty space to the right. Also, each traffic light `btn` element also contained within it a `radio` button which occasionally lead to some weird rendering. Both these issues were easily resolved and now look much cleaner.

![New Traffic Light](/COMP0016_2020_21_Team19/assets/traffic-light-new.png)

## Next Steps

We have created GitHub issues for some features we need to implement such as an email invite system, and the ability for Surveyors to view an indivual Respondent's history. Implementing a test suite for our application within the coming weeks is also a priority.

Following this, the next stages of development will be guided almost entirely by user feedback.