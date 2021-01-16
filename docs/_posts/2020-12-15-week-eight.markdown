---
layout: post
title:  "Week Eight: Integrating the Database, Configuring CI/CD"
date:   2020-12-15
categories: sso, system architecture, linode, backend, docker, ci, cd
name: Team 19
---

## Linode

Since our last meeting, our client has provided us with access to a Linode server with the same specifications as we had outlined last week. We began this week by configuring this server to be more secure by setting up firewalls, adding key-based authentication for SSH and creating a new user with virtually no privileges, which will be used to host the application.

## Dockerising the Application

This week we tasked ourselves with deploying our application to our new Linode server. 

To avoid dependency issues and ensure that our application would run inside the new server, we decided to dockerise the application.

To do this, we first attempted to dockerise the image locally. Following the official docker documentation, we attempted to do this using ```docker build```, but given that we were no longer using Django's default choice of database (SQLite) which is embedded in Django projects, this failed, and the database locally was a nightmare connecting to the docker container containing the project. After additional research, we discovered that there was an easier approach to integrate the database into our new docker image. To do this, we'd use ```docker-compose build``` and would compose a new image consisting of our existing project and a PostgreSQL image. 

This was initially a success, and we were able to dockerise the application. However, we realised that after every time that we rebuilt the image, the state of the database was destroyed. This left us with a dilemma - we could either:
* Save the state of the database within the docker image. This would allow us to continue using the same data during development and prevent us from having to either manually add dummy data each time the application was built for testing (or automate the process).
* Have a state saved locally in which our docker image's database would connect to.

We decided on the latter, given saving the state of the database in the docker image itself was likely to blow the size of the image up significantly, to the point at which it might not be runnable on our light server!

Subsequently, we managed to resolve this issue using ```volumes```. This essentially consisted of pointing our postgres ```db``` image to ```/var/lib/postgres/data``` on each machine that the image is run. We realised that actually, not preserving the state of the database in the image was what we wanted, as it means we won't have access to confidential patient information once they start using the application). What we really cared about was whether the state of the database was preserved across builds. Now that we had resolved this problem locally, we tried to automate the same process on the Linode server.

## Continuous Integration & Deployment

After much initial research on how to get started with this, we came to the conclusion that the easiest (and conveniently, most commonly implemented mechanism) for continuous integration (CI) and continuous deployment (CD) was to use GitHub actions.

While our existing research had shown this was a great way to automatically run integration tests, it hadn't answered the biggest questions: how are we going to deloy the docker image to Linode?

Our options as we saw them were:
1. Use ```rsync``` or ```scp``` to copy over the latest image as and when we had built it (though this isn't really CD).
2. Write a script locally which detected new images locally and sent the latest image to Linode.

Neither of these options appeared suitable, and both were susceptible to numerous issues:
* Our script which detected local builds would not differentiate between working and failing builds, and would send it over to Linode.
* If two of us were working on two different features at the same time, we might not see our changes on Linode at all as the latest built image might be from the other person working on the project - resulting in time potentially wasted debugging an issue that does not exist.
* If two of us were working simultaneously and one had made a change to the structure of the database, the existing data might be invalidated and the break the entire application for the other (whose edition does not reflect these latest changes).

We weren't quite sure how to get around these issues, until we encountered: https://docs.github.com/en/free-pro-team@latest/actions/guides/publishing-docker-images (hosting our latest docker image using either DockerHub or GitHub Packages), which was immediately seen as a much more appropriate solution to our problems.

After investigating both options, we decided to use GitHub packages as we realised publishing to DockerHub involves being part of a paid plan.

The guide above taught us to create ```publish.yaml``` and use GitHub workflows, which we configured to use our ```main``` branch as our production/release version of the Django project. Hence, every time that we push/merge a commit to the ```main``` branch, GitHub builds our docker image and hosts it in our repository as a GitHub package.

This wasn't easy, given none of the three of us had any prior experience using GitHub workflows or any significant experience using Docker and required several days of experimentation before we were actually able to get it working.

However, even with these latest works, we still hadn't resolved our initial issue: How do we get our latest version onto Linode?

## WatchTower

In the process of researching answers to "How to automatically deploy the latest version of a GitHub package in a Linode server?" we came across WatchTower (https://github.com/containrrr/watchtower), a solution to this exact problem that we had. After setting up WatchTower on Linode, we tested to see whether making and committing small changes to our ```main``` branch would result in a pull-down and rebuild of the Linode image, which it did. 

## Summing Up

Our intense process of creating our GitHub actions, and CI/CD had enabled us to autonomously rebuild and host the latest version of the application that we were developing on Linode. 

This was an intense learning experience which we have not yet seen the benefits of yet, but I am sure that we shall in future.

## Next Steps

Next week we intend to properly integrate our backend functionality with the work that we have completed to-date on the frontend. This involves ensuring adding elements to and removing elements from the database, implementing visualisations to our user's pages and making the outwards-facing functional elements work. 