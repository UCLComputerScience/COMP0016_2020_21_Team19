---
layout: post
title:  "Week Nineteen: Organisations & Invitations"
date:   2021-03-02
categories: models, architecture, documentation, invitations
name: Team 19
---

This week we made some major changes to the structure of our system, and also began working on the documentation.

## Restructuring & Invitations

Our client had suggested to us that our focus should be on making a generalised system which could be used by not only the NHS, but schools, companies and any other body which relies on accurate user-reported outcomes. As such, we decided the best way to fulfil this requirement would be by introducing `Organisation`s as a model in our system.

### Organisations

The idea of having a high-level `Organisation` entity required some thought, especially in regards to how they would be created, how users would be assigned to them, and whether there needed to be users with special privileges to manage them.

We initially considered the approach of having `Organisation`s being closed off entirely to end users and for their creation to be handled entirely by system administrators (us). However, this felt like a poor solution as, given our system will be open source, having a "Contact Sales"-esque sign up requirement just adds an additional step to the sign up procedure without any real advantage. We also didn't like how this added a layer of human intervention which was unnecessary.

Ultimately, the solution we decided to implement follows this workflow:

- A single `Surveyor` can sign up, creating an `Organisation` in the process.
  - This `Surveyor` is assigned as the `admin` for the `Organisation`
- They can invite other `Surveyor`s to their organisation and `Respondent`s to specific groups which they create.
- Each `Surveyor` in an organisation has their own `Group`s which they manage.
- Any `Surveyor` may invite more `Surveyor`s to the organisation, but only the `admin` of the organisation can delete them.

Since we now have this organisational flow, it follows that new sign ups be restricted only to `Surveyor`s wishing to create a new organisation. As such, `Surveyor`s wishing to join an `Organisation` and `Respondent`s who need to be added to a group can only sign up through an invitation received via email.

### Invitations

The sign up page now shows the following message to users who try to sign up at `/accounts/signup` without an invite

![Sign Up Closed](/COMP0016_2020_21_Team19/assets/sign-up-closed.png)

This page only allows sign ups to users who have been redirected to it via a valid invite link.

`Surveyor`s wishing to join an `Organisation`, can do so through `/create-organisation`.

To handle this new inviation sign up flow, we found a package which seemed to be a perfect fit.

#### django-invitations

After reading the brief (and very confusing) documentation this package had to offer, we were struggling to struggling to understand how exactly we would go about implementing this feature.

The main issue we faced was distinguishing between invitations sent to `Surveyor`s and `Respondent`s, such that we could have the same sign up procedure for both user types and abstract away as much of the complexity as possible.

Failing to adapt the package's existing functionality to fit our needs, we were forced to define our own custom invitation which had the following additional instance fields compared to the base invitation model the package came with.

```python
class UserInvitation(AbstractBaseInvitation)
    ...
    ...
    instance = cls._default_manager.create(
        email=email,
        key=key,
        inviter=inviter,
        organisation=organisation,
        group=group,
        is_respondent=is_respondent,
        **kwargs
    )
```

This allows us to streamline the sign up process, without having to define custom forms for each user type as we can simply access the `Invitation` object at time of sign up.

We found this package extremely difficult to work with—even though it provided some good functionality—almost entirely due to its terrible documentation. We will be considering contributing to this package's documentation and source code to help future developers who may seek similar functionality in their Django app.

### Managing Users and Organisations

Since `Surveyor`s now have to be invited to join an `Organisation`, we added the following page to allow `Surveyor`s to do so.

![Organisation](/COMP0016_2020_21_Team19/assets/organisation.png)

Users can be invited through their email.
Following some feedback received from our client, we also added the ability to invite multiple users through uploading a `.xlsx` spreadsheet. This applies to both inviting `Respondent`s to groups and `Surveyor`s to `Organisation\`s.

![Add Respondent](/COMP0016_2020_21_Team19/assets/add-respondent.png)

![Add Multiple](/COMP0016_2020_21_Team19/assets/add-multiple.png)

## Enhancements

We made some minor enhancements to existing features, as suggested by our client's feedback.

### Complete Tasks

`Surveyor`s can now mark tasks as completed, removing them from the dashboard.

![Marking Tasks](/COMP0016_2020_21_Team19/assets/task-overview-mark-complete.png)

These tasks are shown only in the Task History page which shows all tasks that a `Surveyor` has ever created.

### Bar & Pie Charts

There is now the ability to toggle between pie and bar charts in the Task Overview page.

![Pie/Bar Charts](/COMP0016_2020_21_Team19/assets/task-overview-pie-bar.png)

## Sphinx Documentation

We also began formally documenting our code in detail using Sphinx.

This allows us to convert docstrings (see format below) to HTML very easily.

```python
def sanitize_link(url):
    """
    Removes the protocol from the given URL.
    :param url: The URL to be sanitized
    :type url: str
    :return: The sanitized URL.
    :rtype: str
    """
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)
```

## Next Steps

Over the coming week, we intend to implement some final functionality and resolve a few bugs pointed out by our client.
Alongside this we hope to make significant progress on out report website, User Manual, and Documentation, which will be deployed online shortly.
