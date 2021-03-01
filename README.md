# Activity League

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/pypi/pyversions/django)
![Coverage](./ActivityLeague/coverage.svg)
[![Django CI Actions Status](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/workflows/Django CI/badge.svg)](https://github.com/UCLComputerScience/COMP0016_2020_21_Team19/actions)

### UCL Project Report Website

The [`ucl`](ucl) directory has the Jekyll project which we will use to generate the static site being deployed on UCL servers.

Since the UCL servers cannot build the Jekyll site, we need to manually build the site and then copy the generated site into the `/cs/student/www/2020/group19/` directory on UCL servers.

- Run `jekyll build` in the [`ucl`](ucl) directory

- Copy the contents in the [`_site`](ucl/_site) direcory over to `/cs/student/www/2020/group19/` (through ThinLinc or SSH). This can be done easily with
    ```
    $ scp -r path/to/COMP0016_2020_21_Team19/ucl/_site/. UCLCSUSERNAME@csrw2.cs.ucl.ac.uk:/cs/student/www/2020/group19/
    ```

---

### Blog

To add a blog post:

- Create a new file in [`docs/_posts`](docs/_posts) named according to the following format:

    `YYYY-MM-DD-title.markdown`

- The file must have a header enclosed in `---`
    ```yml
    ---
    layout: post
    title:  "Post Title"
    date:   2020-10-20
    categories: cat1, cat2
    author: Name
    ---
    ```
    note that the `layout` must always be `post`

- To work on draft posts, simply place the file in the [`docs/_drafts`](docs/_drafts) directory.

- You can view a live preview of the blog post as you write it by running
    ```
    $ bundle exec jekyll serve --livereload
    ```
    or if the post is a draft
    ```
    $ bundle exec jekyll serve --livereload --drafts
    ```
    within the [`docs`](docs/) directory

- Once the post is complete, it can be pushed to GitHub
