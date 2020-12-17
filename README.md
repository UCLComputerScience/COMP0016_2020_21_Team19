# Activity League

### Working with Django

#### Clone this repo

Paste one of the below lines into terminal (depending on if you use SSH or HTTPS with `git`)

SSH
```bash
git clone git@github.com:UCLComputerScience/COMP0016_2020_21_Team19.git; cd COMP0016_2020_21_Team19; python -m venv venv; source venv/bin/activate; pip install -r requirements.txt;   
```
HTTPS
```bash
git clone https://github.com/UCLComputerScience/COMP0016_2020_21_Team19.git; cd COMP0016_2020_21_Team19; python -m venv venv; source venv/bin/activate; pip install -r requirements.txt;   
```
This will:
- Clone the repository
- `cd` into to the `COMP0016_2020_21_Team19` directory
- Create a new virtual environment and install all the requirements

---

### UCL Project Report Website

The [`ucl`](ucl) directory has the Jekyll project which we will use to generate the static site being deployed on UCL servers.

Since the UCL cannot build the Jekyll site, we need to manually build the site and then copy the generated site into the `/cs/student/www/2020/group19/` directory on UCL servers.

- Run `jekyll build` in the [`ucl`](ucl) directory

- Copy the contents in the [`_site`](ucl/_site) direcory over to `/cs/student/www/2020/group19/` (through ThinLinc or SSH)


---

### The blog is ready to host content.

To add a blog post:

- Create a new file in [`docs/_posts`](docs/_posts) named according to the following format:

    `YEAR-MONTH-DAY-title.markdown`
    
    Where `YEAR` is a four-digit number, `MONTH` and `DAY` are both two-digit numbers

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
