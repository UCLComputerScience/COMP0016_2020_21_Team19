---
layout: post
title:  "Week Seventeen: Unit Testing and Client Feedback"
date:   2021-02-16
categories: unit-testing
name: Team 19
---

## This week

This week, we received feedback from our client on their initial thoughts on the solution, what worked, what didn't and what they'd like to see from us in the future. Whilst this feedback was coming in however, we performed unit-testing.

## Unit Testing

In accordance with the suggestions made by [django's testing documentation](https://docs.djangoproject.com/en/3.1/topics/testing/overview/), we used the `unittest` package to conduct unit tests. 

After creating an application in django for the first time using the `startapp` command, django pre-builds a `tests.py` file as part of the new application. We didn't like this structure, as this would have forced all of our unit tests for all components of the application (models, views, templates, ...) into a single file. We discovered we [weren't the only ones](https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#testing-reusable-applications) who thought that we could make things a lot neater by creating individual files containing tests for other files, and replicating the file structure of our application in the tests to make them as easily accessible as possible:

```
ActivityLeague    
│
|   ...
|
└───respondent
│   │   models.py
│   │   views.py
|   |   forms.py
|   |   ...
│   │
│   └───tests
│       │   test_models.py
│       │   test_views.py
│       │   test_forms.py
```

For integration testing, [unittest](https://docs.python.org/3/library/unittest.html) was everything that we needed. It supported: 

- **Test Fixtures**: The ability to perform pre-test and cleanup actions. Useful for us creating objects/pre-populating the database.
- **Test Cases**: For the most basic unit assertions.
- **Test Suites**: The ability to for us to group tests that belong together togther, for example, having numerous tests on a class or a method.
- **Test Runner**: The ability to execute all of the tests and display to us the output and what went wrong.

We subsequently unit-tested every file that we had, and obtained a statement coverage of **94%**. However, we expect to have to clean this up in the coming weeks and add more functionality to our solution, so this will have to be built upon.

Unit testing served as a form of validation for us that our code did what we wanted it to do. Fortunately, given our extensive hands on testing that we had been doing when we were building new functionality, and given the visual nature of our project, we discovered very few new bugs and resolved those that we had identified.

The full suite of tests that we wrote are available on our [repo](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19) at commit `81119b2afdb8579c3ef8d7570d9e9f4f36c8d1a4`.

During testing, we made the assumption that everything coming from django itself will work. 

As would likely be anticipated, the vast majority of our tests concerned our most dense files: `views.py` which contains a lot of the business logic of the application. 

## Updating our workflow

Given our new suite of unit tests, we also decided to integrate this into our existing workflow using GitHub actions. Now, every time that we push to the `main` branch, we also execute our unit tests.

This has the unseen benefit of informing us if any changes that we make to the codebase in the future result in bugs or breakages in the functionality that we have already implemented, and is likely to save us a lot of time going forward which we otherwise have spent looking for the origin of a bug.

The configuration of this workflow can also be found on our [repo](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19) at commit `81119b2afdb8579c3ef8d7570d9e9f4f36c8d1a4`.

## Client Feedback

We also received feedback on the first proper iteration of our web app. The feedback was largely negative for a reason that we had not previously considered: the client had accessed our application through Internet Explorer, whose last update was in 2013. Subsequently we realised that some of the technologies that we had employed were incompatible with Internet Explorer, for example: 

- The datepicker element in HTML5 (we had to introduce another type of datepicker in the event that the browser was incompatible using JavaScript)
- Ajax not supporting `json` as a `repsonseType`
- jQuery is not supported at all

The above was discovered using [this tool](https://caniuse.com/) which is greatly useful in informing you which browsers might be incompatible with the dependencies being used.

## Next Steps

Over the course of the next week, we've identified a number of areas in which our solution may be improved. These include:

- Resolving existing compatibility issues with Internet Explorer and Edge (the two browsers mainly used by the NHS) 
- Allowing users to be added to the platform in bulk via spreadsheets
- The ability to mark tasks as complete