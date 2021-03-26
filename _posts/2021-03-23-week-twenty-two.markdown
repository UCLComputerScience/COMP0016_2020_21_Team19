---
layout: post
title:  "Week Twenty-Two: Finishing Development"
date:   2021-03-23
categories: integration, testing, 
name: Team 19
---

This week we finished our unit and integration testing suites, and touched up a few details in our codebase to allow our repo to become publicly visible and open source.

## Testing


### Unit

Since we recently conducted a major refactoring of our code base, we needed to rewrite several of our unit test cases. We also needed to add entirely new test cases for new methods and functionality.

After finishing our new unit testing suite, we are pleased to have achieved 97% statement coverage.

![Coverage](/COMP0016_2020_21_Team19/assets/coverage.png)

### Integration

We also finished our integration test suite using [Cypress](https://www.cypress.io/).

![Coverage](/COMP0016_2020_21_Team19/assets/cypress.gif)

We also decided to create new [GitHub workflows](https://github.com/features/actions) to automate the integration testing, similar to our unit testing workflow.

To achieve this, we were able to use the [Cypress GitHub action](https://github.com/cypress-io/github-action) which runs the integration tests in headless browsers of our choosing. By default, this action supports testing on Chrome, Firefox and Edge. While we would have preferred to run our integration tests on all three of these browsers, since Microsoft Edge is not available on Linux, to run tests on Edge within GitHub Actions requires a [self-hosted Mac or Windows runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners). Consequently, we decided to go with Chrome and Firefox only and we feel this should be sufficient especially given that the newest version of Edge is based on Chromium and hence testing on Chrome should also cover the Edge case (pardon the pun).

## Secrets and publicising the repository

Up until this week, we had kept our repo private as our code contained sensitive information, namely the Django production key, database credentials, and API keys which we use to facilitate Google SSO.
We knew we could use [GitHub Secrets](https://docs.github.com/en/actions/reference/encrypted-secrets) to some extent to hide these keys, but our main concern was whether this would work with our continuous deployment flow.
After doing some research, we found out we could use [Docker secrets](https://docs.docker.com/engine/swarm/secrets/) to allow us to achieve what we wanted.

Now, instead of hard-coding the sensitive tokens in our `settings.py`, we simply set our tokens as enviromment variables which we can access by using the `os.getenv()` method in Python.
This requires us to make a local `secrets/` folder which contains several files, each containing one of these tokens. We also had to add the following section to our `docker-compose.yml`.

```yaml
web:
  ...
  ...
  environment:
    DB_USER_FILE: /run/secrets/db_user
    DB_PASSWORD_FILE: /run/secrets/db_password
    DEBUG: "True"
    EMAIL_HOST_FILE: /run/secrets/email_host
    EMAIL_HOST_PASSWORD_FILE: /run/secrets/email_host_password
    EMAIL_HOST_USER_FILE: /run/secrets/email_host_user
    GOOGLE_CLIENT_ID_FILE: /run/secrets/google_client_id
    GOOGLE_SECRET_FILE: /run/secrets/google_secret  
    SECRET_KEY_FILE: /run/secrets/secret_key
secrets:
  db_user:
    file: ./secrets/DB_USER
  db_password:
    file: ./secrets/DB_PASSWORD
  email_host:
    file: ./secrets/EMAIL_HOST
  email_host_password:
    file: ./secrets/EMAIL_HOST_PASSWORD
  email_host_user:
    file: ./secrets/EMAIL_HOST_USER
  google_client_id:
    file: ./secrets/GOOGLE_CLIENT_ID
  google_secret:
    file: ./secrets/GOOGLE_SECRET
  secret_key:
    file: ./secrets/SECRET_KEY
```

Each time our container is built, an environment variable containing the path to the secret file is created.

For example, `GOOGLE_CLIENT_ID_FILE` has the value `/run/secrets/google_client_id`. We then use the following shell script within the container to create an environment variable called `GOOGLE_CLIENT_ID_FILE` which has the value of the contents of the file.

```bash
set -e

file_env() {
   local var="$1"
   local fileVar="${var}_FILE"
   local def="${2:-}"

   if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
      echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
      exit 1
   fi
   local val="$def"
   if [ "${!var:-}" ]; then
      val="${!var}"
   elif [ "${!fileVar:-}" ]; then
      val="$(< "${!fileVar}")"
   fi
   export "$var"="$val"
   unset "$fileVar"
}

file_env "GOOGLE_CLIENT_ID"
```

We can then access the secret in our code using `os.getenv("GOOGLE_CLIENT_ID")`.

This means we can commit our code to VCS, without ever exposing the secrets as long as the `secrets/` directory is included in our `.gitignore`.

## Next Steps

Given that we have presented our code to both our TA and Dr Yun Fu, we have now stopped working on development. Our efforts are entirely focused on finishing other deliverables like the report website within the time constraint.
