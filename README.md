# NHS4 Activity Diary

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
